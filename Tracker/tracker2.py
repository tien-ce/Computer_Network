import socket
import threading
import json
import time

# Danh sách các peer theo info_hash
peers = {}

# Hàm xử lý request từ client
def handle_client(client_socket):
    try:
        # Nhận request từ client (dữ liệu HTTP GET)
        request = client_socket.recv(1024).decode('utf-8')
        print(f"📥 Request nhận được:\n{request}")

        # Tách request để lấy phần URL
        lines = request.split("\r\n")
        first_line = lines[0]  # GET /announce?info_hash=... HTTP/1.1
        if "GET" not in first_line:
            return

        # Lấy phần query từ URL
        url = first_line.split(" ")[1]
        if not url.startswith("/announce"):
            return

        # Parse query string để lấy tham số
        query_params = {}
        if "?" in url:
            query_string = url.split("?")[1]
            params = query_string.split("&")
            for param in params:
                key, value = param.split("=")
                query_params[key] = value

        # Lấy thông tin quan trọng
        info_hash = query_params.get("info_hash", "")
        peer_id = query_params.get("peer_id", "")
        ip = client_socket.getpeername()[0]  # Lấy IP từ kết nối
        port = int(query_params.get("port", 6881))
        event = query_params.get("event", "")

        # Thêm peer vào danh sách nếu chưa có
        if info_hash not in peers:
            peers[info_hash] = []

        # Xử lý các sự kiện từ client
        if event == "started":
            # Thêm peer vào danh sách
            peers[info_hash].append({"ip": ip, "port": port, "peer_id": peer_id})
        elif event == "stopped":
            # Xóa peer khi client dừng
            peers[info_hash] = [p for p in peers[info_hash] if p["peer_id"] != peer_id]

        # Tạo response JSON
        response_data = {
            "interval": 1800,  # Client nên gửi request mỗi 30 phút
            "complete": len([p for p in peers[info_hash] if p["peer_id"] == peer_id]),
            "incomplete": len(peers[info_hash]),
            "peers": peers[info_hash]
        }
        response_json = json.dumps(response_data)

        # Gửi response HTTP
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: {}\r\n"
            "\r\n"
            "{}"
        ).format(len(response_json), response_json)
        client_socket.sendall(http_response.encode('utf-8'))

    except Exception as e:
        print(f"❌ Lỗi xử lý request: {e}")

    finally:
        client_socket.close()  # Đóng kết nối sau khi xử lý xong

# Hàm chạy server tracker
def start_tracker(host="0.0.0.0", port=8000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"🚀 Tracker đang chạy trên {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"🔗 Kết nối từ {addr}")

        # Xử lý request trong luồng riêng
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Chạy tracker trong luồng riêng
if __name__ == "__main__":
    tracker_thread = threading.Thread(target=start_tracker, args=("0.0.0.0", 8000), daemon=True)
    tracker_thread.start()

    # Vòng lặp chờ lệnh từ admin
    while True:
        cmd = input(">> ")
        if cmd == "exit":
            print("🛑 Dừng tracker...")
            break
        elif cmd == "show":
            print(json.dumps(peers, indent=4))  # Hiển thị danh sách peer hiện tại
