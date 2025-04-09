import threading
from peer_shared.Info_shared import TRACKER_IP,TRACKER_PORT,PIECE_SIZE
import threading
import os
from flask import jsonify
def start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port,tracker_ip = TRACKER_IP,tracker_port = TRACKER_PORT):
    """
    Khởi động server chia sẻ file (seeder) và gửi thông báo completed tới tracker.

    Tham số:
    - file_hash: mã định danh file (chuỗi hex 40 ký tự)
    - file_path: đường dẫn tới file cần chia sẻ
    - piece_count: số lượng mảnh
    - piece_size: kích thước mỗi mảnh
    - upload_port: cổng mà peer sẽ lắng nghe
    """
    from peer_shared.announce import announce
    from peer_server.start_and_handle_request import start_peer_server

    # Bước 1: Gửi thông báo tới tracker
    total_size = os.path.getsize(file_path)
    status = announce(
        info_hash=file_hash,
        peer_id=None,
        port=upload_port,
        event="completed",
        uploaded=0,
        downloaded=total_size,
        left=0,
        tracker_ip= tracker_ip,
        tracker_port= tracker_port
    )

    # Bước 2: Kiểm tra phản hồi trước khi khởi động peer server
    if status.get("error"):
        print(f"[ERROR] Tracker announce failed: {status['error']}")
        return jsonify({"error": f"Failed to announce to tracker: {status['error']}"}), 500

    # Bước 3: Khởi động server chia sẻ file
    # threading.Thread(
    #     target=start_peer_server,
    #     args=(upload_port, file_path, piece_count, piece_size),
    #     daemon=True
    # ).start()
    start_peer_server(upload_port,file_path,piece_count,piece_size)
    return jsonify({"message": "Upload server started after successful tracker announce."}), 200


