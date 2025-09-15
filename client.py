import socket
import threading
import sys

# Constants
HOST = "127.0.0.1"
PORT = 5000
ENCODING = "utf-8"
BUFFER_SIZE = 4096

def recv_loop(sock: socket.socket):
    """Handle receiving messages from server"""
    try:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("\n[Disconnected by server]")
                break
            print(data.decode(ENCODING), end="")
    except Exception as e:
        print(f"\n[Receive loop ended: {e}]")

def main(host=HOST, port=PORT, username=None):
    """Main client loop"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to server
            try:
                s.connect((host, port))
            except ConnectionRefusedError:
                print(f"[ERROR] Could not connect to server at {host}:{port}")
                return
            
            # Handle username
            prompt = s.recv(BUFFER_SIZE).decode(ENCODING)
            print(prompt, end="")
            if not username:
                username = input().strip()
            s.sendall((username + "\n").encode(ENCODING))

            # Print welcome message
            welcome = s.recv(BUFFER_SIZE).decode(ENCODING)
            print(welcome, end="")

            # Start receiver thread
            t = threading.Thread(target=recv_loop, args=(s,), daemon=True)
            t.start()

            # Main send loop
            try:
                while True:
                    msg = input()
                    s.sendall((msg + "\n").encode(ENCODING))
                    if msg == "/quit":
                        break
            except (KeyboardInterrupt, EOFError):
                try:
                    s.sendall("/quit\n".encode(ENCODING))
                except Exception:
                    pass

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    # Usage: python client.py [host] [port] [username]
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT
    username = sys.argv[3] if len(sys.argv) > 3 else None
    
    main(host, port, username)