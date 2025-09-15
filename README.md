Python Concurrent Chat Application

A minimal, reliable multi-user chat system built with Python sockets.
This project was created as an independent learning exercise to strengthen networking, troubleshooting, and documentation skills.

-------------------------------------------------------------
Features
-------------------------------------------------------------
- Multi-client broadcast with threading
- Simple commands:
  - /users – list online users
  - /help – show quick help
  - /quit – exit the chat
- Logging to logs/server.log for easy troubleshooting
- Graceful disconnects & basic error handling
- Clear documentation and runbook-style instructions

-------------------------------------------------------------
Quick Start
-------------------------------------------------------------
1. Clone this repository
   git clone https://github.com/KaziBadrulArif/Python-ChatApp.git
   cd Python-ChatApp

2. Start the server
   Windows: python server.py
   macOS/Linux: python3 server.py
   The server will print: "Server listening on 0.0.0.0:5050"

3. Start a client (new terminal window)
   Windows: python client.py 127.0.0.1 5050 YourName
   macOS/Linux: python3 client.py 127.0.0.1 5050 YourName

   You can open multiple clients to chat.

-------------------------------------------------------------
Troubleshooting
-------------------------------------------------------------
- Port already in use → Change the PORT variable in server.py (e.g., 5051).
- Firewall blocked → Allow Python through your firewall, or use 127.0.0.1 for local testing.
- No output → Make sure both server and clients are running on the same host/network.

-------------------------------------------------------------
Runbook (Ops-style)
-------------------------------------------------------------
- Restart server → Ctrl+C, then python server.py
- Rotate logs → Stop server → backup logs/server.log → restart server
- Kick ghost users → Restart server (simple method for this demo)

-------------------------------------------------------------
Frameworks & Tools
-------------------------------------------------------------
Python, Sockets, Threading, Logging

-------------------------------------------------------------
License
-------------------------------------------------------------
This project is open for educational use. Feel free to fork and adapt.
