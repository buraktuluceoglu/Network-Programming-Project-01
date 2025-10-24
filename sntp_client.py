"""
    This code retrieves the current time from an SNTP server 
    (e.g., pool.ntp.org) using the 'ntplib' library.

    In accordance with project requirements, 
    this module converts the received UTC time 
    to Turkish time (UTC+3) and compares it to the 
    local system time.
    
"""

import ntplib
from datetime import datetime, timedelta
import time
import socket

def get_sntp_time(server="pool.ntp.org"):
    
    print(f"Querying time from {server}...")

    ntp_client = ntplib.NTPClient()
    
    try:
        response = ntp_client.request(server, version=3)
        
        sntp_time_unix = response.tx_time
        
        local_time_unix = time.time()
        
        # Convert SNTP time (which is UTC) to Python datetime object
        sntp_datetime_utc = datetime.utcfromtimestamp(sntp_time_unix)
        
        # --- Turkey Time (UTC+3) Conversion ---
        # Add 3 hours to UTC time to get Turkish time
        sntp_datetime_turkey = sntp_datetime_utc + timedelta(hours=3)
        # --- End Conversion ---

        local_datetime_now = datetime.now() 

        print(f"------------------------------------")
        print(f"SNTP Server Time (UTC):     {sntp_datetime_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"SNTP Server Time (Turkey):  {sntp_datetime_turkey.strftime('%Y-%m-%d %H:%M:%S')} (UTC+3)")
        print(f"Local System Time:          {local_datetime_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        offset = sntp_time_unix - local_time_unix
        print(f"Time Offset (Server - Local): {offset:+.4f} seconds")
        
        if abs(offset) < 0.1: 
            print("Result: System clock is synchronized.")
        elif offset > 0:
            print(f"Result: System clock is {abs(offset):.4f} seconds BEHIND.")
        else:
            print(f"Result: System clock is {abs(offset):.4f} seconds AHEAD.")
            
    except ntplib.NTPException as e:
        print(f"ERROR: Could not retrieve time from NTP server. Details: {e}")
    except socket.gaierror:
        print(f"ERROR: Could not resolve server address ({server}). Check your internet connection.")
    except socket.timeout:
        print(f"ERROR: Connection timed out.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
    finally:
        print("------------------------------------")

if __name__ == "__main__":
    print("--- Testing SNTP Client Module Directly ---")
    get_sntp_time()