import React, { useEffect, useState } from 'react';

export function TorrentFileReader() {
    const [torrentDataArray, setTorrentDataArray] = useState([]);
    const [extractedData, setExtractedData] = useState([]);
    const [error, setError] = useState(null);
    
    const importAll = (r) => r.keys().map(r);
    const torrentFiles = importAll(require.context('./../../../../Peer-Peer/file_server', true, /\.(torrent)$/));
    
    useEffect(() => {
        const fetchTorrentData = async () => {
            const dataArr = [];

            for (const torrentFile of torrentFiles) {
                try {
                    const response = await fetch(torrentFile);
                    if (!response.ok) throw new Error('Network response was not ok');
                    const data = await response.json();
                    dataArr.push(data);
                } catch (err) {
                    console.error('Error fetching file:', err);
                    setError('Error fetching file data');
                }
            }

            setTorrentDataArray(dataArr);
            const values = extractValues(dataArr); // Gọi hàm để trích xuất giá trị
            console.log(values); // In ra kết quả trích xuất
            setExtractedData(values); // Cập nhật biến extractedData với các giá trị đã trích xuất
        };

        fetchTorrentData();
    }, [torrentFiles]);

    const extractValues = (dataArr) => {
        return dataArr.map(item => ({
            file_name: item.file_name,
            file_size: item.file_size,
            piece_count: item.piece_count,
            file_hash: item.file_hash
        }));
    };

    if (error) return <div>{error}</div>;

    return (
        <div>
            <h2>Torrent Data</h2>
            <pre>{JSON.stringify(extractedData, null, 4)}</pre> {/* Hiển thị dữ liệu đã trích xuất */}
        </div>
    );
}