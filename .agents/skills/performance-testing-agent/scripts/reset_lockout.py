import sqlite3
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

def reset_lockout():
    ws_root = get_workspace_root()
    backend_dir = os.path.join(ws_root, "eshop-sut", "backend")
    db_path = os.path.join(backend_dir, "database.sqlite")
    
    if not os.path.exists(db_path):
        print(f"[-] Database not found at {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET login_attempts = 0, locked_until = NULL")
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"[+] Successfully reset login_attempts and locked_until for {affected} users in SQLite.")

if __name__ == "__main__":
    reset_lockout()
