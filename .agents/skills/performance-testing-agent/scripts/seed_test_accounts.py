import sqlite3
import os
import sys
import csv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

def seed_accounts(num_accounts=50):
    ws_root = get_workspace_root()
    backend_dir = os.path.join(ws_root, "eshop-sut", "backend")
    db_path = os.path.join(backend_dir, "database.sqlite")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}. Please run `node database.js` first.")
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    accounts = []
    print(f"[*] Seeding {num_accounts} test accounts...")
    
    for i in range(1, num_accounts + 1):
        email = f"loadtest_user{i:02d}@eshop.com"
        name = f"LoadTest User {i:02d}"
        password = "Test1234!"
        role = "user"
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            cursor.execute(
                "INSERT INTO users (name, email, password, role, login_attempts, locked_until) VALUES (?, ?, ?, ?, 0, NULL)",
                (name, email, password, role)
            )
        else:
            cursor.execute(
                "UPDATE users SET login_attempts = 0, locked_until = NULL, password = ? WHERE email = ?",
                (password, email)
            )
        accounts.append((email, password))
        
    conn.commit()
    conn.close()
    print(f"[+] Successfully seeded {len(accounts)} accounts into database.")
    
    # Export to submissions/23127205/data/credentials.csv
    data_dir = os.path.join(ws_root, "submissions", "23127205", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, "credentials.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "password"])
        for email, password in accounts:
            writer.writerow([email, password])
            
    print(f"[+] Exported credentials CSV to: {csv_path}")
    
def seed_datasets():
    ws_root = get_workspace_root()
    data_dir = os.path.join(ws_root, "submissions", "23127205", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Products CSV (search_term, product_id, product_name, price)
    products_csv = os.path.join(data_dir, "products.csv")
    products = [
        ("iPhone", 1, "iPhone 15 Pro Max", 30000000),
        ("Samsung", 2, "Samsung Galaxy S24 Ultra", 28000000),
        ("MacBook", 3, "MacBook Pro M3", 45000000),
        ("AirPods", 4, "Tai nghe AirPods Pro 2", 6000000),
        ("Keychron", 5, "Bàn phím cơ Keychron Q1", 4000000),
    ]
    with open(products_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["search_term", "product_id", "product_name", "price"])
        for p in products:
            writer.writerow(p)
    print(f"[+] Exported products CSV to: {products_csv}")
    
    # Orders CSV (shipping_address, total_amount)
    orders_csv = os.path.join(data_dir, "orders.csv")
    orders = [
        ("227 Nguyen Van Cu, Quan 5, TP.HCM", 30000000),
        ("123 Le Loi, Quan 1, TP.HCM", 28000000),
        ("456 Vo Van Kiet, Quan 1, TP.HCM", 45000000),
        ("789 Dien Bien Phu, Binh Thanh, TP.HCM", 6000000),
        ("101 Tran Hung Dao, Quan 5, TP.HCM", 4000000),
    ]
    with open(orders_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["shipping_address", "total_amount"])
        for o in orders:
            writer.writerow(o)
    print(f"[+] Exported orders CSV to: {orders_csv}")

if __name__ == "__main__":
    seed_accounts(50)
    seed_datasets()
