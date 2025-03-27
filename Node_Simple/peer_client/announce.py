import socket
import json

def announce_to_tracker(file_hash, port, tracker_ip, tracker_port):
    """
    Gửi thông báo 'announce' đến tracker để báo rằng peer này đang chia sẻ file nào.
    
    Tham số:
    - file_hash: mã hash định danh file đang chia sẻ
    - port: cổng mà peer server đang mở để cho tải
    - tracker_ip, tracker_port: địa chỉ của tracker
    """
    try:
        # Tạo socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Kết nối đến tracker
            s.connect((tracker_ip, tracker_port))

            # Tạo nội dung gói tin gửi đi
            request_data = {
                "action": "announce",
                "file_hash": file_hash,
                "port": port
            }

            # Gửi dữ liệu dưới dạng JSON
            s.sendall(json.dumps(request_data).encode())

            # Nhận phản hồi từ tracker
            response = s.recv(4096).decode()
            print("Tracker response:", response)
    except Exception as e:
        print(f"[!] Connection error to tracker: {e}")
