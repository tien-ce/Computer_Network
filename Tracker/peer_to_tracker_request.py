import requests
import urllib.parse

def send_tracker_request(tracker_url, info_hash, peer_id, port, event="started", uploaded=0, downloaded=0, left=1048576):
    """
    Gửi HTTP request đến tracker để đăng ký peer và nhận danh sách peer khác.
    
    :param tracker_url: URL của tracker (ví dụ: "http://localhost:8080/announce")
    :param info_hash: Mã hash của file torrent (20 byte, URL-encoded)
    :param peer_id: ID của peer (mỗi client có một ID duy nhất)
    :param port: Cổng mà peer sử dụng
    :param event: Sự kiện (started, stopped, completed, update)
    :param uploaded: Số byte đã upload
    :param downloaded: Số byte đã download
    :param left: Số byte còn lại cần tải về
    :return: Phản hồi JSON từ tracker (chứa danh sách peer)
    """
    
    # Chuyển đổi info_hash sang dạng URL-encoded
    info_hash_encoded = urllib.parse.quote_plus(bytes.fromhex(info_hash))

    # Tạo URL request gửi đến tracker
    params = {
        "info_hash": info_hash_encoded,
        "peer_id": peer_id,
        "port": port,
        "uploaded": uploaded,
        "downloaded": downloaded,
        "left": left,
        "event": event
    }

    # Gửi request đến tracker
    try:
        response = requests.get(tracker_url, params=params)
        if response.status_code == 200:
            return response.json()  # Trả về danh sách peer
        else:
            return {"error": f"Tracker không phản hồi, mã lỗi {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Ví dụ sử dụng hàm
tracker_url = "http://localhost:8000/announce"
info_hash = "abcdef123456abcdef123456abcdef123456abcdef12"  # Ví dụ hash của torrent
peer_id = "-PC0001-123456789012"
port = 6881

result = send_tracker_request(tracker_url, info_hash, peer_id, port)
print("Phản hồi từ tracker:", result)
