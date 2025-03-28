import socket
import json

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
        port = peer["port"]
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


import socket

def request_piece(peer_ip, peer_port, file_path, index):
    """Yêu cầu một mảnh từ peer server theo đúng định dạng action/index."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Giới hạn thời gian chờ kết nối là 5 giây
            s.connect((peer_ip, peer_port))

            # Tạo chuỗi JSON thủ công và gửi đi
            request = '{"action": "get_piece", "index": ' + str(index) + '}'
            s.sendall(request.encode())

            # Nhận dữ liệu trả về
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

    except socket.timeout:
        print("Timeout when connecting to", peer_ip, peer_port, "for part", index)
    except Exception as e:
        print("Error downloading part", index, "from", peer_ip, peer_port, ":", e)

