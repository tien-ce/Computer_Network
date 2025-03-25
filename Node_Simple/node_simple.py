import socket   # Thư viện socket để kết nối TCP
import json     # Định dạng dữ liệu kiểu JSON

# --- Cấu hình kết nối tới tracker ---
TRACKER_IP = "10.229.188.6"   # IP của máy chạy tracker (bạn đã cung cấp)
TRACKER_PORT = 8000           # Port tracker đang mở (mặc định mình dùng 8000)

# --- Tạo socket TCP ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# --- Kết nối tới tracker ---
try:
    print(f"[+] Kết nối tới tracker tại {TRACKER_IP}:{TRACKER_PORT}")
    client.connect((TRACKER_IP, TRACKER_PORT))  # Kết nối TCP tới tracker

    # --- Tạo request kiểu announce ---
    request_data = {
        "action": "announce",          # Hành động muốn gửi tới tracker
        "file_hash": "abc123",         # Giả định: peer đang giữ file có hash abc123
        "port": 5000                   # Cổng mà peer sẽ mở để chia sẻ (giả sử)
    }

    # --- Gửi request (chuyển thành JSON rồi encode) ---
    client.sendall(json.dumps(request_data).encode())

    # --- Nhận phản hồi từ tracker ---
    response = client.recv(4096).decode()
    print(f"[Tracker Phản hồi] {response}")

except Exception as e:
    print(f"[!] Lỗi khi kết nối tracker: {e}")

finally:
    client.close()  # Đóng kết nối sau khi xong
