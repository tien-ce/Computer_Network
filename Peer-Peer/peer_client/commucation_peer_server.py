import socket
import json
import os
def count_downloaded_pieces(file_path, piece_count):
    """
    Đếm số lượng mảnh đã tồn tại trên đĩa.

    Tham số:
    - file_path: đường dẫn file tạm (không gồm đuôi .partX)
    - piece_count: tổng số mảnh

    Trả về:
    - Số mảnh đã có
    """
    count = 0
    for i in range(piece_count):
        if os.path.exists(f"{file_path}.part{i}"):
            count += 1
    return count

def get_bitfields(peers, total_parts, timeout=3):
    """
    Kết nối đến từng peer và yêu cầu 'bitfield' để biết peer đó có những mảnh nào.
    
    Tham số:
    - peers: danh sách các peer, mỗi peer là dict {"ip": ..., "port": ...}
    - total_parts: tổng số mảnh của file
    - timeout: thời gian chờ kết nối (giây)

    Trả về:
    - Dictionary dạng {(ip, port): [0,1,0,...]} thể hiện các mảnh peer đó đang giữ
    """
    bitfields = {}

    for peer in peers:
        ip = peer["ip"]
        port = int(peer["port"])
        try:
            # Tạo kết nối TCP đến peer
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))

                # Gửi yêu cầu 'bitfield'
                request = {
                    "action": "bitfield"
                }
                s.sendall(json.dumps(request).encode())

                # Nhận phản hồi
                response = s.recv(4096).decode()
                data = json.loads(response)
                bitfield = data.get("bitfield", [])

                # Kiểm tra độ dài bitfield có khớp không
                if len(bitfield) != total_parts:
                    print(f"Warning: Bitfield from {ip}:{port} has wrong length.")
                    continue

                # Lưu vào dict với key là (ip, port)
                bitfields[(ip, port)] = bitfield
                print(f"Received bitfield from {ip}:{port}: {bitfield}")

        except Exception as e:
            print(f"[!] Failed to get bitfield from {ip}:{port} → {e}")

    return bitfields



def request_piece(peer_ip, peer_port, file_path, index, file_hash, peer_id, total_pieces, piece_size):
    """
    Yêu cầu một mảnh từ peer server và thông báo cho tracker sau khi tải thành công.

    Tham số:
    - peer_ip, peer_port: địa chỉ peer đang giữ mảnh
    - file_path: đường dẫn file tạm để lưu mảnh
    - index: chỉ số mảnh cần tải
    - file_hash: mã định danh file
    - tracker_ip, tracker_port: địa chỉ tracker để gửi thông báo update
    - peer_id: mã định danh peer hiện tại
    - total_pieces, piece_size: để tính kích thước và tiến độ
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((peer_ip, peer_port))
            request = '{"action": "get_piece", "index": ' + str(index) + '}'
            s.sendall(request.encode())

            part_data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                part_data += chunk

        if not part_data:
            print("Empty response from", peer_ip, peer_port, "for part", index)
            return

        part_file = f"{file_path}.part{index}"
        with open(part_file, 'wb') as f:
            f.write(part_data)

        print("Downloaded part", index, "from", peer_ip, peer_port)

        # Gửi thông báo "update" cho tracker
        from peer_shared.announce import announce
        downloaded = count_downloaded_pieces(file_path,total_pieces)
        left = max((total_pieces - index - 1) * piece_size, 0)
        announce(
            peer_id = peer_id,
            info_hash=file_hash,
            port=peer_port,
            event="update",
            uploaded=0,
            downloaded=downloaded,
            left=left,
        )

    except socket.timeout:
        print("Timeout when connecting to", peer_ip, peer_port, "for part", index)
    except Exception as e:
        print("Error downloading part", index, "from", peer_ip, peer_port, ":", e)
