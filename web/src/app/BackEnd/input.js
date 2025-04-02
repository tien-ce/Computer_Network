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

export function Input() {
    const [torrentDataArray, setTorrentDataArray] = useState([]);
    const [extractedData, setExtractedData] = useState([]);
    const [error, setError] = useState(null);
    const [action, setAction] = useState(false);
    const [Use, setUse] = useState("Bulk Action");
    const [allChecked, setAllChecked] = useState(false);
    const importAll = (r) => r.keys().map(r);
    const torrentFiles = importAll(require.context('./../../../../Peer-Peer/file_server', true, /\.(torrent)$/));
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
        return dataArr.map((item, index)=> ({
            id: index,
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
        let torrentPath = "D:/btl mang/Computer_Network/Peer-Peer/file_server/" + extractedData[index].file_name + ".torrent";
        setStatus('Starting Upload...');
        try {
            const response = await axios.post('http://127.0.0.1:5000/input', {
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

    function handleAction() {
        setAction(!action);
    }

    const [input, SecrchResult, results] = Search(extractedData, checkedItems, handleCheckboxChange, handleDownload, "Upload");

    return (
        <form className="container mx-auto">
            <header className="flex"><p className="text-[70px] font-serif">List Item</p></header>
            <div>
                <p className="bg-[#D9EDF7] py-[15px] pl-[15px] rounded-t-lg flex">List Items</p>
                <div className="border-x-4 border-b-4 pb-[20px] px-[20px] rounded-b-lg border-[#D9EDF7]">
                <div className="flex h-[80px] items-center relative ">
                        <div className={`flex w-[114px] h-[40px] items-center cursor-pointer transition-transform absolute duration-700 ease-in-out ${action ? "translate-x-[115px] hover:scale-110 " : "-translate-x-[0px] "}`} >
                            <p href="/admin/post/All" className="w-[100px] m-[10px] z-0 flex h-full justify-center items-center text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
                                All
                            </p>
                        </div>
                        <div className={`flex w-[114px] h-[40px] items-center cursor-pointer transition-transform absolute duration-700 ease-in-out ${action ? "translate-x-[230px] hover:scale-110 " : "-translate-x-[0px] "}`} >
                            <p className="w-[100px] m-[10px] z-0 flex h-full justify-center items-center text-gray-900 bg-gradient-to-r from-lime-200 via-lime-400 to-lime-500 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-lime-300 dark:focus:ring-lime-800 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
                                Active
                            </p>
                        </div>
                        <div className={`flex w-[114px] h-[40px] cursor-pointer items-center transition-transform absolute duration-700 ease-in-out ${action ? "translate-x-[345px] hover:scale-110 " : "-translate-x-[0px]"}`} >
                            <p className={`w-[100px] m-[10px] z-0 flex h-full justify-center items-center text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 shadow-lg shadow-red-500/50 dark:shadow-lg dark:shadow-red-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2`}>
                                InActive
                            </p>
                        </div>
                        <div className={`flex w-[114px] h-[40px] cursor-pointer items-center transition-transform absolute duration-700 ease-in-out ${action ? "translate-x-[460px] hover:scale-110 " : "-translate-x-[0px]"} `} >
                            <p className={`w-[100px] m-[10px] z-0 flex h-full justify-center items-center focus:outline-none text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2`}>
                                Edit
                            </p>
                        </div>
                        <div className={`flex w-[114px] h-[40px] cursor-pointer items-center transition-transform absolute duration-700 ease-in-out ${action ? "translate-x-[575px] hover:scale-110" : "-translate-x-[0px]"}`} >
                            <p className={`w-[100px] m-[10px] z-0 flex h-full justify-center items-center focus:outline-none text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l focus:ring-4 focus:ring-purple-200 dark:focus:ring-purple-800 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2`}>
                                Delete
                            </p>
                        </div>
                        <div className={`flex w-[114px] h-[40px] cursor-pointer items-center transition-transform absolute duration-700 ease-in-out ${!action ? "translate-x-[115px] hover:scale-110" : "-translate-x-[0px]"}`} >
                            <p className={`w-[100px] m-[10px] z-0 flex h-full justify-center items-center focus:outline-none text-white bg-gradient-to-r from-pink-400 via-pink-500 to-pink-600 hover:bg-gradient-to-br focus:ring-4 focus:ring-pink-300 dark:focus:ring-pink-800 shadow-lg shadow-pink-500/50 dark:shadow-lg dark:shadow-pink-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2`}>
                                Apply
                            </p>
                        </div>
                        <div className={`hover:scale-110 m-[10px] h-[42px]  w-[100px] flex relative cursor-pointer items-center justify-center  ${Use === "Bulk Action" && "text-white bg-gradient-to-r from-purple-500 via-purple-600 to-purple-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-purple-300 dark:focus:ring-purple-800 shadow-lg shadow-purple-500/50 dark:shadow-lg dark:shadow-purple-800/80 font-medium rounded-lg text-sm  text-center "}
                                                                                                                                            ${Use === "Active" && "text-gray-900 bg-gradient-to-r from-lime-200 via-lime-400 to-lime-500 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-lime-300 dark:focus:ring-lime-800 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"}
                                                                                                                                            ${Use === "InActive" && "text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 shadow-lg shadow-red-500/50 dark:shadow-lg dark:shadow-red-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"}
                                                                                                                                            ${Use === "Edit" && "text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"}
                                                                                                                                            ${Use === "Delete" && "text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l focus:ring-4 focus:ring-purple-200 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"}
                                                                                                                                            ${Use === "All" && "text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 shadow-lg shadow-lime-500/50 dark:shadow-lg dark:shadow-lime-800/80 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2"}
                        `} onClick={handleAction}>
                            <p>{Use}</p>
                        </div>
                        <div
                            className={`w-[1000px] items-center justify-center flex transition-opacity duration-300 ease-in-out ${
                                !action ? 'opacity-100' : 'opacity-0 pointer-events-none'
                            }`}
                            >
                        {input}
                        </div>
                    </div>
                    <ul className="flex py-[20px] text-[20px] shadow-lg border rounded-t-lg ">
                        <li className="w-[2%] pl-[2%]"><input type="checkbox" className="size-4 cursor-pointer" onClick={() => handleCheckAll()} /></li>
                        <li className="w-[25%]">Name</li>
                        <li className="w-[10%]">File Size</li>
                        <li className="w-[10%]">Piece Size</li>
                        <li className="w-[12%] px-[2%]">Piece Count</li>
                        <li className="w-[30%] px-[2%]">File Hash</li>
                        <li className="w-[10%]">Action</li>
                    </ul>

                    {results.length > 0 ? SecrchResult : 
                        <PaginationHelper
                            data={extractedData}
                            checkedItems={checkedItems}
                            handleCheckboxChange={handleCheckboxChange}
                            handleDownload={handleDownload}
                            Action="Upload"
                        />
                    }
                </div>
            </div>
            {status && <div className="status-message">{status}</div>} 
        </form>
    );
}