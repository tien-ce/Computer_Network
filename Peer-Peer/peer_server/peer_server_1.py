import threading
import os
from split_file import split_file
from start_and_handle_request import start_peer_server
import sys  # Ngắt chương trình đang chạy
from announce import announce
import json
#---------------------- Đây là phần add các path để import cùng các thông tin chung------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # thư mục  cha
sys.path.append(PROJECT_ROOT)   
from peer_shared.Info_shared import TRACKER_IP, TRACKER_PORT,PIECE_SIZE
from peer_shared.choose_file_ui import choose_torrent_file
#-----------------------------------------------------------------------------------------------------------------------#


#--------------------------- Đây là phần định nghĩa các path liên quan đến nơi upload và tải file---------------------------------------#
# Lấy đường dẫn tuyệt đối tới thư mục chứa file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ghép với đường dẫn tương đối đến file cần chia
# FILE_PATH = os.path.join(BASE_DIR, "../file_server", "2025-03-02 20-50-04.mkv")
TORRENT_PATH = choose_torrent_file(PROJECT_ROOT) #Đường dẫn đến file torrent để cung cấp cho tracker, 
#truyền vào root thì khi mở lêm giao diện sẽ ở ngay thư mục root.
# Port mà peer này sẽ mở ra để chia sẻ file
UPLOAD_PORT = 6000  # Cần khác với peer_server để có thể test 2 server cùng 1 lúc
if not TORRENT_PATH :
    print("Bạn chưa chọn file .torrent. Kết thúc chương trình.")
    exit()
total_parts = 0
#-----------------------------------------------------------------------------------------------------------------------------------------#

# Bước 1: Chia file thành các mảnh
# print("Splitting file...")
# total_parts = split_file(FILE_PATH, PIECE_SIZE)
# Bước 2: Gửi announce lên tracker
# Lấy file_hash từ file .torrent tương ứng
with open(TORRENT_PATH, 'r') as f:
    meta = json.load(f)
    file_hash = meta["file_hash"]
    total_parts = meta.get("piece_count")
print("Announcing to tracker...")
announce(TRACKER_IP, TRACKER_PORT, file_hash, UPLOAD_PORT)
# Bước 3: Khởi động server chia sẻ file cho các peer khác
FILE_PATH = TORRENT_PATH[0:-8] # Đường dẫn đến nơi chứa cách mảng, cắt đuôi .torrent từ TORRENT_PATH
threading.Thread(target=start_peer_server, args=(UPLOAD_PORT, FILE_PATH, total_parts)).start()

# Giữ chương trình chạy
while True:
    sys.exit()
    pass
