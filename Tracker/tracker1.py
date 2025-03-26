import socket            # Thư viện tạo kết nối mạng TCP
import threading         # Dùng để xử lý nhiều kết nối từ peer cùng lúc
import json              # Dùng để truyền nhận dữ liệu dưới dạng JSON
import time
import os
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
            file_hash = request.get("file_hash")      # Mã hash của file
            peer_info = {
                "ip": addr[0],                        # IP của peer tự động lấy từ addr
                "port": request.get("port")           # Port peer gửi kèm theo
            }

            # Nếu chưa có file này trong hệ thống thì thêm mới
            if file_hash not in file_peer_map:
                file_peer_map[file_hash] = []

            # Nếu peer này chưa có trong danh sách, thì thêm vào
            if peer_info not in file_peer_map[file_hash]:
                file_peer_map[file_hash].append(peer_info)

            # Trả về phản hồi đơn giản
            conn.sendall(b"Announce OK\n")

        # Nếu peer yêu cầu "get_peers" – muốn biết ai đang có file
        elif action == "get_peers":
            file_hash = request.get("file_hash")          # Lấy mã hash file cần tìm
            peer_list = file_peer_map.get(file_hash, [])  # Trả về danh sách peer nếu có

            # Chuyển danh sách peer thành chuỗi JSON và gửi lại cho peer
            response = json.dumps(peer_list)
            conn.sendall(response.encode())
        elif action == "status":
            file_hash = request.get("file_hash")
            peer_info = {
                "ip": addr[0],                        # IP của peer tự động lấy từ addr
                "port": request.get("port")           # Port peer gửi kèm theo
            }
            state = request.get("state")
            peer_list = file_peer_map.get(file_hash, [])  # Trả về danh sách peer nếu có
            print(file_hash + " to " + json.dumps(peer_info) + " state: "+ state)
            response = {
                'action' : 'status_response',
                'tracker_id' : '1',
                'peers' : json.dumps(peer_list)
            }
            conn.sendall(json.dumps(response).encode('utf-8'))
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
        print("Waiting connect")
        conn, addr = server.accept()    
        print(f"Connect from {addr}")
        # Tạo một luồng mới để xử lý peer đó
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()


def ping_client(peer_ip, peer_port):
    try:
        peer_port = int(peer_port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.connect((peer_ip, peer_port))
            print(f"Connected to {peer_ip}:{peer_port}")
            
            request = {
                'action': 'ping',
            }

            s.sendall(json.dumps(request).encode('utf-8'))
            
            response_data = s.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            if response['type'] == 'PONG':
                print('Client is working')
            else:
                print('Client is not working')
    except (socket.error, ConnectionRefusedError, TimeoutError) as e:
        print('Client is not working')
def process_input(cmd):
    params = cmd.split()

    if len(params) == 0:
        return
    try:
        if params[0] == 'ping':
            if not params[1]:
                print('Argument IP is required')
            if not params[2]:
                print('Argument PORT is required')
            ping_client(params[1], params[2])
        elif params[0] == 'discover':
            if not params[1]:
                print('Argument infohash is required')
            # get_peers_keep_file(params[1])
        elif params[0] == 'show':
            print(file_peer_map)
        else:
            print('Invalid command')
    except IndexError as e:
        print('Invalid command')
# Nếu file này được chạy trực tiếp (không phải import)
if __name__ == "__main__":
    try:
        tracker_thread = threading.Thread(target = start_tracker, daemon= True) 
        tracker_thread.start()
        time.sleep(1)
        while True:
            cmd = input('>>')
            if cmd == 'exit':
                break
            process_input(cmd)

    except KeyboardInterrupt:
        print('\nMessenger stopped by user')
    finally:
        print("Cleanup done.")