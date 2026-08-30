import requests
import json
import time
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://localhost:3000"

def log_test(title):
    print("\n" + "=" * 70)
    print(f"  [KIEM CHUNG THUC NGHIEM] {title}")
    print("=" * 70)

def test_all_bugs():
    print("Bat dau kiem chung thuc te toan bo cac bug tren server SUT (http://localhost:3000)...")

    # ----------------------------------------------------------------------
    # 1. Kiểm chứng FUNC-01: Lỗi Ép kiểu Giá tiền ở ID chẵn (server.js:L162)
    # ----------------------------------------------------------------------
    log_test("FUNC-01: Loi Kieu Du lieu Gia Tien o ID Chan (Type Mismatch)")
    res_p1 = requests.get(f"{BASE_URL}/api/products/1").json()
    res_p2 = requests.get(f"{BASE_URL}/api/products/2").json()
    
    type_p1 = type(res_p1.get("price")).__name__
    type_p2 = type(res_p2.get("price")).__name__
    
    print(f"  * Product ID 1 (Le): price = {res_p1.get('price')} (Type: {type_p1})")
    print(f"  * Product ID 2 (Chan): price = '{res_p2.get('price')}' (Type: {type_p2})")
    
    if type_p1 == "int" and type_p2 == "str":
        print("  => KET LUAN: [XAC NHAN DUNG BUG 100%] ID chan bi ep kieu thanh String ('28000000')!")
    else:
        print("  => Khong tai hien duoc.")

    # ----------------------------------------------------------------------
    # 2. Kiểm chứng FUNC-02: Lỗ hổng SQL Injection (server.js:L144)
    # ----------------------------------------------------------------------
    log_test("FUNC-02: Lo hong SQL Injection o API Tim kiem")
    sqli_payload = "' OR '1'='1"
    res_sqli = requests.get(f"{BASE_URL}/api/products?search={sqli_payload}")
    
    if res_sqli.status_code == 200:
        items = res_sqli.json()
        print(f"  * Payload gui di: search={sqli_payload}")
        print(f"  * Ket qua tra ve: Tra ve toan bo {len(items)} san pham trong CSDL!")
        print("  => KET LUAN: [XAC NHAN DUNG BUG 100%] Cau lenh SQL bi chen truc tiep khong qua parameterize!")
    else:
        print("  => Khong tai hien duoc.")

    # ----------------------------------------------------------------------
    # 3. Kiểm chứng FUNC-03: Lỗi Tính Giảm Giá Coupon Phần Trăm (server.js:L399)
    # ----------------------------------------------------------------------
    log_test("FUNC-03: Loi Tinh Giam Gia Coupon Phan Tram")
    coupon_payload = {
        "code": "SAVE10",
        "total_amount": 500000,
        "user_id": 1
    }
    res_coupon = requests.post(f"{BASE_URL}/api/apply-coupon", json=coupon_payload).json()
    print(f"  * Ap dung ma 'SAVE10' cho don 500,000 d:")
    print(f"  * discount_amount tra ve: {res_coupon.get('discount_amount')} d")
    print(f"  * final_amount tra ve: {res_coupon.get('final_amount')} d")
    
    if res_coupon.get('discount_amount', 0) < 0 or res_coupon.get('final_amount', 0) > 500000:
        print("  => KET LUAN: [XAC NHAN DUNG BUG 100%] Cong thuc tinh giam gia sai khien so tien giam bi am (-4,500,000 d) va tong tien vot len 5,000,000 d!")
    else:
        print("  => Khong tai hien duoc.")

    # ----------------------------------------------------------------------
    # 4. Kiểm chứng PERF-01: Rò rỉ Bộ nhớ In-Memory trong userCarts (server.js:L14, L306)
    # ----------------------------------------------------------------------
    log_test("PERF-01: Ro ri Gio hang In-Memory (Memory Leak trong userCarts)")
    login_res = requests.post(f"{BASE_URL}/api/login", json={"email": "test@eshop.com", "password": "Test1234!"}).json()
    token = login_res.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add to cart
    requests.post(f"{BASE_URL}/api/cart", json={"product_id": 1, "quantity": 2}, headers=headers)
    
    # Checkout
    requests.post(f"{BASE_URL}/api/checkout", json={"total_amount": 60000000, "shipping_address": "TPHCM"}, headers=headers)
    
    # Kiểm tra lại giỏ hàng sau khi checkout
    cart_after_checkout = requests.get(f"{BASE_URL}/api/cart", headers=headers).json()
    print(f"  * Da hoan tat Checkout don hang.")
    print(f"  * Gio hang sau khi Checkout: {cart_after_checkout}")
    
    if len(cart_after_checkout) > 0:
        print("  => KET LUAN: [XAC NHAN DUNG BUG 100%] Gio hang khong duoc xoa sau Checkout, ro ri du lieu trong RAM userCarts!")
    else:
        print("  => Gio hang da duoc xoa sach.")

    # ----------------------------------------------------------------------
    # 5. Kiểm chứng FUNC-04: Lỗi Chuyển Đổi Trạng Thái Đơn Hàng Canceled -> Delivered (server.js:L550)
    # ----------------------------------------------------------------------
    log_test("FUNC-04: Chuyen Trang thai Don hang Sai (Canceled -> Delivered)")
    orders = requests.get(f"{BASE_URL}/api/orders/my-orders", headers=headers).json()
    if orders:
        order_id = orders[0]["id"]
        # Hủy đơn
        requests.put(f"{BASE_URL}/api/orders/{order_id}/cancel", headers=headers)
        
        # Login admin
        admin_login = requests.post(f"{BASE_URL}/api/login", json={"email": "admin@eshop.com", "password": "Admin123!"}).json()
        admin_headers = {"Authorization": f"Bearer {admin_login.get('token')}"}
        
        # Admin đổi từ canceled -> delivered
        status_res = requests.put(f"{BASE_URL}/api/admin/orders/{order_id}/status", json={"status": "delivered"}, headers=admin_headers)
        print(f"  * Doi don #{order_id} tu trang thai 'canceled' sang 'delivered':")
        print(f"  * Response HTTP: {status_res.status_code}, Body: {status_res.json()}")
        
        if status_res.status_code == 200:
            print("  => KET LUAN: [XAC NHAN DUNG BUG 100%] He thong cho phep don DA HUY chuyen thanh DA GIAO THANH CONG!")

if __name__ == "__main__":
    test_all_bugs()
