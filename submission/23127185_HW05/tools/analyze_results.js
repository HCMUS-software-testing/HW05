#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
function parse(file) {
  const raw = fs.readFileSync(file, "utf8").trim().split(/\r?\n/);
  const hasHeader = raw[0].startsWith("timeStamp,");
  const header = hasHeader ? raw.shift().split(",") : ["timeStamp", "elapsed", "label", "responseCode", "responseMessage", "threadName", "dataType", "success", "failureMessage", "bytes", "sentBytes", "grpThreads", "allThreads", "URL", "Latency", "IdleTime", "Connect"];
  const index = name => header.indexOf(name);
  const lines = raw;
  const values = lines.map(line => { const p = line.split(/","|,(?=[^\"]*(?:\"|$))/).map(x => x.replace(/^"|"$/g, "")); const successAt = index("success"); return { elapsed: Number(p[index("elapsed")]), success: p[successAt] === "true", label: p[index("label")], error: p[index("failureMessage")] || p[index("failureMessage")] }; });
  const sorted = values.map(x => x.elapsed).sort((a,b) => a-b);
  const pct = p => sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * p))] || 0;
  const errors = values.filter(x => !x.success);
  return { samples: values.length, errors: errors.length, errorRate: values.length ? +(errors.length / values.length * 100).toFixed(2) : 0, averageMs: values.length ? +(values.reduce((a,x)=>a+x.elapsed,0)/values.length).toFixed(2) : 0, medianMs: pct(.5), p90Ms: pct(.9), p95Ms: pct(.95), p99Ms: pct(.99), byLabel: Object.fromEntries([...new Set(values.map(x=>x.label))].map(label=>[label,{samples:values.filter(x=>x.label===label).length,errors:values.filter(x=>x.label===label&&!x.success).length}])) };
}
const resultsRoot = path.join(root, "jmeter", "results");
const dirs = fs.readdirSync(resultsRoot, { withFileTypes: true }).filter(x=>x.isDirectory());
const result = {};
for (const d of dirs) { const files=fs.readdirSync(path.join(resultsRoot,d.name)).filter(x=>x.endsWith(".jtl")); if(files.length) result[d.name]=parse(path.join(resultsRoot,d.name,files.sort().at(-1))); }
fs.mkdirSync(path.join(root,"report"),{recursive:true});
fs.writeFileSync(path.join(root,"report","metrics.json"), JSON.stringify(result,null,2)+"\n");
let md="# Performance Metrics\n\n| Scenario | Samples | Errors | Error rate | Average ms | Median ms | P95 ms | P99 ms |\n|---|---:|---:|---:|---:|---:|---:|---:|\n";
for(const [s,r] of Object.entries(result)) md+=`| ${s} | ${r.samples} | ${r.errors} | ${r.errorRate}% | ${r.averageMs} | ${r.medianMs} | ${r.p95Ms} | ${r.p99Ms} |\n`;
fs.writeFileSync(path.join(root,"report","metrics.md"),md);
console.log(md);
