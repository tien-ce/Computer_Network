import socket
import urllib.parse
import uuid  # để tạo peer_id ngẫu nhiên
# Hàm gửi thông báo announce đến tracker
def announce(tracker_ip, tracker_port, file_hash, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tracker_ip, tracker_port))

    peer_id = str(uuid.uuid4())  # hoặc bạn có thể tạo peer_id cố định

    # Tạo URL với query string
    query_params = urllib.parse.urlencode({
        "info_hash": file_hash,
        "peer_id": peer_id,
        "port": port
    })

    request = (
        f"GET /announce?{query_params} HTTP/1.1\r\n"
        f"Host: {tracker_ip}:{tracker_port}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    s.sendall(request.encode())

    response = s.recv(4096).decode()
    print("Tracker response:", response)
    s.close()
