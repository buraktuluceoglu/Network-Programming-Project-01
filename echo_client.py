"""
    This code connects to the echo server running
    on the specified IP and port. We can send any 
    echo message we want to this server. The sent 
    and received messages are compared to determine 
    whether the connection is successful or unsuccessful.
      
"""

import socket

def start_echo_client(host="127.0.0.1", port=5050, message="Hello World"):
    
    with socket.create_connection((host, port)) as client:
        print(f"[Echo Client] Connected to {host}:{port}")
        client.sendall(message.encode("utf-8"))
        print(f"[Echo Client] Sent: {message}")

        data = client.recv(1024)
        received = data.decode("utf-8")
        print(f"[Echo Client] Received: {received}")

        if received == message:
            print("Connection successful, data matches")
        else:
            print("Connection failed, data mismatch")


if __name__ == "__main__":
    start_echo_client()