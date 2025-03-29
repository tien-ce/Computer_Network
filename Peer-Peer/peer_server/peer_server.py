import threading
from peer_server.split_file import split_file
from peer_shared.Info_shared import TRACKER_IP,TRACKER_PORT,PIECE_SIZE
import threading
import os

def start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port):
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

    # Tính kích thước file để gửi thông tin đầy đủ cho tracker
    total_size = os.path.getsize(file_path)

    # Gửi thông báo tới tracker: peer này đã hoàn thành file, trở thành seeder
    announce(
        info_hash=file_hash,
        port=upload_port,
        event="completed",
        uploaded=0,
        downloaded=total_size,
        left=0
    )

    print(f"Announced to tracker: file_hash={file_hash}, port={upload_port}, event=completed")

    # Khởi động server chia sẻ file
    threading.Thread(
        target=start_peer_server,
        args=(upload_port, file_path, piece_count, piece_size),
        daemon=True
    ).start()

    print(f"Peer server started on port {upload_port} sharing file at {file_path}")
