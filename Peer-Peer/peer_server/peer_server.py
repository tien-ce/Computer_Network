import threading
import os
from split_file import split_file
from start_and_handle_request import start_peer_server
from announce import announce

# Cấu hình địa chỉ tracker
TRACKER_IP = "192.168.15.86" # Nếu muốn test dùng ip hiện tại của máy
TRACKER_PORT = 8000

# Lấy đường dẫn tuyệt đối tới thư mục chứa file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ghép với đường dẫn tương đối đến file cần chia
FILE_PATH = os.path.join(BASE_DIR, "../file_server", "Alice_in_wonderland.txt")
PIECE_SIZE = 150 * 1024  # 150 KB

# Port mà peer này sẽ mở ra để chia sẻ file
UPLOAD_PORT = 5000

# Bước 1: Chia file thành các mảnh
print("Splitting file...")
total_parts = split_file(FILE_PATH, PIECE_SIZE)

# Bước 2: Gửi announce lên tracker
# Lấy file_hash từ file .torrent tương ứng
torrent_file = f"{FILE_PATH}.torrent"
import json
with open(torrent_file, 'r') as f:
    meta = json.load(f)
    file_hash = meta["file_hash"]

print("Announcing to tracker...")
announce(TRACKER_IP, TRACKER_PORT, file_hash, UPLOAD_PORT)

# Bước 3: Khởi động server chia sẻ file cho các peer khác
threading.Thread(target=start_peer_server, args=(UPLOAD_PORT, FILE_PATH, total_parts)).start()

# Giữ chương trình chạy
while True:
    pass
