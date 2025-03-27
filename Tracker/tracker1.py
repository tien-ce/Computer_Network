import socket            # Thư viện tạo kết nối mạng TCP
import threading         # Dùng để xử lý nhiều kết nối từ peer cùng lúc
import json              # Dùng để truyền nhận dữ liệu dưới dạng JSON
import time
import os
import urllib.parse
# Biến toàn cục: lưu thông tin file_hash → danh sách peer đang có file đó
# Ví dụ: { "abc123": [ {"ip": "192.168.1.2", "port": 5000}, ... ] }
file_peer_map = {}
def handle_peer(conn, addr):
    try:
        # Nhận dữ liệu từ peer
        request = conn.recv(1024).decode()
        print(f"[REQUEST] từ {addr}:\n{request}")

        # Phân tích HTTP request
        path, params = parse_http_request(request)

        # Xử lý request
        if path == "/announce":
            response = handle_announce(params)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"

        # Gửi phản hồi về peer
        conn.sendall(response.encode())

    except Exception as e:
        print(f"Lỗi xử lý peer {addr}: {e}")
    finally:
        conn.close()

def parse_http_request(request):
    """
    Phân tích HTTP request lấy đường dẫn và query string.
    """
    try:
        lines = request.split("\r\n")
        first_line = lines[0]  # GET /announce?info_hash=... HTTP/1.1
        _, path, _ = first_line.split(" ")

        # Lấy query string
        if "?" in path:
            path, query = path.split("?", 1)
        else:
            query = ""

        # Phân tích query string thành dictionary
        params = urllib.parse.parse_qs(query)

        return path, params
    except Exception as e:
        print(f"Lỗi parse request: {e}")
        return None, {}

def handle_announce(params):
    """
    Xử lý request announce từ peer.
    """
    info_hash = params.get("info_hash", [""])[0].lower()
    peer_id = params.get("peer_id", [""])[0]
    port = params.get("port", [""])[0]

    if not info_hash or not peer_id or not port:
        return "HTTP/1.1 400 Bad Request\r\n\r\nThiếu thông tin"

    # Nếu chưa có info_hash này, tạo mới danh sách
    if info_hash not in file_peer_map:
        file_peer_map[info_hash] = []

    # Thêm peer vào danh sách nếu chưa có
    new_peer = {"peer_id": peer_id, "port": port}
    if new_peer not in file_peer_map[info_hash]:
        file_peer_map[info_hash].append(new_peer)

    # Tạo response JSON danh sách peer
    response_body = json.dumps({"peers": file_peer_map[info_hash]})
    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
    
    return response
# Hàm xử lý từng kết nối đến từ peer
# def handle_peer(conn, addr):
#     print(f"[+] Kết nối mới từ {addr}")

#     try:
#         # Nhận dữ liệu từ peer (tối đa 4096 byte), và decode thành chuỗi
#         data = conn.recv(4096).decode()

#         # Giải mã chuỗi JSON thành dict Python
#         request = json.loads(data)

#         # Kiểm tra action từ peer gửi lên
#         action = request.get("action")

#         # Nếu là thông báo "announce" – peer gửi thông tin file mà nó đang có
#         if action == "announce":
#             file_hash = request.get("file_hash")      # Mã hash của file
#             peer_info = {
#                 "ip": addr[0],                        # IP của peer tự động lấy từ addr
#                 "port": request.get("port")           # Port peer gửi kèm theo
#             }

#             # Nếu chưa có file này trong hệ thống thì thêm mới
#             if file_hash not in file_peer_map:
#                 file_peer_map[file_hash] = []

#             # Nếu peer này chưa có trong danh sách, thì thêm vào
#             if peer_info not in file_peer_map[file_hash]:
#                 file_peer_map[file_hash].append(peer_info)

#             # Trả về phản hồi đơn giản
#             conn.sendall(b"Announce OK\n")

#         # Nếu peer yêu cầu "get_peers" – muốn biết ai đang có file
#         elif action == "get_peers":
#             file_hash = request.get("file_hash")          # Lấy mã hash file cần tìm
#             peer_list = file_peer_map.get(file_hash, [])  # Trả về danh sách peer nếu có

#             # Chuyển danh sách peer thành chuỗi JSON và gửi lại cho peer
#             response = json.dumps(peer_list)
#             conn.sendall(response.encode())
#         elif action == "status":
#             file_hash = request.get("file_hash")
#             peer_info = {
#                 "ip": addr[0],                        # IP của peer tự động lấy từ addr
#                 "port": request.get("port")           # Port peer gửi kèm theo
#             }
#             state = request.get("state")
#             peer_list = file_peer_map.get(file_hash, [])  # Trả về danh sách peer nếu có
#             print(file_hash + " to " + json.dumps(peer_info) + " state: "+ state)
#             response = {
#                 'action' : 'status_response',
#                 'tracker_id' : '1',
#                 'peers' : json.dumps(peer_list)
#             }
#             conn.sendall(json.dumps(response).encode('utf-8'))
#         else:
#             # Nếu action không hợp lệ
#             conn.sendall(b"Unknown action\n")

#     except Exception as e:
#         # In lỗi ra màn hình và trả về lỗi cho peer
#         print(f"[!] Lỗi xử lý peer {addr}: {e}")
#         conn.sendall(b"Tracker error occurred\n")

#     finally:
#         # Đóng kết nối với peer
#         conn.close()

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