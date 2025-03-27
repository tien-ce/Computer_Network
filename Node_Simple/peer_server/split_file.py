import os
import hashlib
import json

def split_file(file_path, piece_size):
    """
    Chia một file thành nhiều phần nhỏ có kích thước cố định.
    Tự động tạo file metainfo (.torrent) chứa thông tin về file đã chia.
    Trả về số lượng mảnh đã tạo.
    """

    # Mở file gốc để chia nhỏ
    with open(file_path, 'rb') as f:
        index = 0
        while True:
            chunk = f.read(piece_size)
            if not chunk:
                break

            part_file = f"{file_path}.part{index}"
            with open(part_file, 'wb') as pf:
                pf.write(chunk)

            print(f"Saved part {index} with {len(chunk)} bytes")
            index += 1

    total_parts = index
    print(f"Total parts: {total_parts}")

    # Tính hash toàn bộ file để tạo file_hash
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha1.update(data)
    file_hash = sha1.hexdigest()

    # Ghi thông tin vào file metainfo (.torrent)
    metainfo = {
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "piece_size": piece_size,
        "piece_count": total_parts,
        "file_hash": file_hash
    }

    torrent_path = f"{file_path}.torrent"
    with open(torrent_path, 'w') as f:
        json.dump(metainfo, f, indent=2)

    print(f"Metainfo saved to {torrent_path}")
    return total_parts
