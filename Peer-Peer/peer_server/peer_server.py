import threading
from peer_server.split_file import split_file
from peer_shared.Info_shared import TRACKER_IP,TRACKER_PORT,PIECE_SIZE
def start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port):
    # Gửi announce tới tracker (dùng IP và port cố định từ Info_shared)
    from peer_server.announce import announce
    from peer_server.start_and_handle_request import start_peer_server

    announce(TRACKER_IP, TRACKER_PORT, file_hash, upload_port)
    print(f"Announced to tracker: file_hash={file_hash}, port={upload_port}")

    # Khởi động peer_server chia sẻ file (dưới dạng thread)
    threading.Thread(
        target=start_peer_server,
        args=(upload_port, file_path, piece_count, piece_size),
        daemon=True
    ).start()

    print(f"Peer server started on port {upload_port} sharing file at {file_path}")
