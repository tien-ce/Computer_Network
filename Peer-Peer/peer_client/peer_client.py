import os
import json
import time
from peer_client.torrent_handler import prepare_download_plan
from peer_client.commucation_peer_server import get_bitfields
from peer_client.commucation_peer_server import request_piece
from peer_shared.Info_shared import TRACKER_IP, TRACKER_PORT
from peer_client.get_peers import get_peers
import sys

def show_progress_bar(current, total, bar_length=30):
    percent = float(current) / total
    arrow = '#' * int(round(percent * bar_length))
    spaces = '-' * (bar_length - len(arrow))
    sys.stdout.write(f"\r[{arrow}{spaces}] {int(percent * 100)}% downloaded...")
    sys.stdout.flush()
def start_download_from_torrent(TORRENT_PATH,SAVE_DIR):
    if not TORRENT_PATH or not SAVE_DIR:
        print("Not path file, please choose again")
        return
    # Đọc file .torrent để lấy file_hash (cái định danh duy nhất của file cần chia sẻ)
    complete = False
    while complete == False:
        with open(TORRENT_PATH, 'r') as f:
            meta = json.load(f)
            file_hash = meta["file_hash"]
            file_name = meta["file_name"]
            piece_count = meta["piece_count"]
            piece_size = meta['piece_size']
        # Bước 1 : Lấy danh sách các peer chứa file đang cần
        peers = get_peers(file_hash, TRACKER_IP, TRACKER_PORT)  # Trả về danh sách các peer chứa file

        # Bước 2 : Lập bảng các mảnh sẽ có các các peer nào có
        os.makedirs(SAVE_DIR, exist_ok=True)
        save_path = os.path.join(SAVE_DIR, file_name)  # Đường dẫn lưu file
        bitfields = get_bitfields(peers, piece_count)  # Các peer chứa các mảnh nào
        piece_to_peer = prepare_download_plan(bitfields=bitfields, piece_count=piece_count)  # Danh sách các peer tương ứng với mảnh

        # Bước 3 : Tải các part nếu có peer_server đang chứa
        complete = True
        downloaded_parts = 0
        for i in range(piece_count):
            if os.path.exists(f"{save_path}.part{i}"):
                downloaded_parts += 1
                continue

            peer_list = piece_to_peer.get(i, [])
            if not peer_list:
                complete = False
                continue

            peer_ip, peer_port = peer_list[0]
            request_piece(
                peer_ip=peer_ip,
                peer_port=peer_port,
                file_path=save_path,
                index=i,
                file_hash=file_hash,
                peer_id=None,
                piece_size=piece_size,
                total_pieces=piece_count
            )
            # show_progress_bar(downloaded_parts, piece_count)
            time.sleep(0.2)  # Cho dễ thấy tiến độ (có thể bỏ đi)
        time.sleep(3)  # Tránh gọi liên tục
    # Bước 4 : Ghép file
    with open(save_path, 'wb') as out:
        for i in range(piece_count):
            part_file = f"{save_path}.part{i}"
            if os.path.exists(part_file):
                with open(part_file, 'rb') as pf:
                    out.write(pf.read())

    print(f"File merged as {save_path}")