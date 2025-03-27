import os
from torrent_handler import download_from_torrent
from announce import announce_to_tracker
from get_peers import get_peers
# Lấy đường dẫn tuyệt đối tới thư mục chứa file hiện tại (peer_client.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ghép đường dẫn để tìm tới file .torrent cần sử dụng
TORRENT_PATH = os.path.join(BASE_DIR, "..", "file_client", "Alice_in_wonderland.txt.torrent")

# Thư mục dùng để lưu các file đã tải và các mảnh
SAVE_DIR = os.path.join(BASE_DIR, "..", "file_client")

# Địa chỉ IP của peer server sẽ kết nối đến để tải các mảnh
PEER_IP = "192.168.15.86"  # Cập nhật IP đúng nếu cần
PEER_PORT = 5000           # Cổng mà peer server đang lắng nghe

# Địa chỉ IP và cổng của tracker dùng để gửi announce
TRACKER_IP = "192.168.15.86"
TRACKER_PORT = 8000

# Đọc file .torrent để lấy file_hash (định danh duy nhất của file cần chia sẻ)
# file_hash này sẽ dùng để thông báo lên tracker xem node này đang tải/giữ file nào
import json
with open(TORRENT_PATH, 'r') as f:
    file_hash = json.load(f)["file_hash"]

peers = get_peers(file_hash,TRACKER_IP,TRACKER_PORT) # Trả về danh sách các peer chứa file
peer = peers[0] # Tạm thời chỉ có 1 phần tử, dùng để test  , có định dạng {'ip':.... , 'port':....}
print(peer)
PEER_IP = peer['ip']
PEER_PORT = peer['port']
# Gọi hàm để tiến hành tải các mảnh từ peer server
# Sau khi tải đủ các mảnh, tự động ghép thành file hoàn chỉnh theo định dạng ban đầu
download_from_torrent(TORRENT_PATH, SAVE_DIR, PEER_IP, PEER_PORT)
