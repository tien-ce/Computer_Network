import socket

def request_piece(peer_ip, peer_port, file_path, index):
    """Yêu cầu 1 mảnh từ peer server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer_ip, peer_port))
            s.sendall(str(index).encode())

            part_data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                part_data += chunk

        part_file = f"{file_path}.part{index}"
        with open(part_file, 'wb') as f:
            f.write(part_data)

        print(f"Downloaded part {index} and saved as {part_file}")
    except Exception as e:
        print(f"Error downloading part {index}: {e}")
