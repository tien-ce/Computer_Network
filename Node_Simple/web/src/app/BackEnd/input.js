import { useState } from "react";

export function Input() {
    const [fileName, setFileName] = useState("");
    const [fileSize, setFileSize] = useState(288765); 
    const [pieceCount, setPieceCount] = useState(5); 
    const [fileHash, setFileHash] = useState("SHA256:MockHashForExample");
    const [pieceSize, setPieceSize] = useState(153600); 

    const createTorrentFile = () => {
        const torrentData = {
            file_name: fileName,
            file_size: fileSize,
            pieceSize: pieceSize,
            piece_count: pieceCount,
            file_hash: fileHash,
        };

        const jsonString = JSON.stringify(torrentData, null, 4);
        const blob = new Blob([jsonString], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement("a");
        link.href = url;
        link.download = `${fileName}.torrent`; 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="w-full flex flex-col items-center justify-center p-5 bg-gray-100">
            <div>
                <h2 className="text-2xl font-bold mb-6">Create a Torrent File</h2>
                <p className="flex">File Name</p>
                <input
                    type="text"
                    value={fileName}
                    onChange={(e) => setFileName(e.target.value)}
                    placeholder="File Name"
                    className="mb-4 p-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="flex">File Size</p>
                <input
                    type="number"
                    value={fileSize}
                    onChange={(e) => setFileSize(e.target.value)}
                    placeholder="File Size (bytes)"
                    className="mb-4 p-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="flex">Piece Size (bytes)</p>
                <input
                    type="number"
                    value={pieceSize}
                    onChange={(e) => setPieceSize(e.target.value)}
                    placeholder="Piece Size (bytes)"
                    className="mb-4 p-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="flex">Piece Count</p>
                <input
                    type="number"
                    value={pieceCount}
                    onChange={(e) => setPieceCount(e.target.value)}
                    placeholder="Piece Count"
                    className="mb-4 p-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="flex">File Hash</p>
                <input
                    type="text"
                    value={fileHash}
                    onChange={(e) => setFileHash(e.target.value)}
                    placeholder="File Hash"
                    className="mb-4 p-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <br></br>
                <button
                    onClick={createTorrentFile}
                    className="bg-blue-500 w-full text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Create Torrent File
                </button>
            </div>
        </div>
    );
}