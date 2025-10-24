""" 
    This code starts an echo server on the specified host 
    IP and port. It uses a TCP connection to do this. It 
    ensures that the port becomes available again after
    the server is shut down. Once the TCP connection is 
    established with the client, we can test it by sending an
    echo message.

"""

import socket

def start_echo_server(host="0.0.0.0", port=5050):
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"[Echo Server] Listening on {host}:{port} ...")

        conn, addr = server.accept()
        print(f"[Echo Server] Connected by {addr}")

        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    print("[Echo Server] Client disconnected.")
                    break
                print(f"[Echo Server] Received: {data.decode('utf-8')}")
                conn.sendall(data) 
                print("[Echo Server] Echoed the message back.")


if __name__ == "__main__":
    start_echo_server()