import os
import sys
import json
import re
import time
import requests

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def parse_issues_from_report(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by ISSUE #
    sections = re.split(r"### ISSUE #\d+:\s*", content)
    issues = []
    
    for sec in sections[1:]:
        lines = sec.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body_text = "\n".join(lines[1:]).split("\n---\n")[0].strip()
        
        # Remove local markdown image path relative notation if needed or keep standard
        # Body text already has standard Markdown with headers, steps, diffs!
        
        # Determine labels based on category
        labels = ["bug"]
        if "BUG-PERF" in title:
            labels.append("performance")
        if "BUG-SEC" in title:
            labels.append("security")
        if "BUG-LOGIC" in title:
            labels.append("logic")
        if "BUG-CONCUR" in title:
            labels.append("concurrency")
        if "BUG-FUNC" in title:
            labels.append("functional")
            
        issues.append({
            "title": title,
            "body": body_text,
            "labels": labels
        })
        
    return issues

def create_github_issue(token, repo, title, body, labels=None):
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "HW05-Defect-Automation-Agent"
    }
    payload = {
        "title": title,
        "body": body,
        "labels": labels or ["bug"]
    }
    
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=15)
            if r.status_code == 201:
                return r.json()
            else:
                print(f"    [-] HTTP {r.status_code}: {r.text}")
                time.sleep(2)
        except Exception as e:
            print(f"    [-] Request error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return None

def main():
    if len(sys.argv) < 2:
        token = os.environ.get("GITHUB_TOKEN", "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")
    else:
        token = sys.argv[1]
        
    repo = sys.argv[2] if len(sys.argv) >= 3 else "HCMUS-software-testing/HW05"
    
    ws_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    md_path = os.path.join(ws_root, "submissions", "23127205", "report", "bug-report.md")
    
    issues = parse_issues_from_report(md_path)
    print("=" * 70)
    print(f"    POSTING {len(issues)} ISSUES TO GITHUB: https://github.com/{repo}/issues")
    print("=" * 70)
    
    created_issues = []
    for idx, iss in enumerate(issues, 1):
        print(f"\n[*] [{idx:02d}/{len(issues):02d}] Submitting Issue: {iss['title']}")
        res = create_github_issue(token, repo, iss['title'], iss['body'], iss['labels'])
        if res and "html_url" in res:
            print(f"    [+] SUCCESS: #{res['number']} -> {res['html_url']}")
            created_issues.append({
                "number": res['number'],
                "title": iss['title'],
                "url": res['html_url']
            })
        else:
            print(f"    [-] FAILED to create issue: {iss['title']}")
        time.sleep(1)
        
    print("\n" + "=" * 70)
    print(f"    SUMMARY: Successfully created {len(created_issues)}/{len(issues)} GitHub Issues!")
    print("=" * 70)
    
    # Save output log
    log_file = os.path.join(ws_root, "submissions", "23127205", "evidence", "bugs", "github_issues_created.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(created_issues, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved GitHub issues log to: {log_file}")

if __name__ == "__main__":
    main()
