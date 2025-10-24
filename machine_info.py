"""

"""

import os 
import socket
import psutil

def print_machine_info():

    try:
        hostname = socket.gethostname()
        print(f"Hostname: {hostname}")
    except socket.error as e:
        print(f"Error: Could not get hostname: {e}")
        hostname = "Unknown"

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"IP address: {ip_address}")
    except socket.error as e:
        print("Error!")
        hostname = "Unknown"

    try:
        network_interface = psutil.net_if_addrs()
        print(f"Network Interface: {network_interface}")
    except psutil.Error as e:
        print("Error!")
        network_interface = "Unknown"

if __name__ == "__main__":
    print_machine_info()

