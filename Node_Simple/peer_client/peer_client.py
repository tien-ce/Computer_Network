import os
from torrent_handler import download_from_torrent
from announce import announce_to_tracker

# Lấy đường dẫn tuyệt đối tới thư mục chứa file hiện tại (peer_client.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ghép đường dẫn để tìm tới file .torrent cần sử dụng
TORRENT_PATH = os.path.join(BASE_DIR, "..", "file_client", "keywords.txt.torrent")

# Thư mục dùng để lưu các file đã tải và các mảnh
SAVE_DIR = os.path.join(BASE_DIR, "..", "file_client")

# Địa chỉ IP của peer server sẽ kết nối đến để tải các mảnh
PEER_IP = "192.168.1.153"  # Cập nhật IP đúng nếu cần
PEER_PORT = 5000           # Cổng mà peer server đang lắng nghe

# Địa chỉ IP và cổng của tracker dùng để gửi announce
TRACKER_IP = "192.168.1.153"
TRACKER_PORT = 8000

# Đọc file .torrent để lấy file_hash (định danh duy nhất của file cần chia sẻ)
# file_hash này sẽ dùng để thông báo lên tracker xem node này đang tải/giữ file nào
import json
with open(TORRENT_PATH, 'r') as f:
    file_hash = json.load(f)["file_hash"]

# Gửi thông báo announce tới tracker
# Nội dung thông báo gồm: action = "announce", file_hash, và cổng của peer
announce_to_tracker(file_hash, PEER_PORT, TRACKER_IP, TRACKER_PORT)

# Gọi hàm để tiến hành tải các mảnh từ peer server
# Sau khi tải đủ các mảnh, tự động ghép thành file hoàn chỉnh theo định dạng ban đầu
download_from_torrent(TORRENT_PATH, SAVE_DIR, PEER_IP, PEER_PORT)
