import os
import sys
import time
import threading
#---------------------- Đây là phần add các path để import------------------------------------#
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # thư mục  cha
sys.path.append(PROJECT_ROOT)
sys.path.append(BASE_DIR)
#-------------------------------------------------------------------------------------------------#


from peer_server.peer_server import start_upload_server
# Ta cũng có sẵn hai hàm dưới đây:
# - choose_torrent_file: cho người dùng duyệt chọn file
# - parse_torrent_file: đọc file .torrent lấy thông tin
from peer_client.peer_client import start_download_from_torrent
from peer_shared.choose_file_ui import choose_torrent_file,choose_save_dir,get_user_command,get_port
from parse_torrent import parse_torrent_file
torrent_path = None

enter_event = threading.Event()

def wait_for_enter():
    """
    Luồng phụ: chờ người dùng nhấn Enter, sau đó set event.
    Dùng input() để đảm bảo tương thích tốt với mọi môi trường.
    """
    while True:
        _ = input()  # Chờ người dùng nhấn Enter
        enter_event.set()

def run_agent():
    print("Agent started. Possible commands:")
    print("  uploadfile     (to choose a .torrent file and share it)")
    print("  exit           (to exit the program)")
    print("  downloadfile   (to choose a .torrent file and download it)")
    print()
    command = None
    threading.Thread(target=wait_for_enter, daemon=True).start()
    while True:
        # Chờ Enter được nhấn
        print("Waiting for Enter to continue...")
        enter_event.wait()
        enter_event.clear()  # Đặt lại trạng thái cho lần Enter tiếp theo
        command = get_user_command()
        if not command:
            print("No command entered. Exiting.")
            break
        command = command.strip()
        if command == "uploadfile":
            # Gọi giao diện chọn file
            torrent_path = choose_torrent_file(PROJECT_ROOT)
            if not torrent_path:
                print("No .torrent file was selected.")
                continue
            # Đọc thông tin từ file .torrent
            try:
                meta = parse_torrent_file(torrent_path)
            except Exception as e:
                print("Error reading torrent file:", e)
                continue

            # Lấy ra các thông số cần thiết
            file_hash = meta["file_hash"]
            file_name = meta["file_name"]
            piece_count = meta["piece_count"]
            piece_size = meta["piece_size"]

            if not file_name:
                print("not file name")
                return
            # file gốc nằm trong thư mục file_server (Đang fix cố định dựa vào file name)
            file_path = os.path.join(PROJECT_ROOT, "file_server", file_name)
            time.sleep(0.1)
            port_str = get_port()
            if not port_str or not port_str.isdigit():
                print("Invalid port input.")
                exit()
            upload_port = int(port_str)
            start_upload_server(file_hash,file_path,piece_count,piece_size,upload_port)
            # upload_port = 5000
            # Gọi hàm khởi động server chia sẻ

        elif command == "downloadfile":
            torrent_client_path = choose_torrent_file(PROJECT_ROOT)
            save_dir = choose_save_dir(PROJECT_ROOT)
            start_download_from_torrent(torrent_client_path,save_dir)
        elif command == "exit":
            print("Shutting down agent...")
            break
        else:
            print("Invalid command. Please type 'uploadfile' or 'exit'.")
if __name__ == "__main__":
    run_agent()
