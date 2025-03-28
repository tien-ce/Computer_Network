import os
import json
import time
from torrent_handler import prepare_download_plan
from commucation_peer_server import get_bitfields
from commucation_peer_server import request_piece
from get_peers import get_peers
import sys
#---------------------- Đây là phần add các path để import------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # thư mục  cha
sys.path.append(PROJECT_ROOT)   
from peer_shared.Info_shared import TRACKER_IP, TRACKER_PORT
from peer_shared.choose_file_ui import choose_torrent_file
#-------------------------------------------------------------------------------------------------#

TORRENT_PATH = choose_torrent_file(PROJECT_ROOT)
if not TORRENT_PATH:
    print("Bạn chưa chọn file .torrent. Kết thúc chương trình.")
    exit()
# Thư mục dùng để lưu các file đã tải và các mảnh
SAVE_DIR = os.path.join(BASE_DIR, "..", "file_client")

# Đọc file .torrent để lấy file_hash (định danh duy nhất của file cần chia sẻ)
# file_hash này sẽ dùng để thông báo lên tracker xem node này đang tải/giữ file nào

complete = False
while complete == False:
    with open(TORRENT_PATH, 'r') as f:
        meta = json.load(f)
        file_hash = meta["file_hash"]
        file_name = meta["file_name"]
        piece_count = meta["piece_count"]
    # Bước 1 : Lấy danh sách các peer chứa file đang cần
    peers = get_peers(file_hash,TRACKER_IP,TRACKER_PORT) # Trả về danh sách các peer chứa file
    # Bước 2 : Lập bảng các mảnh sẽ có các các peer nào có
    os.makedirs(SAVE_DIR,exist_ok=True)
    save_path = os.path.join(SAVE_DIR,file_name)    # Đường dẫn lưu file
    bitfields = get_bitfields(peers,piece_count)    # Các peer chứa các mảnh nào
    # [{ip:...,port:....} : 0110 , {ip:...,port:....} : 1110]  
    piece_to_peer = prepare_download_plan(bitfields=bitfields,piece_count=piece_count) # Danh sách các peer tương ứng với mảnh
    # [0: {ip:...,port:....},{ip:...,port},....]
    # Bước 3 : Tải các part nếu có peer_server đang chứa
    complete = True
    for i in range(piece_count):
        if os.path.exists(f"{save_path}.part{i}"):
            continue    #Nếu đã có mảnh thì bỏ qua
        peer_list = piece_to_peer.get(i,[]) # Danh sách các peer chứa part thứ i
        if not peer_list:
            print(f"[!] No peer has part {i}, skipping.") # Part thứ i không có peer nào chứa
            complete = False
            continue
        # Chọn peer đầu tiên trong danh sách có mảnh này để tải
        peer_ip, peer_port = peer_list[0]
        request_piece(peer_ip=peer_ip,peer_port=peer_port,file_path=save_path,index=i) # Tải peer xuống 
    time.sleep(3) # Tránh gọi liên tục
# Bước 4 : Ghép file
with open(save_path, 'wb') as out:
    for i in range(piece_count):
        part_file = f"{save_path}.part{i}"
        if os.path.exists(part_file):
            with open(part_file, 'rb') as pf:
                out.write(pf.read())

print(f"File merged as {save_path}")