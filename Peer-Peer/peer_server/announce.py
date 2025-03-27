import socket
import json

# Hàm gửi thông báo announce đến tracker
def announce(tracker_ip, tracker_port, file_hash, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tracker_ip, tracker_port))

    # Gửi JSON chứa file_hash và cổng peer đang lắng nghe
    request = {
        "action": "announce",
        "file_hash": file_hash,
        "port": port
    }

    s.sendall(json.dumps(request).encode())
    response = s.recv(4096).decode()
    print("Tracker response:", response)
    s.close()
