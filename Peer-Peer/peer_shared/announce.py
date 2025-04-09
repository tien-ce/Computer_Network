import socket
import urllib.parse
import uuid
import json
from peer_shared.Info_shared import TRACKER_IP,TRACKER_PORT,PIECE_SIZE
def announce(info_hash,peer_id, port, event="started", uploaded=0, downloaded=0, left=None,tracker_ip = TRACKER_IP,tracker_port = TRACKER_PORT):
    """
    Gửi HTTP GET request đến tracker để thông báo trạng thái của peer và nhận danh sách peer khác.

    Tham số:
    - tracker_ip: Địa chỉ IP của tracker
    - tracker_port: Cổng của tracker
    - info_hash: Mã hash (chuỗi hex 40 ký tự) đại diện cho file torrent
    - port: Cổng mà peer đang sử dụng để chờ kết nối từ peer khác
    - event: Trạng thái hiện tại của peer (started, completed, stopped, update)
    - uploaded: Số byte đã upload lên mạng
    - downloaded: Số byte đã tải về
    - left: Số byte còn lại cần tải về

    Trả về:
    - Từ điển chứa danh sách các peer hoặc thông báo lỗi nếu có
    """

    try:
        # Tạo peer_id ngẫu nhiên
        peer_id = str(uuid.uuid4())

        # Chuyển info_hash sang dạng byte, sau đó URL-encode
        info_hash_bytes = bytes.fromhex(info_hash)
        info_hash_encoded = urllib.parse.quote_plus(info_hash_bytes)

        # Tạo chuỗi truy vấn gửi lên tracker
        query_params = urllib.parse.urlencode({
            "info_hash": info_hash_encoded,
            "peer_id": peer_id,
            "port": port,
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left,
            "event": event
        })

        # Tạo HTTP GET request theo đúng định dạng
        request = (
            f"GET /announce?{query_params} HTTP/1.1\r\n"
            f"Host: {tracker_ip}:{tracker_port}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )

        # Tạo kết nối TCP tới tracker
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((tracker_ip, tracker_port))
            s.sendall(request.encode())

            # Nhận toàn bộ phản hồi từ tracker
            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk

        # Tách phần header và body trong phản hồi HTTP
        response_str = response_data.decode()
        _, _, body = response_str.partition("\r\n\r\n")

        # Giải mã chuỗi JSON từ phần body
        try:
            json_data = json.loads(body)
            print("Tracker response (JSON):", json_data)
            return json_data
        except json.JSONDecodeError:
            print("Tracker response (Raw):", response_str)
            return {"error": "Invalid JSON format from tracker"}

    except Exception as e:
        print("Tracker communication error:", str(e))
        return {"error": str(e)}
