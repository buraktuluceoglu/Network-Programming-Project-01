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

def handle_receive(conn):
    """Thread to continuously listen for messages from the client."""
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("\n[Server] Client disconnected.")
                break
            print(f"\n[Client]: {data.decode('utf-8', errors='replace')}")
            print("[You]: ", end="", flush=True)
        except:
            break

def start_server(host="0.0.0.0", port=6060):
    """Simple concurrent chat server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((host, port))
            srv.listen(1)
            print(f"[Server] Listening on {host}:{port}")
            print("[Server] Waiting for a connection...")

            conn, addr = srv.accept()
            print(f"[Server] Connected by {addr}")
            
            with conn:
                t = threading.Thread(target=handle_receive, args=(conn,), daemon=True)
                t.start()

                while True:
                    msg = input("[You]: ").strip()
                    if msg.lower() in ("exit", "quit"):
                        print("[Server] Chat ended.")
                        break
                    
                    if t.is_alive():
                        conn.sendall(msg.encode("utf-8"))
                    else:
                        print("[Server] Client is not connected. Cannot send message.")
                        break

    except KeyboardInterrupt:
        print("\n[Server] Interrupted by user.")
    except Exception as e:
        print(f"[Server] ERROR: {e}")
    finally:
        print("[Server] Connection closed.")

if __name__ == "__main__":
    start_server()