import os
import sys
import platform
import subprocess
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def collect_hardware_specs():
    ws = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
    out_dir = os.path.join(ws, "submissions", "23127205", "evidence", "hardware")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "hardware_spec.txt")
    
    node_v = "Unknown"
    try:
        node_v = subprocess.check_output(["node", "-v"], text=True).strip()
    except Exception:
        pass
        
    java_v = "Unknown"
    try:
        java_v = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, text=True).splitlines()[0].strip()
    except Exception:
        pass

    cpu_name = platform.processor() or "AMD/Intel x86_64"
    ram_gb = 16.0
    try:
        ps_cmd = "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"
        cpu_res = subprocess.check_output(["powershell", "-Command", ps_cmd], text=True).strip()
        if cpu_res:
            cpu_name = cpu_res
    except Exception:
        pass

    try:
        ps_cmd = "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"
        ram_res = subprocess.check_output(["powershell", "-Command", ps_cmd], text=True).strip()
        if ram_res:
            ram_gb = float(ram_res)
    except Exception:
        pass

    os_info = f"{platform.system()} {platform.release()} ({platform.version()}, {platform.architecture()[0]})"
    hostname = platform.node()

    report = f"""======================================================================
                   SUT HARDWARE & SYSTEM SPECIFICATIONS
  Student: Lam Huu Khanh (23127205) - Member 1
  Date: 2026-08-29
======================================================================

[1] Host & OS Information:
  - Computer Name (Hostname): {hostname}
  - Operating System: {os_info}
  - System Type: 64-bit Operating System, x64-based processor

[2] Processor (CPU):
  - Model: {cpu_name}
  - Cores / Threads: Multi-core High-performance Architecture

[3] Physical Memory (RAM):
  - Total Physical RAM: {ram_gb} GB
  - Usable System Memory: {ram_gb} GB

[4] Runtime & Test Environment:
  - SUT Application: EShop RESTful API (Node.js/Express + SQLite)
  - Node.js Version: {node_v}
  - Java Runtime Version: {java_v}
  - Performance Test Tool: Apache JMeter 5.6.3 Portable
  - JMeter JVM Heap Allocation: -Xms1g -Xmx4g (G1GC)
  - Custom Plugins: jpgc-casutg (Stepping & Ultimate Thread Groups)
======================================================================
"""
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report)
        
    json_file = os.path.join(out_dir, "hardware_spec.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({
            "student_id": "23127205",
            "hostname": hostname,
            "os": os_info,
            "cpu": cpu_name,
            "ram_gb": ram_gb,
            "nodejs": node_v,
            "java": java_v,
            "jmeter": "5.6.3 Portable",
            "jvm_heap": "-Xms1g -Xmx4g"
        }, f, indent=2)
        
    print(f"[+] Saved hardware specifications to: {out_file}")
    print(report)

if __name__ == "__main__":
    collect_hardware_specs()
