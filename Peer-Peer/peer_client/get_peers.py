import socket
import json

def get_peers(file_hash, tracker_ip, tracker_port):
    """
    Gửi yêu cầu get_peers đến tracker để lấy danh sách các peer đang giữ file.

    Tham số:
    - file_hash: mã định danh file cần tải
    - tracker_ip, tracker_port: địa chỉ của tracker

    Trả về:
    - Danh sách các peer dạng [{"ip": ..., "port": ...}, ...]
    """
    try:
        # Tạo kết nối TCP tới tracker
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((tracker_ip, tracker_port))

            # Gửi yêu cầu dưới dạng JSON
            request_data = {
                "action": "get_peers",
                "file_hash": file_hash
            }
            s.sendall(json.dumps(request_data).encode())

            # Nhận phản hồi và giải mã
            response = s.recv(4096).decode()
            peer_list = json.loads(response)

            print(f"Received peers from tracker: {peer_list}")
            return peer_list

    except Exception as e:
        print(f"[!] Error getting peers from tracker: {e}")
        return []
