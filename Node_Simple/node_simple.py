import socket
import threading
import json
from split_file import split_file
from peer_server import start_peer_server
import os
# Địa chỉ của tracker
TRACKER_IP = "10.0.108.24"
TRACKER_PORT = 8000
# Lấy đường dẫn tuyệt đối tới thư mục chứa file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ghép với đường dẫn tương đối đến file cần chia
FILE_PATH = os.path.join(BASE_DIR,"file_server", "Alice_in_wonderland.txt")
PIECE_SIZE = 150 * 1024  # 150 KB

# Port mà peer này sẽ mở ra để chia sẻ file
UPLOAD_PORT = 5000

# Hàm gửi thông báo announce đến tracker
def announce(file_hash, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TRACKER_IP, TRACKER_PORT))
    request = {
        "action": "announce",
        "file_hash": file_hash,
        "port": port
    }
    s.sendall(json.dumps(request).encode())
    response = s.recv(4096).decode()
    print("Tracker response:", response)
    s.close()

# Bước 1: Chia file thành các mảnh
print("Splitting file...")
total_parts = split_file(FILE_PATH, PIECE_SIZE)

# Bước 2: Gửi announce lên tracker
# print("Announcing to tracker...")
# announce("test_file_hash", UPLOAD_PORT)

# Bước 3: Khởi động server chia sẻ file cho các peer khác
threading.Thread(target=start_peer_server, args=(UPLOAD_PORT, FILE_PATH, total_parts)).start()

# Giữ chương trình chạy
while True:
    pass
