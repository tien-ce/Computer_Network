import socket
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from split_file import split_file
from peer_server import start_peer_server
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Peer server configuration
PEER_IP = "10.0.108.24"  # Update to the actual peer IP
PEER_PORT = 5000          # Default port for the peer server
TRACKER_IP = "10.0.108.24"  # Update to the tracker IP
TRACKER_PORT = 8000     

# Directory for saving downloaded pieces
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "..", "file_client")
os.makedirs(SAVE_DIR, exist_ok=True)
FILE_PATH = os.path.join(BASE_DIR, "file_server", "Alice_in_wonderland.txt")

@app.route('/')
def index():
    """Serve the main HTML file."""
    return app.send_static_file('index.html')

def request_piece(peer_ip, peer_port, file_path, index):
    """Request a piece from the peer server and save it."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer_ip, peer_port))
            s.sendall(str(index).encode())

            part_data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                part_data += chunk

        part_file = f"{file_path}.part{index}"
        with open(part_file, 'wb') as f:
            f.write(part_data)

        print(f"Downloaded part {index} and saved as {part_file}")
    except Exception as e:
        print(f"Error downloading part {index}: {e}")

@app.route('/download', methods=['POST'])
def download_from_torrent():
    """Download and merge pieces from a torrent file specified in the request."""
    torrent_path = request.json.get('torrent_path')

    if not torrent_path or not os.path.exists(torrent_path):
        return jsonify({"error": "The specified torrent file does not exist."}), 400

    try:
        with open(torrent_path, 'r') as f:
            meta = json.load(f)

        file_name = meta.get("file_name")
        piece_count = meta.get("piece_count")

        if file_name is None or piece_count is None:
            return jsonify({"error": "Invalid torrent metadata."}), 400

        save_path = os.path.join(SAVE_DIR, file_name)

        # Download each piece
        for i in range(piece_count):
            request_piece(PEER_IP, PEER_PORT, save_path, i)

        # Merge downloaded pieces
        merged_path = save_path
        with open(merged_path, 'wb') as out:
            for i in range(piece_count):
                part_file = f"{save_path}.part{i}"
                with open(part_file, 'rb') as pf:
                    out.write(pf.read())

        return jsonify({"message": f"File merged as {merged_path}"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/delete', methods=['POST'])
def delete_file():
    """Delete a specified file from the server."""
    file_name = request.json.get('file_name')
    file_path = os.path.join(SAVE_DIR, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
        return jsonify({"message": f"File {file_name} deleted successfully."}), 200
    else:
        return jsonify({"error": "File not found."}), 404

# Global variable to track server state
is_connect = False

@app.route('/join', methods=['POST'])
def join_port():
    """Join the tracker with the peer port."""
    global PEER_PORT, is_connect  # Use global variables for the peer configuration
    peer_port = request.json.get('peer_port')

    if not peer_port:
        return jsonify({"error": "Peer port is required!"}), 400

    PEER_PORT = peer_port  # Update the peer port
    print(f"Starting peer server on port {PEER_PORT}...")
    
    if not is_connect:
        threading.Thread(target=start_peer_server, args=(PEER_PORT, FILE_PATH)).start()
        is_connect = True  # Mark that the peer server has started

        # Announce to the tracker
        file_hash = "test_file_hash"  # Replace with actual file hash
        announce_to_tracker(file_hash, PEER_PORT)

    return jsonify({"message": f"Peer server started on port {PEER_PORT}!"}), 200

def announce_to_tracker(file_hash, port):
    """Send an announce message to the tracker."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TRACKER_IP, TRACKER_PORT))
            request_data = {
                "action": "announce",
                "file_hash": file_hash,
                "port": port
            }
            s.sendall(json.dumps(request_data).encode())
            response = s.recv(4096).decode()
            print("Tracker response:", response)
    except Exception as e:
        print(f"[!] Connection error to tracker: {e}")

if __name__ == "__main__":
    app.run(debug=True)