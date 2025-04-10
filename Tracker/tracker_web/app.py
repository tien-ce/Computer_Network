from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import os
import json
import threading
import hashlib
import uuid
import time
import requests
import urllib
app = Flask(__name__)
app.config["SECRET_KEY"] = "joiafejgyinkpqhfywkndh"
app.permanent_session_lifetime = timedelta(minutes=10)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKER_DATA_FILE = os.path.join(BASE_DIR, "data/tracker_data.json")

tracker_id = "TRACKER_" + uuid.uuid4().hex[:6]

file_peer_map = {}
processing_peers = {}
PEER_TRACKERS = []
peer_tracker_lock = threading.Lock()
tracker_failures = {}
MAX_FAILURES = 5

# --------- File Handling ---------
def save_data_to_file():
    with open(TRACKER_DATA_FILE, "w") as f:
        json.dump(file_peer_map, f, indent=2)

def load_data_from_file():
    global file_peer_map
    if os.path.exists(TRACKER_DATA_FILE):
        try:
            with open(TRACKER_DATA_FILE, "r") as f:
                file_peer_map = json.load(f)
        except json.JSONDecodeError:
            file_peer_map = {}
    else:
        file_peer_map = {}

def merge_data(incoming_data):
    for info_hash, peer_list in incoming_data.items():
        if info_hash not in file_peer_map:
            file_peer_map[info_hash] = peer_list
        else:
            existing_peers = file_peer_map[info_hash]
            for peer in peer_list:
                if peer not in existing_peers:
                    existing_peers.append(peer)

def sync_from_peers_periodically(interval=10):
    def sync_loop():
        while True:
            with peer_tracker_lock:
                for url in PEER_TRACKERS[:]:
                    try:
                        res = requests.get(f"{url}/api/tracker-data", timeout=3)
                        if res.status_code == 200:
                            data = res.json()
                            peer_map = {}
                            for peer in data["peers"]:
                                info_hash = peer["info_hash"]
                                entry = {
                                    "peer_id": peer["peer_id"],
                                    "ip": peer["ip"],
                                    "port": peer["port"]
                                }
                                peer_map.setdefault(info_hash, []).append(entry)
                            merge_data(peer_map)
                            save_data_to_file()
                            tracker_failures[url] = 0  # reset nếu thành công
                    except Exception as e:
                        print(f"[ERROR] Sync from {url} failed: {e}")
                        tracker_failures[url] = tracker_failures.get(url, 0) + 1
                        if tracker_failures[url] >= MAX_FAILURES:
                            print(f"[REMOVE] Tracker {url} removed after {MAX_FAILURES} failures")
                            PEER_TRACKERS.remove(url)
                            tracker_failures.pop(url, None)
            time.sleep(interval)

    threading.Thread(target=sync_loop, daemon=True).start()


# --------- Peer Matching Helper ---------
def peer_match(p1, p2):
    return p1["peer_id"] == p2["peer_id"] and p1["ip"] == p2["ip"] and p1["port"] == p2["port"]

# --------- Tracker Routes ---------
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/processing")
def processing():
    return render_template("processing.html")
@app.route("/connect-tracker")
def connect_tracker():
    return render_template("connect_tracker.html")
@app.route("/add-tracker", methods=["POST"])
def add_tracker():
    new_url = request.form.get("tracker_url")
    if not new_url:
        return jsonify({"error": "Missing tracker URL"}), 400

    try:
        res = requests.get(f"{new_url}/api/tracker-data", timeout=3)
        if res.status_code == 200:
            with peer_tracker_lock:
                if new_url not in PEER_TRACKERS:
                    PEER_TRACKERS.append(new_url)
                    tracker_failures[new_url] = 0

            return jsonify({"message": f"Added tracker {new_url}"})
    except:
        return jsonify({"error": "Cannot connect to tracker"}), 400

@app.route("/announce")
def announce():
    info_hash_raw = request.args.get("info_hash", "").lower()
    info_hash = urllib.parse.unquote_to_bytes(info_hash_raw).hex()
    peer_id = request.args.get("peer_id", "")
    event = request.args.get("event", "")
    port = request.args.get("port", "")
    ip = request.remote_addr

    if not peer_id:
        raw = f"{ip}:{port}"
        peer_id = "PEER_" + hashlib.sha1(raw.encode()).hexdigest()[:4]

    current_peer = {"peer_id": peer_id, "ip": ip, "port": port}

    if not info_hash:
        return "Missing info_hash", 400

    peer_list = file_peer_map.get(info_hash, [])

    if event == "started":
        uploaded = request.args.get("uploaded", "")
        downloaded = request.args.get("downloaded", "")
        left = request.args.get("left", "")

        if peer_id not in processing_peers:
            processing_peers[peer_id] = {}

        processing_peer = processing_peers[peer_id]
        processing_peer[info_hash] = {
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left
        }

        return jsonify({
            "tracker": tracker_id,
            "peers": peer_list
        })

    elif event == "stopped":
        peer_list = [p for p in peer_list if not peer_match(p, current_peer)]

        if peer_list:
            file_peer_map[info_hash] = peer_list
        else:
            file_peer_map.pop(info_hash, None)  # Xóa luôn nếu danh sách rỗng

        save_data_to_file()
        return jsonify({
            "tracker": tracker_id,
            "warning": "peer removed",
            "peers": peer_list
        })

    elif event == "completed":
        # Thêm peer vào danh sách nếu chưa có
        if not any(peer_match(p, current_peer) for p in peer_list):
            peer_list.append(current_peer)
            file_peer_map[info_hash] = peer_list
            save_data_to_file()

        # Xóa peer khỏi danh sách processing nếu có
        if peer_id in processing_peers:
            processing_peers[peer_id].pop(info_hash, None)
            if not processing_peers[peer_id]:  # Nếu không còn info_hash nào đang xử lý
                del processing_peers[peer_id]

        return jsonify({
            "tracker": tracker_id,
            "warning": "peer added",
            "peers": peer_list
        })

    return jsonify({"failure reason": "Invalid event"}), 400
@app.route("/api/tracker-data")
def tracker_data():
    result = {
        "torrents": [],
        "peers": []
    }

    for info_hash, peer_list in file_peer_map.items():
        # Thêm info về từng torrent
        result["torrents"].append({
            "info_hash": info_hash,
            "peer_count": len(peer_list)
        })

        # Thêm info của các peer thuộc torrent đó
        for peer in peer_list:
            result["peers"].append({
                "peer_id": peer.get("peer_id", ""),
                "ip": peer.get("ip", ""),
                "port": peer.get("port", ""),
                "info_hash": info_hash
            })

    return jsonify(result)
@app.route("/api/processing-peers")
def api_processing_peers():
    return jsonify(processing_peers)

@app.route("/reload")
def reload_data():
    load_data_from_file()
    return jsonify({"message": "Data reloaded from file"})

# --------- App Start ---------
if __name__ == "__main__":
    load_data_from_file()
    sync_from_peers_periodically(interval=10)
    app.run(debug=True, host="0.0.0.0", port=8080)