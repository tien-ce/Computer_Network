import socket
import urllib.parse
import json
def get_peers(file_hash, tracker_ip, tracker_port):
    """
    Gửi yêu cầu GET đến tracker để lấy danh sách các peer đang giữ file.

    Tham số:
    - file_hash: mã định danh của file cần tải (chuỗi)
    - tracker_ip: địa chỉ IP của tracker
    - tracker_port: cổng mà tracker đang lắng nghe

    Trả về:
    - Danh sách các peer ở dạng [{"peer_id": ..., "port": ...}, ...]
    """

    try:
        # Tạo socket TCP để kết nối tới tracker
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Thiết lập kết nối đến tracker qua IP và port
            s.connect((tracker_ip, tracker_port))

            # Tạo chuỗi truy vấn (query string) cho HTTP GET
            query_params = urllib.parse.urlencode({
                "info_hash": file_hash
            })

            # Tạo HTTP GET request để gửi lên tracker
            request = (
                f"GET /get_peers?{query_params} HTTP/1.1\r\n"
                f"Host: {tracker_ip}:{tracker_port}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )

            # Gửi request lên tracker
            s.sendall(request.encode())

            # Nhận phản hồi từ tracker (dưới dạng chuỗi)
            response = s.recv(4096).decode()

            # Tách phần thân (body) của HTTP response ra khỏi phần header
            body = response.split("\r\n\r\n", 1)[-1]

            # Chuyển phần thân từ chuỗi JSON thành danh sách Python
            peer_list = json.loads(body)

            # In ra kết quả để kiểm tra
            print(f"Received peers from tracker: {peer_list}")

            # Trả về danh sách các peer
            return peer_list

    except Exception as e:
        # Nếu có lỗi, in thông báo và trả về danh sách rỗng
        print(f"[!] Error getting peers from tracker: {e}")
        return []