from peer_shared.announce import announce

def get_peers(file_hash, tracker_ip, tracker_port, peer_id=None):
    """
    Gửi request announce (event=started) để lấy danh sách các peer đang giữ file.

    Tham số:
    - file_hash: mã định danh file (chuỗi hex)
    - tracker_ip: địa chỉ IP của tracker
    - tracker_port: cổng tracker
    - port: cổng mà peer này sẽ lắng nghe (để thông báo cho tracker)
    - peer_id: ID của peer, nếu không có sẽ tự sinh

    Trả về:
    - Danh sách các peer ở dạng [{"peer_id": ..., "ip": ..., "port": ...}, ...]
    """
    response = announce(
        info_hash=file_hash,
        port=None,
        peer_id=None,
        event="started",
        uploaded=0,
        downloaded=0,
        left=1048576,  # hoặc kích thước file thực tế
    )

    peers = response.get("peers", [])
    print(f"Received peers from tracker: {peers}")
    return peers
