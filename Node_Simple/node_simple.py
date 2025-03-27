import socket
import threading
import json
from split_file import split_file
from peer_server import start_peer_server
import os

TRACKER_IP = "10.0.108.24"
TRACKER_PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Đã sửa từ 'file' thành '__file__'
FILE_PATH = os.path.join(BASE_DIR, "file_server", "Alice_in_wonderland.txt")
PIECE_SIZE = 150 * 1024  # 150 KB

UPLOAD_PORT = 5000

def announce(file_hash, port):
    """Gửi thông báo announce đến tracker."""
    # try:
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((TRACKER_IP, TRACKER_PORT))
    #         request = {
    #             "action": "announce",
    #             "file_hash": file_hash,
    #             "port": port
    #         }
    #         s.sendall(json.dumps(request).encode())
    #         response = s.recv(4096).decode()
    #         print("Tracker response:", response)
    # except Exception as e:
    #     print(f"[!] Lỗi kết nối đến tracker: {e}")

def main():
    # Bước 1: Chia file thành các mảnh
    # print("Splitting file...")
    # total_parts = split_file(FILE_PATH, PIECE_SIZE)

    # # # Bước 2: Gửi announce lên tracker
    # file_hash = "test_file_hash"  # Thay thế bằng hash file thực tế
    # print("Announcing to tracker...")
    # announce(file_hash, UPLOAD_PORT)

    # # Bước 3: Khởi động server chia sẻ file cho các peer khác
    # print("Starting peer server...")
    threading.Thread(target=start_peer_server, args=(UPLOAD_PORT, FILE_PATH)).start()

    # Giữ chương trình chạy
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping the peer client.")

if __name__ == "__main__":
    main()