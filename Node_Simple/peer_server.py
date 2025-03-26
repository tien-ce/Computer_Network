import socket
import threading

# Hàm xử lý khi nhận yêu cầu từ peer khác
def handle_peer_request(conn, addr, file_path, total_parts):
    try:
        data = conn.recv(1024).decode()
        part_index = int(data)

        part_file = f"{file_path}.part{part_index}"
        with open(part_file, 'rb') as pf:
            part_data = pf.read()
            conn.sendall(part_data)

        print(f"Sent part {part_index} to {addr}")

    except Exception as e:
        print(f"Error handling request from {addr}: {e}")
    finally:
        conn.close()

# Hàm khởi chạy server lắng nghe yêu cầu tải mảnh từ peer khác
def start_peer_server(port, file_path, total_parts):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    print(f"Peer server is listening on port {port}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_peer_request, args=(conn, addr, file_path, total_parts)
        )
        thread.start()
