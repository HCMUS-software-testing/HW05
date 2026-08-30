import os
import sys
import json
import time
import requests

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

UPDATES = {
    1: "[BUG-PERF-01] Rò rỉ bộ nhớ RAM do không giải phóng mảng giỏ hàng userCarts sau khi Checkout",
    2: "[BUG-PERF-02] Bất đối xứng độ trễ và nghẽn khóa độc quyền tệp SQLite khi Checkout đồng thời",
    3: "[BUG-PERF-03] Chạm trần Throughput do Event Loop Node.js đơn luồng không tận dụng đa nhân CPU",
    4: "[BUG-CONCUR-04] Khóa tài khoản oan chỉ sau 2 lần sai do bước tăng login_attempts + 2",
    5: "[BUG-FUNC-05] Sai lệch kiểu dữ liệu giá sản phẩm (Sản phẩm ID chẵn bị ép sang kiểu String)",
    6: "[BUG-SEC-06] Lỗ hổng SQL Injection tại ô tìm kiếm và phản hồi lỗi dạng HTML thay vì JSON",
    7: "[BUG-LOGIC-07] Lỗi máy trạng thái đơn hàng: Cho phép chuyển từ trạng thái Canceled sang Delivered",
    8: "[BUG-FUNC-08] Lỗi công thức tính tiền giảm giá Coupon phần trăm làm số tiền bị âm và đội giá x10",
    9: "[BUG-LOGIC-09] Điều kiện bất đẳng thức ngặt (>) từ chối Coupon có đơn hàng bằng đúng mức tối thiểu",
    10: "[BUG-SEC-10] Lỗ hổng leo thang đặc quyền Admin qua API cập nhật hồ sơ cá nhân /api/users/me",
    11: "[BUG-LOGIC-11] Cho phép người dùng hủy đơn hàng khi đơn đã ở trạng thái Đang giao hàng (Shipping)"
}

def update_issue_title(token, repo, issue_num, new_title):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "HW05-Defect-Automation-Agent"
    }
    payload = {"title": new_title}
    
    for attempt in range(3):
        try:
            r = requests.patch(url, json=payload, headers=headers, timeout=15)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"    [-] HTTP {r.status_code}: {r.text}")
                time.sleep(2)
        except Exception as e:
            print(f"    [-] Error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return None

def main():
    token = sys.argv[1] if len(sys.argv) >= 2 else "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"
    repo = sys.argv[2] if len(sys.argv) >= 3 else "HCMUS-software-testing/HW05"
    
    print("=" * 70)
    print(f"    UPDATING 11 GITHUB ISSUES TO VIETNAMESE TITLES: https://github.com/{repo}/issues")
    print("=" * 70)
    
    updated = 0
    for num, vi_title in UPDATES.items():
        print(f"\n[*] Updating Issue #{num:02d}...")
        res = update_issue_title(token, repo, num, vi_title)
        if res and "html_url" in res:
            print(f"    [+] Updated #{num}: {res['title']}")
            print(f"    [+] URL: {res['html_url']}")
            updated += 1
        else:
            print(f"    [-] Failed to update #{num}")
        time.sleep(1)
        
    print("\n" + "=" * 70)
    print(f"    COMPLETED: Updated {updated}/{len(UPDATES)} GitHub Issue Titles to Vietnamese!")
    print("=" * 70)

if __name__ == "__main__":
    main()
