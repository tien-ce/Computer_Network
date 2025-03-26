import socket
import json
import os

# Địa chỉ IP và cổng của peer server
PEER_IP = "192.168.15.86"     # Cập nhật IP peer thật
PEER_PORT = 5000              # Cổng peer server mở để chia sẻ

# Đường dẫn tới file .torrent
# Lấy đường dẫn tuyệt đối tới thư mục chứa file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ghép với đường dẫn tương đối đến file cần chia
TORRENT_PATH = os.path.join(BASE_DIR,"..","file_server","Alice_in_wonderland.txt.torrent")

# Thư mục lưu mảnh
SAVE_DIR = os.path.join(BASE_DIR,"..","file_client")
print("Torrent file path:", TORRENT_PATH)
print("Save directory:", SAVE_DIR)
# Hàm gửi yêu cầu tải một mảnh
def request_piece(peer_ip, peer_port, file_path, index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((peer_ip, peer_port))
        s.sendall(str(index).encode())

        part_data = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            part_data += chunk

        part_file = f"{file_path}.part{index}"
        with open(part_file, 'wb') as f:
            f.write(part_data)

        print(f"Downloaded part {index} and saved as {part_file}")
        s.close()
    except Exception as e:
        print(f"Error downloading part {index}: {e}")

# Hàm đọc file .torrent và tải tất cả các mảnh
def download_from_torrent(torrent_path):
    with open(torrent_path, 'r') as f:
        meta = json.load(f)

    file_name = meta["file_name"]
    piece_count = meta["piece_count"]

    # Tạo thư mục lưu nếu chưa có
    os.makedirs(SAVE_DIR, exist_ok=True)
    save_path = os.path.join(SAVE_DIR, file_name)

    # Tải từng mảnh
    for i in range(piece_count):
        request_piece(PEER_IP, PEER_PORT, save_path, i)

    print("All parts downloaded.")

    # Ghép lại file hoàn chỉnh
    merged_path = f"{save_path}"
    with open(merged_path, 'wb') as out:
        for i in range(piece_count):
            part_file = f"{save_path}.part{i}"
            with open(part_file, 'rb') as pf:
                out.write(pf.read())

    print(f"File merged as {merged_path}")

# Gọi hàm chính
download_from_torrent(TORRENT_PATH)
