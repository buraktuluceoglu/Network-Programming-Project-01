"""
This script serves as the main entry point for the Network Programming 
Project. It integrates all the separate modules:
A. Machine Information
B. Echo
C. SNTP Time Check
D. Simple Chat
E. Settings & Error Management

It presents an interactive command-line menu to the user, allowing
them to select and run any of the implemented modules. It also
handles basic logging for key actions to a 'logs/main.log' file.
"""

from datetime import datetime
from pathlib import Path

# Module Imports
from machine_info import print_machine_info
from echo_server import start_echo_server
from echo_client import start_echo_client
from sntp_client import get_sntp_time
from settings import demo_socket_settings
from simple_chat_server import start_server as start_chat_server
from simple_chat_client import start_client as start_chat_client

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_line(msg: str):
    """Logs a message to both the console and the main.log file."""
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG_DIR / "main.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")

def menu():
    """Displays the main menu and returns the user's choice."""
    print("""
======================================
    Network Programming - Project 01
======================================
1) Machine Information
2) Echo
3) SNTP Time Check
4) Socket Settings / Error Management
5) Simple Chat
0) Exit
""")
    return input("Your choice: ").strip()

def run_machine_info():
    """Executes Module A: Machine Information."""
    print("\n--- 1. Machine Information ---")
    print_machine_info()
    log_line("[OK] Machine Information executed.")

def run_echo():
    """Executes Module B: Echo Test (Server or Client)."""
    print("\n--- 2. Echo Test ---")
    mode = input("Run as server or client? (s/c): ").strip().lower()
    port = int(input("Port [5050]: ") or 5050)

    if mode == "s":
        host = input("Bind Host [0.0.0.0]: ").strip() or "0.0.0.0"
        log_line(f"[Echo] Server starting on {host}:{port}")
        print("Server starting... (You can stop it with Ctrl+C)\n")
        start_echo_server(host, port)
    else:
        host = input("Server IP [127.0.0.1]: ").strip() or "127.0.0.1"
        message = input("Message [Hello World]: ").strip() or "Hello World"
        log_line(f"[Echo] Client -> {host}:{port}, msg='{message}'")
        start_echo_client(host, port, message)

def run_sntp():
    """Executes Module C: SNTP Time Check."""
    print("\n--- 3. SNTP Time Check (Turkey UTC+3) ---")
    get_sntp_time()
    log_line(f"[SNTP] Checked time from pool.ntp.org")

def run_settings():
    """Executes Module E: Socket Settings & Error Management Demo."""
    print("\n--- 4. Socket Settings & Error Management ---")
    host = input("Host [google.com]: ").strip() or "google.com"
    port = int(input("Port [80]: ").strip() or 80)
    timeout = float(input("Timeout (sec) [2.0]: ").strip() or 2.0)
    recvbuf = int(input("Recv Buffer (bytes) [8192]: ").strip() or 8192)
    sendbuf = int(input("Send Buffer (bytes) [8192]: ").strip() or 8192)
    nonblocking = input("Use Non-blocking mode? (y/N): ").strip().lower() == "y"
    log_path = str(LOG_DIR / "settings_demo.log")

    demo_socket_settings(
        host=host,
        port=port,
        timeout=timeout,
        recvbuf=recvbuf,
        sendbuf=sendbuf,
        nonblocking=nonblocking,
        log_path=log_path,
    )
    log_line("[Settings] Demo completed.")

def run_chat_simple():
    """Executes Module D: Simple Chat (Server or Client)."""
    print("\n--- 5. Simple Chat ---")
    role = input("Run as (s)erver or (c)lient? (s/c): ").strip().lower()
    port = int(input("Port [6060]: ").strip() or 6060)

    if role == "s":
        host = input("Bind Host [0.0.0.0]: ").strip() or "0.0.0.0"
        log_line(f"[ChatSimple] Server on {host}:{port}")
        start_chat_server(host=host, port=port)
    else:
        host = input("Server IP [127.0.0.1]: ").strip() or "127.0.0.1"
        log_line(f"[ChatSimple] Client -> {host}:{port}")
        start_chat_client(host=host, port=port)

def main():
    """Main program loop. Displays the menu and executes choices."""
    while True:
        choice = menu()
        if choice == "1":
            run_machine_info()
        elif choice == "2":
            run_echo()
        elif choice == "3":
            run_sntp()
        elif choice == "4":
            run_settings()
        elif choice == "5":
            run_chat_simple()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Program was terminated by user (Ctrl+C).")