import socket
import threading
import json
# Hàm xử lý khi nhận yêu cầu từ peer khác
import os
import sys
#---------------------- Add paths for importing ------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # Parent directory
sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)
from peer_shared.announce import announce
from peer_shared.Info_shared import TRACKER_IP, TRACKER_PORT,PIECE_SIZE
#----------------------------------------------------------------------------------#
stop_server_flag = threading.Event()
def handle_peer_request(conn, addr, file_path, total_parts,piece_length):
    """
    Hàm xử lý yêu cầu từ một peer khác.
    Có thể là yêu cầu gửi một mảnh cụ thể hoặc yêu cầu gửi danh sách các mảnh đang có.
    
    Tham số:
    - conn: đối tượng kết nối socket
    - addr: địa chỉ peer yêu cầu
    - file_path: đường dẫn tới file gốc (chưa có đuôi .partN)
    - total_parts: tổng số mảnh của file
    """
    try:
        # Nhận dữ liệu từ peer (giới hạn 1024 byte) và giải mã từ chuỗi sang JSON
        data = conn.recv(1024).decode()
        request = json.loads(data)

        # Trích ra hành động được yêu cầu, ví dụ: "bitfield", "get_piece", v.v.
        action = request.get("action")

        # Nếu peer yêu cầu "bitfield": danh sách các mảnh peer này đang có
        if action == "bitfield":
            # Bitfield là một danh sách 0/1 biểu diễn mảnh nào có (1 là có, 0 là không có)
            bitfield = []
            for index in range(total_parts):
                path_part = f"{file_path}.part{index}"  # Đường dẫn đến part của 1 file
                if os.path.exists(path_part):
                    bitfield.append(1)  # Có mảnh index  
                else:
                    bitfield.append(0) # k có mảnh index
            # Gửi bitfield dạng JSON về lại cho peer yêu cầu
            conn.sendall(json.dumps({"bitfield": bitfield}).encode()) # Dữ liệu trả về sẽ là {"bitfield": [0,0,1,0...]}
            print(f"Sent bitfield to {addr}")

        # Nếu peer yêu cầu "get_piece": tải một mảnh cụ thể theo chỉ số
        elif action == "get_piece":
            # Lấy chỉ số mảnh cần gửi
            part_index = request.get("index")

            # Tạo tên file mảnh cần đọc (ví dụ: file.txt.part3)
            part_file = f"{file_path}.part{part_index}"

            # Kiểm tra mảnh có tồn tại không
            if os.path.exists(part_file):
                # Đọc nội dung mảnh và gửi đi
                with open(part_file, 'rb') as pf:
                    part_data = pf.read()
                    conn.sendall(part_data)
                print(f"Sent part {part_index} to {addr}")
            else:
                # Nếu mảnh không tồn tại thì in ra lỗi (nhưng không crash)
                print(f"Part {part_index} not found on this peer")
        else:
            # Nếu nhận action không đúng định dạng
            print(f"Unknown action from {addr}: {action}")

    except Exception as e:
        # Bắt mọi lỗi xảy ra trong quá trình xử lý yêu cầu
        print(f"Error handling request from {addr}: {e}")

    finally:
        # Dù thành công hay lỗi, luôn đóng kết nối
        conn.close()

# Hàm khởi chạy server lắng nghe yêu cầu tải mảnh từ peer khác
def start_peer_server(port, file_path, total_parts, piece_length):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    print(f"Peer server is listening on port {port}...")

    try:
        while not stop_server_flag.is_set():
            server.settimeout(1.0)  # cho phép thoát vòng lặp mỗi 1s
            try:
                conn, addr = server.accept()
                thread = threading.Thread(
                    target=handle_peer_request, args=(conn, addr, file_path, total_parts, piece_length)
                )
                thread.start()
            except socket.timeout:
                continue
    finally:
        server.close()
        print("Peer server stopped.")
        
