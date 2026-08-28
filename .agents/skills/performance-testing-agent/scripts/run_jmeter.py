import os
import sys
import subprocess
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

def run_jmeter(args=None):
    if args is None:
        args = sys.argv[1:]
        
    ws_root = get_workspace_root()
    jmeter_bin = os.path.join(ws_root, "tools", "apache-jmeter-5.6.3", "bin")
    
    if not os.path.exists(jmeter_bin):
        print(f"[-] JMeter bin directory not found at {jmeter_bin}")
        sys.exit(1)
        
    # Auto-clean target .jtl and html-report folder to prevent JMeter "not empty" errors
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "-l" and i + 1 < len(args):
            jtl_file = args[i + 1]
            abs_jtl = jtl_file if os.path.isabs(jtl_file) else os.path.abspath(jtl_file)
            if os.path.exists(abs_jtl):
                try:
                    os.remove(abs_jtl)
                    print(f"[*] Auto-cleaned existing results log: {abs_jtl}")
                except Exception as e:
                    print(f"[!] Warning cleaning JTL: {e}")
        elif arg == "-o" and i + 1 < len(args):
            report_dir = args[i + 1]
            abs_report = report_dir if os.path.isabs(report_dir) else os.path.abspath(report_dir)
            if os.path.exists(abs_report):
                try:
                    shutil.rmtree(abs_report)
                    print(f"[*] Auto-cleaned existing HTML report folder: {abs_report}")
                except Exception as e:
                    print(f"[!] Warning cleaning HTML report folder: {e}")
        i += 1

    # Convert path arguments (-t, -l, -o, -g) into relative paths FROM jmeter_bin
    # This completely eliminates Unicode / accented characters from the JVM CLI arguments!
    processed_args = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ["-t", "-l", "-o", "-g"] and i + 1 < len(args):
            val = args[i + 1]
            abs_val = val if os.path.isabs(val) else os.path.abspath(val)
            try:
                rel_val = os.path.relpath(abs_val, jmeter_bin)
                processed_args.extend([arg, rel_val])
            except ValueError:
                processed_args.extend([arg, abs_val])
            i += 2
        else:
            processed_args.append(arg)
            i += 1
            
    java_cmd = [
        "java",
        "-Dfile.encoding=UTF-8",
        "-Dsun.jnu.encoding=UTF-8",
        "-Xms1g",
        "-Xmx4g",
        "-XX:+UseG1GC",
        "-XX:MaxGCPauseMillis=100",
        "-XX:G1ReservePercent=20",
        "-Duser.language=en",
        "-Duser.region=EN",
        "--add-opens", "java.desktop/sun.awt=ALL-UNNAMED",
        "--add-opens", "java.desktop/sun.swing=ALL-UNNAMED",
        "--add-opens", "java.desktop/javax.swing.text.html=ALL-UNNAMED",
        "--add-opens", "java.desktop/java.awt=ALL-UNNAMED",
        "--add-opens", "java.desktop/java.awt.font=ALL-UNNAMED",
        "--add-opens=java.base/java.lang=ALL-UNNAMED",
        "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED",
        "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED",
        "--add-opens=java.base/java.util=ALL-UNNAMED",
        "--add-opens=java.base/java.text=ALL-UNNAMED",
        "--add-opens=java.desktop/sun.awt.shell=ALL-UNNAMED",
        "-jar", "ApacheJMeter.jar"
    ] + processed_args
    
    print(f"[*] Executing JMeter with JVM Heap (-Xms1g -Xmx4g)...")
    print(f"[*] Command args: {' '.join(processed_args)}")
    
    process = subprocess.Popen(
        java_cmd,
        cwd=jmeter_bin,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    for line in process.stdout:
        print(line, end="")
        
    process.wait()
    return process.returncode

if __name__ == "__main__":
    code = run_jmeter()
    sys.exit(code)
