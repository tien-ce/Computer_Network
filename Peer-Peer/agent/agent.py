import os
import sys
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
#---------------------- Add paths for importing ------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # Parent directory
sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)
#----------------------------------------------------------------------------------#

from peer_server.peer_server import start_upload_server
from peer_client.peer_client import start_download_from_torrent
from peer_shared.choose_file_ui import choose_torrent_file, choose_save_dir, get_user_command, get_port
from parse_torrent import parse_torrent_file

torrent_path = None
enter_event = threading.Event()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML file."""
    return app.send_static_file('index.html')

def run_agent():
    print("Agent started. Possible commands:")
    print("  uploadfile     (to choose a .torrent file and share it)")
    print("  exit           (to exit the program)")
    print("  downloadfile   (to choose a .torrent file and download it)")
    print()
    threading.Thread(target=enter_event.set, daemon=True).start()

@app.route('/input', methods=['POST'])
def upload_file():
    """Handle uploading a torrent file and sharing it."""
    torrent_path = request.json.get('torrent_path')
    
    print(torrent_path)
    
    if not torrent_path:
        return jsonify({"error": "No .torrent file was selected."}), 400
    
    # Read information from the .torrent file
    try:
        meta = parse_torrent_file(torrent_path)
    except Exception as e:
        return jsonify({"error": f"Error reading torrent file: {e}"}), 400

    file_hash = meta["file_hash"]
    file_name = meta["file_name"]
    piece_count = meta["piece_count"]
    piece_size = meta["piece_size"]

    if not file_name:
        return jsonify({"error": "No file name found in torrent metadata."}), 400

    # Original file resides in the 'file_server' directory
    file_path = os.path.join(PROJECT_ROOT, "file_server", file_name)
    port_str = get_port()

    if not port_str or not port_str.isdigit():
        return jsonify({"error": "Invalid port input."}), 400

    upload_port = int(port_str)
    start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port)

    return jsonify({"message": "Upload server started."}), 200

@app.route('/download', methods=['POST'])
def download_file():
    """Download and merge pieces from a torrent file specified in the request."""
    torrent_path = request.json.get('torrent_path')
    print(PROJECT_ROOT)
    if not torrent_path or not os.path.exists(torrent_path):
        return jsonify({"error": "The specified torrent file does not exist."}), 400

    # save_dir = choose_save_dir(PROJECT_ROOT)
    start_download_from_torrent(torrent_path, "D:/btl mang/Computer_Network/Peer-Peer/file_client")

    return jsonify({"message": "Download started."}), 200

if __name__ == "__main__":
    app.run(debug=True)
