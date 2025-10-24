"""
    This script implements a multi-threaded TCP chat server.
It listens on a specified port, accepts a single client connection,
and then allows the server operator to send and receive messages
concurrently by using two threads:
- The main thread handles user input (sending messages).
- A background thread handles incoming messages from the client.
"""
import socket
import threading
from datetime import datetime

CHAT_LOG_FILE = "chat_history.log" 

def log_message(message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    print(log_entry)
    
    try:
        with open(CHAT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except IOError as e:
        print(f"!!! CRITICAL: Failed to write to log file {CHAT_LOG_FILE}: {e} !!!")

def handle_receive(conn, addr): 
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                log_message(f"[Server] Client {addr} disconnected.")
                break
            
            log_message(f"[Client {addr}]: {data.decode('utf-8', errors='replace')}")
            
            print("[You]: ", end="", flush=True)
            
        except: 
            log_message(f"[Server] Receive thread for {addr} stopping due to error.")
            break

def start_server(host="0.0.0.0", port=6060):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((host, port))
            srv.listen(1)
            
            log_message(f"[Server] Listening on {host}:{port}")
            log_message("[Server] Waiting for a connection...")

            conn, addr = srv.accept()
            log_message(f"[Server] Connected by {addr}")
            
            with conn:
                t = threading.Thread(target=handle_receive, args=(conn, addr), daemon=True)
                t.start()

                while True:
                    msg = input("[You]: ").strip()
                    if msg.lower() in ("exit", "quit"):
                        log_message("[Server] Chat ended by user.")
                        break
                    
                    if t.is_alive():
                        conn.sendall(msg.encode("utf-8"))
                        log_message(f"[Server (You)]: {msg}")
                    else:
                        log_message("[Server] Client is not connected. Cannot send message.")
                        break

    except KeyboardInterrupt:
        log_message("\n[Server] Interrupted by user.")
    except Exception as e:
        log_message(f"[Server] ERROR: {e}")
    finally:
        log_message("[Server] Connection closed.")

if __name__ == "__main__":
    start_server()
