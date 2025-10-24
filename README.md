## Network Programming Project

### Overview

Python-based network programming project demonstrating key concepts in client-server communication, socket configuration, and time synchronization.
Interactive CLI menu integrates multiple modules with logging and error handling.

### Modules:
	1.	Machine Information
	2.	Echo Server/Client
	3.	SNTP Time Check
	4.	Socket Settings & Error Management
	5.	Simple Chat (multi-threaded)

## Project Structure
	.
	├── main.py
	├── machine_info.py
	├── echo_server.py
	├── echo_client.py
	├── sntp_client.py
	├── settings.py
	├── simple_chat_server.py
	├── simple_chat_client.py
	├── logs/
	├── chat_history.log

## Features

### 1. Machine Information
	 •	Displays hostname, IP, and network interfaces.
<img width="284" height="108" alt="Ekran Resmi 2025-10-24 21 20 03" src="https://github.com/user-attachments/assets/93b2555c-8ce5-42aa-8d39-9d0d6ceeafea" />

### 2. Echo Server/Client
		•	TCP echo server and client.
		•	Server echoes messages received from client.
<img width="488" height="215" alt="Ekran Resmi 2025-10-24 21 42 36" src="https://github.com/user-attachments/assets/35134510-97c4-478c-93d7-58c8a0407442" />
<img width="575" height="180" alt="Ekran Resmi 2025-10-24 21 42 46" src="https://github.com/user-attachments/assets/02e4312b-8cc7-4b97-9b87-98888d6c26f8" />

### 3. SNTP Time Check
		•	Retrieves time from SNTP servers (e.g., pool.ntp.org).
		•	Converts UTC to Turkey time (UTC+3) and compares with local time.
<img width="466" height="182" alt="Ekran Resmi 2025-10-24 21 45 05" src="https://github.com/user-attachments/assets/b4149bbe-78a4-4ce8-8a3d-692f40029659" />

### 4. Socket Settings & Error Management
		•	Demonstrates socket timeout, buffer sizes, blocking/non-blocking modes.
		•	Logs connection results and errors.
<img width="373" height="278" alt="Ekran Resmi 2025-10-24 21 46 15" src="https://github.com/user-attachments/assets/ce2c2c1f-7343-43ea-a9ee-e50e2e109446" />

### 5. Simple Chat
		•	Multi-threaded TCP chat for concurrent send/receive.
		•	Logs all messages to chat_history.log.
<img width="473" height="175" alt="Ekran Resmi 2025-10-24 21 47 23" src="https://github.com/user-attachments/assets/ba8ba012-d34b-4b2f-994c-8ee3795b3b5a" />

## Requirements
	•	Python 3.8+
	•	Libraries: pip install psutil ntplib

## How to Run

### Main Menu
	python3 main.py
	
<img width="323" height="191" alt="Ekran Resmi 2025-10-24 21 49 11" src="https://github.com/user-attachments/assets/1d5f12a7-0ff4-4aae-9ae0-054487d0fc90" />

	Select module from menu.



	









