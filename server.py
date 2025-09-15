import socket
import threading
import logging
from datetime import datetime

# Constants
HOST = '127.0.0.1'  # localhost
PORT = 5000
MAX_CLIENTS = 10
ENCODING = 'utf-8'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Welcome message
WELCOME = (
    "Welcome to the Chat!\n"
    "Commands: /quit to exit, /users to list, /help for help.\n"
)

# Store client connections and usernames
clients = {}
clients_lock = threading.Lock()

def broadcast(message: str, exclude_conn=None):
    with clients_lock:
        for conn in list(clients.keys()):
            if conn is exclude_conn:
                continue
            try:
                conn.sendall(message.encode(ENCODING))
            except Exception as e:
                logging.warning(f"Send failed to {clients.get(conn, 'unknown')}: {e}")
                try:
                    conn.close()
                except Exception:
                    pass
                clients.pop(conn, None)

def handle_client(conn: socket.socket, addr: tuple):
    """Handle individual client connections"""
    try:
        # Get username
        conn.sendall("Enter your username: ".encode(ENCODING))
        username = conn.recv(1024).decode(ENCODING).strip()
        
        with clients_lock:
            clients[conn] = username
        
        # Send welcome message
        conn.sendall(WELCOME.encode(ENCODING))
        broadcast(f"[{username} joined the chat]\n", conn)
        
        # Main client loop
        while True:
            msg = conn.recv(1024).decode(ENCODING).strip()
            if not msg:
                break
                
            if msg == "/quit":
                break
            elif msg == "/users":
                with clients_lock:
                    user_list = ", ".join(clients.values())
                conn.sendall(f"Online users: {user_list}\n".encode(ENCODING))
            elif msg == "/help":
                conn.sendall(WELCOME.encode(ENCODING))
            else:
                timestamp = datetime.now().strftime("%H:%M")
                broadcast(f"[{timestamp}] {username}: {msg}\n")
                
    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}")
    finally:
        with clients_lock:
            username = clients.pop(conn, "unknown")
        try:
            conn.close()
        except Exception:
            pass
        broadcast(f"[{username} left the chat]\n")

def start_server():
    """Initialize and run the chat server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)
        logging.info(f"Server started on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            logging.info(f"New connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
            
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()