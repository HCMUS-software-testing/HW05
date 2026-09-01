#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const base = process.env.BASE_URL || "http://localhost:3000";
const args = Object.fromEntries(process.argv.slice(2).reduce((a, x, i, arr) => {
  if (x.startsWith("--")) a.push([x.slice(2), arr[i + 1] && !arr[i + 1].startsWith("--") ? arr[i + 1] : true]);
  return a;
}, []));
const scenario = String(args.scenario || "load");
const profiles = {
  load: { concurrency: 3, iterations: 8 },
  stress: { concurrency: 1, iterations: 5, levels: [3, 6, 12] },
  spike: { concurrency: 2, iterations: 4, spikeConcurrency: 12 },
  soak: { concurrency: 2, duration: Number(args.duration || 600) },
};
if (!profiles[scenario]) throw new Error(`Unknown scenario: ${scenario}`);
const profile = profiles[scenario];
const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
const outDir = path.join(root, "jmeter", "results", scenario);
const out = path.join(outDir, `23127185_${scenario}_${new Date().toISOString().slice(0, 10).replaceAll("-", "")}.jtl`);
const rows = [];
const csvEscape = v => `"${String(v).replaceAll('"', '""')}"`;
const csvHeader = "timeStamp,elapsed,label,responseCode,success,bytes,threadName,grpThreads,allThreads,URL,Latency,Connect,ErrorCount,FailureMessage";
const write = () => {
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(out, [csvHeader, ...rows.map(r => r.map(csvEscape).join(","))].join("\n") + "\n");
};

async function call(label, method, url, body, token) {
  const started = Date.now();
  let code = 0, data = null, error = "";
  try {
    const res = await fetch(base + url, { method, headers: { "content-type": "application/json", ...(token ? { authorization: `Bearer ${token}` } : {}) }, body: body == null ? undefined : JSON.stringify(body) });
    code = res.status;
    const text = await res.text();
    try { data = JSON.parse(text); } catch { data = text; }
    if (!res.ok) error = typeof data === "object" ? JSON.stringify(data) : String(data);
  } catch (e) { error = e.message; }
  const elapsed = Date.now() - started;
  rows.push([Date.now(), elapsed, label, code, error ? "false" : "true", JSON.stringify(data || "").length, "workflow", 1, 1, base + url, elapsed, 0, error ? 1 : 0, error]);
  return { code, data, error, elapsed };
}

async function workflow(worker, iteration) {
  const email = `m2-${Date.now()}-${worker}-${iteration}@example.com`;
  const password = "Password123!";
  const name = `Mai Test ${worker}-${iteration}`;
  const out = [];
  out.push(await call("Register", "POST", "/api/register", { name, email, password }));
  out.push(await call("Login", "POST", "/api/login", { email, password }));
  const login = out[out.length - 1];
  const token = login.data && login.data.token;
  out.push(await call("Categories", "GET", "/api/categories"));
  out.push(await call("ProductList", "GET", "/api/products?search=i"));
  out.push(await call("ProductDetail", "GET", "/api/products/1"));
  const item = { id: 1, name: "iPhone 15 Pro Max", price: 30000000, quantity: 1 };
  out.push(await call("AddToCart", "POST", "/api/cart", item, token));
  out.push(await call("ApplyCoupon", "POST", "/api/apply-coupon", { code: "SAVE10", total_amount: 30000000, user_id: login.data?.user?.id }, token));
  out.push(await call("Checkout", "POST", "/api/checkout", { items: [item], total_amount: 30000000, shipping_address: "227 Nguyen Van Cu, Q5, HCMC" }, token));
  out.push(await call("Orders", "GET", "/api/orders/my-orders", null, token));
  return out;
}

async function runBatch(concurrency, iterations) {
  let next = 0;
  async function worker(id) { while (true) { const i = next++; if (i >= iterations) return; await workflow(id, i); } }
  await Promise.all(Array.from({ length: concurrency }, (_, i) => worker(i)));
}

(async () => {
  const started = Date.now();
  if (scenario === "stress") for (const level of profile.levels) await runBatch(level, profile.iterations);
  else if (scenario === "spike") { await runBatch(profile.concurrency, 2); await runBatch(profile.spikeConcurrency, 12); await runBatch(profile.concurrency, 2); }
  else if (scenario === "soak") { const end = Date.now() + profile.duration * 1000; let i = 0; while (Date.now() < end) { await runBatch(profile.concurrency, profile.concurrency); i++; } }
  else await runBatch(profile.concurrency, profile.iterations);
  write();
  const good = rows.filter(r => r[4] === "true").length;
  console.log(JSON.stringify({ scenario, output: out, durationMs: Date.now() - started, samples: rows.length, successful: good, errors: rows.length - good }, null, 2));
})().catch(e => { write(); console.error(e.stack); process.exitCode = 1; });
