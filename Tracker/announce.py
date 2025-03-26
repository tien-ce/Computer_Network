def handle_announce(file_peer_map: dict, file_hash: str, peer_info: dict) -> None:
    """
    Hàm xử lý yêu cầu 'announce' từ node gửi tới tracker.

    Tham số:
    - file_peer_map: từ điển lưu thông tin các file và danh sách các peer tương ứng
        (ví dụ: { "abc123": [{"ip": "...", "port": ...}, ...] })
    - file_hash: mã định danh duy nhất của file mà node thông báo đang sở hữu
    - peer_info: thông tin của peer gồm 'ip' và 'port' mà nó sử dụng để chia sẻ file

    Trả về:
    - None. Hàm này sẽ cập nhật trực tiếp vào file_peer_map (tham chiếu).
    """

    # Nếu file_hash chưa tồn tại trong hệ thống thì tạo mới danh sách peer
    if file_hash not in file_peer_map:
        file_peer_map[file_hash] = []

    # Kiểm tra nếu peer chưa có trong danh sách thì thêm vào
    if peer_info not in file_peer_map[file_hash]:
        file_peer_map[file_hash].append(peer_info)
        print(f"[Tracker] Added new peer for file {file_hash}: {peer_info}")
    else:
        print(f"[Tracker] Peer already registered for file {file_hash}.")
