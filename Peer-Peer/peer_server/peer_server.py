import threading
from peer_shared.Info_shared import TRACKER_IP,TRACKER_PORT,PIECE_SIZE
import threading
import os
from flask import jsonify
import signal
import sys
import time
# Biến toàn cục để truyền info cần thiết cho stop
global_file_hash = None
global_upload_port = None
global_tracker_ip = None
global_tracker_port = None

def signal_handler(sig, frame):
    print("Shutting down, notifying tracker...")

    if global_file_hash and global_upload_port:
        stop_upload_server(global_file_hash, global_upload_port, global_tracker_ip, global_tracker_port)

    time.sleep(1)  # Đảm bảo đủ thời gian gửi announce
    sys.exit(0)

# Đăng ký signal handler
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # kill

#---------------------- Add paths for importing ------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # Parent directory
sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)
from peer_shared.announce import announce
from peer_shared.Info_shared import TRACKER_IP, TRACKER_PORT,PIECE_SIZE
#----------------------------------------------------------------------------------#
stop_server_flag = threading.Event()
def start_upload_server(file_hash, file_path, piece_count, piece_size, upload_port, tracker_ip=TRACKER_IP, tracker_port=TRACKER_PORT):
    from peer_shared.announce import announce
    from peer_server.start_and_handle_request import start_peer_server
    global global_file_hash, global_upload_port, global_tracker_ip, global_tracker_port

    # Gửi announce completed
    total_size = os.path.getsize(file_path)
    status = announce(
        info_hash=file_hash,
        peer_id=None,
        port=upload_port,
        event="completed",
        uploaded=0,
        downloaded=total_size,
        left=0,
        tracker_ip=tracker_ip,
        tracker_port=tracker_port
    )

    if status.get("error"):
        print(f"[ERROR] Tracker announce failed: {status['error']}")
        return jsonify({"error": f"Failed to announce to tracker: {status['error']}"}), 500

    # Gán thông tin cho signal handler
    global_file_hash = file_hash
    global_upload_port = upload_port
    global_tracker_ip = tracker_ip
    global_tracker_port = tracker_port

    # Khởi động server
    threading.Thread(
        target=start_peer_server,
        args=(upload_port, file_path, piece_count, piece_size),
        daemon=True
    ).start()

    return jsonify({"message": "Upload Completed."}), 200

def stop_upload_server(file_hash, upload_port, tracker_ip=TRACKER_IP, tracker_port=TRACKER_PORT):
    """
    Dừng peer server và thông báo đến tracker với event 'stopped'
    """
    stop_server_flag.set()  # Dừng vòng lặp trong start_peer_server
    print("[DEBUG] Calling announce with event=stopped")
    try:
        announce(
            info_hash=file_hash,
            peer_id=None,
            port=upload_port,
            event="stopped",
            uploaded=0,
            downloaded=0,
            left=0,
            tracker_ip=tracker_ip,
            tracker_port=tracker_port
        )
        print("[INFO] Sent 'stopped' event to tracker.")
    except Exception as e:
        print(f"[ERROR] Failed to notify tracker: {str(e)}")
