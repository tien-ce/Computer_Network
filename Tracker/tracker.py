import socket            # Thư viện tạo kết nối mạng TCP
import threading         # Dùng để xử lý nhiều kết nối từ peer cùng lúc
import json              # Dùng để truyền nhận dữ liệu dưới dạng JSON
from announce import handle_announce      # Hàm dùng để thêm hash file vào list
import select 
# Biến toàn cục: lưu thông tin file_hash → danh sách peer đang có file đó
# Ví dụ: { "abc123": [ {"ip": "192.168.1.2", "port": 5000}, ... ] }
file_peer_map = {}

# Hàm xử lý từng kết nối đến từ peer
def handle_peer(conn, addr):
    print(f"[+] Kết nối mới từ {addr}")

    try:
        # Nhận dữ liệu từ peer (tối đa 4096 byte), và decode thành chuỗi
        data = conn.recv(4096).decode()

        # Giải mã chuỗi JSON thành dict Python
        request = json.loads(data)

        # Kiểm tra action từ peer gửi lên
        action = request.get("action")

        # Nếu là thông báo "announce" – peer gửi thông tin file mà nó đang có
        if action == "announce":
            file_hash = request.get("file_hash")
            port = request.get("port")
            peer_info = {
                "ip": addr[0],
                "port": port
            }
            handle_announce(file_peer_map, file_hash, peer_info)
            conn.sendall(b"Announce OK\n")

        # Nếu peer yêu cầu "get_peers" – muốn biết ai đang có file
        elif action == "get_peers":
            file_hash = request.get("file_hash")          # Lấy mã hash file cần tìm
            peer_list = file_peer_map.get(file_hash, [])  # Trả về danh sách peer nếu có

            # Chuyển danh sách peer thành chuỗi JSON và gửi lại cho peer
            response = json.dumps(peer_list)
            conn.sendall(response.encode())

        else:
            # Nếu action không hợp lệ
            conn.sendall(b"Unknown action\n")

    except Exception as e:
        # In lỗi ra màn hình và trả về lỗi cho peer
        print(f"[!] Lỗi xử lý peer {addr}: {e}")
        conn.sendall(b"Tracker error occurred\n")

    finally:
        # Đóng kết nối với peer
        conn.close()

# Hàm chính để khởi chạy tracker
def start_tracker(host="0.0.0.0", port=8000):
    # Tạo socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gán địa chỉ IP và cổng cho server
    server.bind((host, port))

    # Bắt đầu lắng nghe kết nối, tối đa 5 kết nối chờ cùng lúc
    server.listen(5)
    print(f"[TRACKER] Đang lắng nghe tại {host}:{port}")

    # Vòng lặp chấp nhận kết nối liên tục
    while True:
        # Chờ một peer mới kết nối đến
        # print("Waiting connect")
        ready_sockets, _, _ = select.select([server], [], [], 1.0)
        if server in ready_sockets:
            conn, addr = server.accept()
            print(f"Connect from {addr}")
            thread = threading.Thread(target=handle_peer, args=(conn, addr), daemon=True)
            thread.start()

# Nếu file này được chạy trực tiếp (không phải import)
if __name__ == "__main__":
    start_tracker()
