import os
import sys
import urllib.request
import zipfile
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def download_file(url, target_path):
    print(f"[*] Downloading: {url}")
    print(f"[*] Saving to: {target_path}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(target_path, 'wb') as out_file:
        total_size = response.length
        downloaded = 0
        chunk_size = 1024 * 1024  # 1MB chunks
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size:
                percent = (downloaded / total_size) * 100
                print(f"\r    -> {downloaded / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB ({percent:.1f}%)", end="", flush=True)
            else:
                print(f"\r    -> {downloaded / (1024*1024):.2f} MB", end="", flush=True)
    print(f"\n[+] Download finished: {os.path.getsize(target_path)} bytes")

def setup_jmeter():
    ws_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    tools_dir = os.path.join(ws_root, "tools")
    os.makedirs(tools_dir, exist_ok=True)
    
    jmeter_home = os.path.join(tools_dir, "apache-jmeter-5.6.3")
    jmeter_zip = os.path.join(tools_dir, "apache-jmeter-5.6.3.zip")
    
    # 1. Download & Extract JMeter
    if not os.path.exists(jmeter_home):
        if not os.path.exists(jmeter_zip) or os.path.getsize(jmeter_zip) < 80000000:
            jmeter_url = "https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-5.6.3.zip"
            download_file(jmeter_url, jmeter_zip)
            
        print(f"[*] Extracting {jmeter_zip} into {tools_dir}...")
        with zipfile.ZipFile(jmeter_zip, 'r') as zip_ref:
            zip_ref.extractall(tools_dir)
        print(f"[+] JMeter extracted to {jmeter_home}")
    else:
        print(f"[+] JMeter already exists at {jmeter_home}")
        
    lib_ext_dir = os.path.join(jmeter_home, "lib", "ext")
    lib_dir = os.path.join(jmeter_home, "lib")
    os.makedirs(lib_ext_dir, exist_ok=True)
    os.makedirs(lib_dir, exist_ok=True)
    
    # 2. Download Plugins
    plugins = [
        ("https://repo1.maven.org/maven2/kg/apc/jmeter-plugins-manager/1.10/jmeter-plugins-manager-1.10.jar", lib_ext_dir, "jmeter-plugins-manager-1.10.jar"),
        ("https://repo1.maven.org/maven2/kg/apc/cmdrunner/2.3/cmdrunner-2.3.jar", lib_dir, "cmdrunner-2.3.jar"),
        ("https://repo1.maven.org/maven2/kg/apc/jmeter-plugins-cmn-jmeter/0.7/jmeter-plugins-cmn-jmeter-0.7.jar", lib_ext_dir, "jmeter-plugins-cmn-jmeter-0.7.jar"),
        ("https://repo1.maven.org/maven2/kg/apc/jmeter-plugins-casutg/2.10/jmeter-plugins-casutg-2.10.jar", lib_ext_dir, "jmeter-plugins-casutg-2.10.jar"),
    ]
    
    for url, dest_dir, fname in plugins:
        target = os.path.join(dest_dir, fname)
        if not os.path.exists(target) or os.path.getsize(target) == 0:
            download_file(url, target)
        else:
            print(f"[+] Plugin {fname} already installed.")
            
    # 3. Configure JVM Heap in jmeter.bat
    jmeter_bat = os.path.join(jmeter_home, "bin", "jmeter.bat")
    if os.path.exists(jmeter_bat):
        with open(jmeter_bat, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "set HEAP=-Xms1g -Xmx4g" not in content:
            heap_config = "\nrem Custom JVM Heap for HW05\nset HEAP=-Xms1g -Xmx4g\n"
            content = content.replace("setlocal", "setlocal" + heap_config, 1)
            with open(jmeter_bat, "w", encoding="utf-8") as f:
                f.write(content)
            print("[+] Configured JVM Heap (HEAP=-Xms1g -Xmx4g) in jmeter.bat")
        else:
            print("[+] JVM Heap already configured in jmeter.bat")
            
    print("\n[SUCCESS] Apache JMeter 5.6.3 with Plugins and JVM Heap is READY!")

if __name__ == "__main__":
    setup_jmeter()
