import { useState } from 'react';
import React from 'react';
import axios from 'axios';

export function Home() {
    const [peerPort, setPeerPort] = useState('');
    const [fileHash, setFileHash] = useState('');
    const [status, setStatus] = useState('');

    const handleJoin = async () => {
        setStatus('Starting join process...');
        try {
            const response = await axios.post('http://127.0.0.1:5000/join', {
                peer_port: parseInt(peerPort),
            });
            setStatus(response.data.message);
            window.location.href = "http://localhost:3000/admin/post";
        } catch (error) {
            if (error.response) {
                setStatus(error.response.data.error);
            } else {
                setStatus('Error: ' + error.message);
            }
        }
    };

    const handleDownload = async () => {
        setStatus('Starting download...');
        try {
            const response = await axios.post('http://127.0.0.1:5000/download', {
                // Gửi yêu cầu tải file nếu cần
            });
            setStatus(response.data.message);
        } catch (error) {
            if (error.response) {
                setStatus(error.response.data.error);
            } else {
                setStatus('Error: ' + error.message);
            }
        }
    };

    const handleDelete = async () => {
        setStatus('Deleting file...');
        try {
            const response = await axios.post('http://127.0.0.1:5000/delete', {
                file_hash: fileHash,
            });
            setStatus(response.data.message);
        } catch (error) {
            if (error.response) {
                setStatus(error.response.data.error);
            } else {
                setStatus('Error: ' + error.message);
            }
        }
    };
    return (
        <div className="h-screen flex justify-center items-center bg-gray-100">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-2xl font-bold mb-4 text-center">Join Tracker</h2>
                <input
                    type="number"
                    placeholder="Enter peer port"
                    value={peerPort}
                    onChange={(e) => setPeerPort(e.target.value)}
                    className="border border-gray-300 rounded-lg p-2 w-full mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    onClick={handleJoin}
                    className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Join
                </button>

                {status && <p className="mt-4 text-center text-green-600">{status}</p>}
            </div>
        </div>
    );
}