import os
from torrent_handler import prepare_download_plan
from commucation_peer_server import get_bitfields
from get_peers import get_peers
import json
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

complete = False
while complete == False:
    with open(TORRENT_PATH, 'r') as f:
        file_hash = json.load(f)["file_hash"]
        file_name = json.load(f)["file_name"]
        piece_count = json.load(f)["piece_count"]
    # Bước 1 : Lấy danh sách các peer chứa file đang cần
    peers = get_peers(file_hash,TRACKER_IP,TRACKER_PORT) # Trả về danh sách các peer chứa file
    # Bước 2 : Lập bảng các mảnh sẽ có các các peer nào có
    os.makedirs(SAVE_DIR,exist_ok=True)
    save_path = os.path.join(SAVE_DIR,file_name)    # Đường dẫn lưu file
    bitfields = get_bitfields(peers,piece_count)    # Danh sách các peer chứa mảnh
    # [0: {ip:...,port:....},{ip:...,port},....]
     