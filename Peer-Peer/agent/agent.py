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
    """
    Nhận vào tên file gốc (file_path), tự tìm file .torrent tương ứng,
    chia file nếu chưa có, rồi khởi động upload server.
    """
    from peer_server.split_file import split_file  # Hàm chia file thành .partX
    file_name = request.json.get('file_path')  # Ví dụ: "Alice_in_wonderland.txt"

    if not file_name:
        return jsonify({"error": "No file was selected."}), 400

    # Xác định đường dẫn file torrent tương ứng
    torrent_filename = file_name + ".torrent"
    torrent_path = os.path.join(PROJECT_ROOT, "file_server", torrent_filename)
    print(f"[DEBUG][UPLOAD] Reading torrent file at: {torrent_path}")

    # Đọc metadata từ file .torrent
    try:
        meta = parse_torrent_file(torrent_path)
    except Exception as e:
        return jsonify({"error": f"Error reading torrent file: {e}"}), 400

    file_hash = meta["file_hash"]
    piece_count = meta["piece_count"]
    piece_size = meta["piece_size"]

    if not meta.get("file_name"):
        return jsonify({"error": "No file name found in torrent metadata."}), 400

    # Đường dẫn tới file gốc cần chia sẻ
    file_path = os.path.join(PROJECT_ROOT, "file_server", file_name)

    # Chia file nếu chưa có part
    if not os.path.exists(f"{file_path}.part0"):
        split_file(file_path, piece_size)
        print("[INFO] File split successfully.")
    else:
        print("[INFO] Part files already exist, skipping split.")

    # Xin port người dùng nhập (hoặc bạn có thể sinh port ngẫu nhiên)
    port_str = get_port()
    if not port_str or not port_str.isdigit():
        return jsonify({"error": "Invalid port input."}), 400

    upload_port = int(port_str)

    # Khởi động upload server (sẽ announce tracker + chia sẻ)
    return start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port)


@app.route('/download', methods=['POST'])
def download_file():
    """
    Download and merge pieces from a torrent file specified in the request.
    Client gửi lên: {
        "torrent_path": "Alice_in_wonderland.txt.torrent",
        "Path": "file_client" (hoặc tên thư mục con khác nếu cần)
    }
    """
    torrent_filename = request.json.get('torrent_path')  
    save_dir_name = request.json.get('Path')             

    if not torrent_filename or not save_dir_name:
        return jsonify({"error": "Missing torrent filename or save path."}), 400

    # Tạo đường dẫn tuyệt đối
    torrent_path = os.path.join(PROJECT_ROOT, "file_client", torrent_filename)
    save_dir = os.path.join(PROJECT_ROOT, save_dir_name)

    print(f"[DEBUG] Torrent path: {torrent_path}")
    print(f"[DEBUG] Save directory: {save_dir}")

    # Kiểm tra file torrent tồn tại
    if not os.path.exists(torrent_path):
        return jsonify({"error": f"The specified torrent file does not exist: {torrent_path}"}), 400

    # Tạo thư mục lưu file nếu chưa có
    try:
        os.makedirs(save_dir, exist_ok=True)
    except PermissionError as e:
        return jsonify({"error": f"Cannot create save directory: {save_dir}. Error: {str(e)}"}), 500

    # Bắt đầu tải
    try:
        start_download_from_torrent(torrent_path, save_dir)
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

    return jsonify({"message": "Download started."}), 200

if __name__ == "__main__":
    app.run(debug=True)
