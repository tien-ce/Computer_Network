import json
def parse_torrent_file(torrent_path):
    """
    Nếu bạn dùng kiểu .torrent dạng JSON do bạn tự thiết kế,
    thì chỉ cần mở file JSON và đọc các trường cần thiết:
    file_hash, piece_count, piece_size, file_name.
    """
    with open(torrent_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    # Trả về dict
    return {
        "file_hash": meta["file_hash"],
        "file_name": meta["file_name"],
        "piece_count": meta["piece_count"],
        "piece_size": meta["piece_size"]
    }
