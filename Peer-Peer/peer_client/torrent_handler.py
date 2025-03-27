import json
import os
from request_piece import request_piece

def download_from_torrent(torrent_path, save_dir, peer_ip, peer_port):
    """
    Đọc file .torrent để biết thông tin về file cần tải,
    sau đó kết nối đến peer server để tải từng mảnh và ghép thành file hoàn chỉnh.

    Tham số:
    - torrent_path: đường dẫn tới file .torrent
    - save_dir: thư mục lưu các mảnh và file gốc
    - peer_ip, peer_port: địa chỉ của peer server sẽ kết nối đến để tải
    """

    # Đọc nội dung từ file .torrent (định dạng JSON)
    with open(torrent_path, 'r') as f:
        meta = json.load(f)

    # Lấy tên file gốc và tổng số mảnh cần tải
    file_name = meta.get("file_name")
    piece_count = meta.get("piece_count")

    # Kiểm tra định dạng file .torrent
    if not file_name or not piece_count:
        print("Invalid .torrent file.")
        return

    # Tạo thư mục lưu file nếu chưa tồn tại
    os.makedirs(save_dir, exist_ok=True)

    # Tạo đường dẫn tuyệt đối để lưu file sau khi tải xong
    save_path = os.path.join(save_dir, file_name)

    # Tải từng mảnh từ peer server
    for i in range(piece_count):
        request_piece(peer_ip, peer_port, save_path, i)

    print("All parts downloaded.")

    # Ghép các mảnh đã tải thành file hoàn chỉnh
    with open(save_path, 'wb') as out:
        for i in range(piece_count):
            part_file = f"{save_path}.part{i}"
            with open(part_file, 'rb') as pf:
                out.write(pf.read())

    print(f"File merged as {save_path}")
