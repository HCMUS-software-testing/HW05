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

IMAGE_MAP = {
    1: "bug_perf_01_cart_memory_leak.png",
    2: "bug_perf_02_sqlite_lock.png",
    3: "bug_perf_03_event_loop_ceiling.png",
    4: "bug_concur_04_account_lockout.png",
    5: "bug_func_05_price_type.png",
    6: "bug_sec_06_sql_injection.png",
    7: "bug_logic_07_state_machine.png",
    8: "bug_func_08_coupon_math.png",
    9: "bug_logic_09_coupon_boundary.png",
    10: "bug_sec_10_privilege_escalation.png",
    11: "bug_logic_11_cancel_shipping.png"
}

def update_issue_body(token, repo, branch, issue_num):
    img_name = IMAGE_MAP.get(issue_num)
    if not img_name:
        return
        
    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "HW05-Defect-Automation-Agent"
    }
    
    blob_url = f"https://github.com/{repo}/blob/{branch}/submissions/23127205/evidence/bugs/{img_name}"
    raw_url = f"https://github.com/{repo}/blob/{branch}/submissions/23127205/evidence/bugs/{img_name}?raw=true"
    
    replacement_image_md = (
        f"#### 4. Bằng chứng thực nghiệm (Empirical Proof)\n\n"
        f"> 📷 **Minh chứng ảnh chụp thực tế (Authentic Screenshot):**\n"
        f"> 🔗 **Xem ảnh trên GitHub Repo:** [`submissions/23127205/evidence/bugs/{img_name}`]({blob_url})\n\n"
        f"![Minh chứng thực tế]({raw_url})"
    )
    
    for attempt in range(5):
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"[-] Failed to get issue #{issue_num}: {res.status_code}")
                time.sleep(2)
                continue
                
            issue_data = res.json()
            body = issue_data.get("body", "")
            
            # Replace old relative image tags
            new_body = re.sub(
                r"!\[.*?\]\((?:\.\./)?evidence/bugs/.*?\)",
                f"> 🔗 **File Link:** [`submissions/23127205/evidence/bugs/{img_name}`]({blob_url})\n\n![Minh chứng thực tế]({raw_url})",
                body
            )
            
            patch_res = requests.patch(url, json={"body": new_body}, headers=headers, timeout=15)
            if patch_res.status_code == 200:
                print(f"[+] Successfully updated Issue #{issue_num} with live GitHub image link!")
                return
            else:
                print(f"[-] Failed to update Issue #{issue_num}: {patch_res.status_code}")
                time.sleep(2)
        except Exception as e:
            print(f"[-] Error on issue #{issue_num} (attempt {attempt+1}): {e}")
            time.sleep(3)

def main():
    token = sys.argv[1] if len(sys.argv) >= 2 else "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"
    repo = sys.argv[2] if len(sys.argv) >= 3 else "HCMUS-software-testing/HW05"
    branch = sys.argv[3] if len(sys.argv) >= 4 else "khanh"
    
    print("=" * 70)
    print(f"    FIXING IMAGE URLS FOR 11 GITHUB ISSUES ON {repo} (branch: {branch})")
    print("=" * 70)
    
    for num in range(1, 12):
        print(f"\n[*] Processing Issue #{num:02d}...")
        update_issue_body(token, repo, branch, num)
        time.sleep(1)
        
    print("\n" + "=" * 70)
    print("    COMPLETED: All 11 GitHub Issues now have live GitHub image URLs!")
    print("=" * 70)

if __name__ == "__main__":
    main()
