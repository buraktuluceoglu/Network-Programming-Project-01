"""
This script implements a multi-threaded TCP chat client.
It connects to a specified server and allows the user to send
and receive messages concurrently by using two threads:
- The main thread handles user input (sending messages).
- A background thread handles incoming messages from the server.
"""

import socket
import threading

def handle_receive(sock):
    """Thread to continuously listen for messages from the server."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[Client] Server disconnected.")
                break
            print(f"\n[Server]: {data.decode('utf-8', errors='replace')}")
            print("[You]: ", end="", flush=True)
        except:
            break

def start_client(host="127.0.0.1", port=6060):
    """Concurrent chat client (write and receive at the same time)."""
    try:
        with socket.create_connection((host, port)) as s:
            print(f"[Client] Connected to {host}:{port}")
            print("You can type 'exit' or Ctrl+C to quit.")

            t = threading.Thread(target=handle_receive, args=(s,), daemon=True)
            t.start()

            while True:
                msg = input("[You]: ").strip()
                if msg.lower() in ("exit", "quit"):
                    print("[Client] Chat ended.")
                    break
                
                if t.is_alive():
                    s.sendall(msg.encode("utf-8"))
                else:
                    print("[Client] Server is not available. Cannot send message.")
                    break

    except KeyboardInterrupt:
        print("\n[Client] Interrupted by user.")
    except ConnectionRefusedError:
        print(f"[Client] ERROR: Connection refused. Is the server running at {host}:{port}?")
    except Exception as e:
        print(f"[Client] ERROR: {e}")
    finally:
        print("[Client] Connection closed.")

if __name__ == "__main__":
    start_client()