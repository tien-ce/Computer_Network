import Modal from "../pages/helper/modal";
import { useState, useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faBook, faList } from '@fortawesome/free-solid-svg-icons';
import $ from "jquery";
import { useLocation } from 'react-router-dom';
import PaginationHelper from "../pages/Admin/pagination";
import { Search } from "./search";
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import axios from 'axios';

export function Post() {
    const [torrentDataArray, setTorrentDataArray] = useState([]);
    const [extractedData, setExtractedData] = useState([]);
    const [error, setError] = useState(null);
    const [action, setAction] = useState(false);
    const [Use, setUse] = useState("Bulk Action");
    const [allChecked, setAllChecked] = useState(false);
    const importAll = (r) => r.keys().map(r);
    const torrentFiles = importAll(require.context('./../../../../file_server', true, /\.(torrent)$/));
    const [checkedItems, setCheckedItems] = useState(Array(torrentFiles.length).fill(false));
    const [status, setStatus] = useState('');
    
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
            const values = extractValues(dataArr);
            setExtractedData(values);
        };

        fetchTorrentData();
    }, [torrentFiles]);

    const extractValues = (dataArr) => {
        return dataArr.map(item => ({
            file_name: item.file_name,
            file_size: item.file_size,
            piece_size: item.piece_size,
            piece_count: item.piece_count,
            file_hash: item.file_hash,
        }));
    };

    if (error) return <div>{error}</div>;

    const handleCheckboxChange = (index) => {
        setCheckedItems(prevCheckedItems => {
            const newCheckedItems = [...prevCheckedItems];
            newCheckedItems[index] = !newCheckedItems[index];
            return newCheckedItems;
        });
    };

    const handleCheckAll = () => {
        const newCheckedItems = Array(torrentFiles.length).fill(!allChecked);
        setCheckedItems(newCheckedItems);
        setAllChecked(!allChecked);
    };

    const getFileNameFromPath = (path) => {
        const segments = path.split('/'); 
        return segments.pop();
    };

    const handleDownload = async (index) => {
        let torrentPath = "C:/xampp/htdocs/btl mang/Computer_Network/Node_Simple/file_server/" + extractedData[index].file_name + ".torrent";
    
        console.log(extractedData[index].file_name + ".torrent");
        setStatus('Starting download...');
        try {
            const response = await axios.post('http://127.0.0.1:5000/download', {
                torrent_path: torrentPath,
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
        <form className="container mx-auto">
            <header className="flex"><p className="text-[70px] font-serif">List Item</p></header>
            <div>
                <p className="bg-[#D9EDF7] py-[15px] pl-[15px] rounded-t-lg flex">List Items</p>
                <div className="border-x-4 border-b-4 pb-[20px] px-[20px] rounded-b-lg border-[#D9EDF7]">
                    <ul className="flex py-[20px] text-[20px] shadow-lg border rounded-t-lg ">
                        <li className="w-[2%] px-[2%]"><input type="checkbox" className="size-4 cursor-pointer" onClick={() => handleCheckAll()} /></li>
                        <li className="w-[30%] px-[2%]">Name</li>
                        <li className="w-[10%]">File Size</li>
                        <li className="w-[10%]">Piece Size</li>
                        <li className="w-[12%] px-[2%]">Piece Count</li>
                        <li className="w-[10%] px-[2%]">File Hash</li>
                        <li className="w-[10%] pl-[20%]">Status</li>
                    </ul>

                    {extractedData.map((element, index) => (
                        <ul key={index} className="flex py-[10px] text-[18px] border-b">
                            <li className="w-[2%] px-[2%]"><input type="checkbox" className="size-4 cursor-pointer" checked={checkedItems[index]} onClick={() => handleCheckboxChange(index)} /></li>
                            <li className="w-[30%] px-[2%]">{element.file_name}</li>
                            <li className="w-[10%]">{element.file_size}</li>
                            <li className="w-[10%] px-[2%]">{element.piece_size}</li>
                            <li className="w-[12%] px-[2%]">{element.piece_count}</li>
                            <li className="w-[10%] px-[2%]">{element.file_hash}</li>
                            <li className="checkbox-wrapper-8 w-[8%] ml-[18%] cursor-pointer rounded-lg flex items-center justify-center" onClick={() => handleDownload(index)}>
                                Download
                            </li>
                        </ul>
                    ))}
                </div>
            </div>
            {status && <div className="status-message">{status}</div>} {/* Hiển thị trạng thái tải xuống */}
        </form>
    );
}