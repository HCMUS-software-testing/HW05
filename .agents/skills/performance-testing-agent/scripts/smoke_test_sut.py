import urllib.request
import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://localhost:3000"

def make_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    
    encoded_data = None
    if data is not None:
        encoded_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.status
            body = resp.read().decode("utf-8")
            try:
                json_data = json.loads(body)
            except Exception:
                json_data = body
            return status_code, json_data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            json_data = json.loads(body)
        except Exception:
            json_data = body
        return e.code, json_data
    except Exception as e:
        return 0, str(e)

def run_smoke_test():
    print("==================================================")
    print("SMOKE TEST FOR MEMBER 1 WORKFLOW APIS")
    print(f"Base URL: {BASE_URL}")
    print("==================================================")
    
    # 1. POST /api/login (Auth-heavy)
    print("\n[Step 1] POST /api/login")
    login_payload = {
        "email": "loadtest_user01@eshop.com",
        "password": "Test1234!"
    }
    status, res = make_request(f"{BASE_URL}/api/login", method="POST", data=login_payload)
    print(f"Status: {status}")
    if status == 200 and "token" in res:
        token = res["token"]
        print(f"[PASS] Login successful. JWT Token obtained: {token[:25]}...")
    else:
        print(f"[FAIL] Login failed: {res}")
        return False
        
    auth_header = {"Authorization": f"Bearer {token}"}
    
    # 2. GET /api/products?search=iPhone (Read-heavy)
    print("\n[Step 2] GET /api/products?search=iPhone")
    status, res = make_request(f"{BASE_URL}/api/products?search=iPhone")
    print(f"Status: {status}")
    if status == 200 and isinstance(res, list) and len(res) > 0:
        print(f"[PASS] Found {len(res)} products matching 'iPhone'. First item: {res[0].get('name')}")
    else:
        print(f"[FAIL] Product search failed: {res}")
        return False
        
    # 3. GET /api/products/1 (Read-heavy)
    print("\n[Step 3] GET /api/products/1")
    status, res = make_request(f"{BASE_URL}/api/products/1")
    print(f"Status: {status}")
    if status == 200 and res.get("id") == 1:
        print(f"[PASS] Product details retrieved: {res.get('name')} - Price: {res.get('price')}")
    else:
        print(f"[FAIL] Product detail failed: {res}")
        return False
        
    # 4. POST /api/cart (Transactional)
    print("\n[Step 4] POST /api/cart")
    cart_payload = {
        "id": 1,
        "name": "iPhone 15 Pro Max",
        "price": 30000000,
        "quantity": 1
    }
    status, res = make_request(f"{BASE_URL}/api/cart", method="POST", headers=auth_header, data=cart_payload)
    print(f"Status: {status}")
    if status == 200 and res.get("message") == "Added to cart":
        print(f"[PASS] Item added to cart successfully.")
    else:
        print(f"[FAIL] Add to cart failed: {res}")
        return False
        
    # 5. POST /api/checkout (Transactional)
    print("\n[Step 5] POST /api/checkout")
    checkout_payload = {
        "total_amount": 30000000,
        "shipping_address": "227 Nguyen Van Cu, Quan 5, TP.HCM"
    }
    status, res = make_request(f"{BASE_URL}/api/checkout", method="POST", headers=auth_header, data=checkout_payload)
    print(f"Status: {status}")
    if status == 200 and "orderId" in res:
        print(f"[PASS] Checkout successful. Created Order ID: {res.get('orderId')}")
    else:
        print(f"[FAIL] Checkout failed: {res}")
        return False
        
    print("\n==================================================")
    print("[ALL PASSED] All 5 API Endpoints in Workflow are fully verified!")
    print("==================================================")
    return True

if __name__ == "__main__":
    run_smoke_test()
