import json
import os
from peer_client.commucation_peer_server import request_piece
from peer_client.commucation_peer_server import get_bitfields
def prepare_download_plan(bitfields, piece_count):
    """
    Dựa vào bitfield của các peer, xác định xem mảnh nào có thể tải từ những peer nào.

    Tham số:
    - bitfields: dict {(ip, port): [1, 0, 1, ...]}, thể hiện các peer đang giữ mảnh nào
    - piece_count: tổng số mảnh của file cần tải

    Trả về:
    - Dictionary {part_index: [list các peer có mảnh này]}
      Ví dụ: {0: [(ip1,port1)], 1: [(ip2,port2), (ip3,port3)], ...}
    """

    # Tạo một dict ban đầu, mỗi key là chỉ số mảnh (0 → piece_count - 1), value là danh sách rỗng
    # Mục tiêu là sau đó sẽ thêm danh sách các peer có từng mảnh tương ứng
    piece_to_peers = {i: [] for i in range(piece_count)} 

    # Duyệt qua từng peer trong bitfields
    # peer có dạng (ip, port), bitfield là list 0/1
    for peer, bitfield in bitfields.items():
        # Duyệt qua từng chỉ số mảnh (index)
        for index in range(piece_count):
            # Kiểm tra: nếu chỉ số index hợp lệ và bitfield[index] == 1 nghĩa là peer này có mảnh đó
            if index < len(bitfield) and bitfield[index] == 1:
                # Thêm peer vào danh sách những peer có mảnh index
                piece_to_peers[index].append(peer)

    # Trả về bảng phân phối mảnh → peer
    return piece_to_peers


import json
import os
from peer_client.commucation_peer_server import request_piece, get_bitfields

def download_from_torrent(torrent_path, save_dir, peers):
    """
    Tải và ghép file từ nhiều peer, dựa trên bitfield mỗi peer.
    
    Tham số:
    - torrent_path: đường dẫn tới file .torrent
    - save_dir: thư mục lưu
    - peers: danh sách peer [{'ip':..., 'port':...}]
    """

    # Bước 1: Đọc thông tin từ file .torrent
    with open(torrent_path, 'r') as f:
        meta = json.load(f)

    file_name = meta.get("file_name")
    piece_count = meta.get("piece_count")

    if not file_name or not piece_count:
        print("Invalid .torrent file.")
        return

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file_name)

    # Bước 2: Lấy bitfield từ tất cả các peer
    bitfields = get_bitfields(peers, piece_count)

    # Bước 3: Lập kế hoạch tải dựa trên bitfield
    piece_to_peers = prepare_download_plan(bitfields, piece_count)

    # Bước 4: Tải từng mảnh từ peer có nó
    for i in range(piece_count):
        peer_list = piece_to_peers.get(i, [])
        if not peer_list:
            print(f"[!] No peer has part {i}, skipping.")
            continue

        # Chọn peer đầu tiên trong danh sách có mảnh này để tải
        peer_ip, peer_port = peer_list[0]
        request_piece(peer_ip, peer_port, save_path, i)

    print("All parts downloaded.")

    # Bước 5: Ghép file
    with open(save_path, 'wb') as out:
        for i in range(piece_count):
            part_file = f"{save_path}.part{i}"
            if os.path.exists(part_file):
                with open(part_file, 'rb') as pf:
                    out.write(pf.read())

    print(f"File merged as {save_path}")
