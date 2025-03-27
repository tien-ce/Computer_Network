import avt from "./image/Avatar.png";
import audience from "./image/audience.png";
import home from "./image/Home-simple-door.png";
import post from "./image/post.png";
import report from "./image/Reports.png";
import schedule from "./image/schedule.png";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import React, { useRef, useEffect, useState } from 'react';
import Radius from "./image/Radius.png";
import thang from "./image/thang.png";
import { faRightToBracket } from '@fortawesome/free-solid-svg-icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { faSquareCaretLeft } from '@fortawesome/free-solid-svg-icons';
import { faSquareCaretRight } from '@fortawesome/free-solid-svg-icons';

export function Navbar() {
    const location = useLocation();
    const [showHtml, setShowHtml] = useState(false);
    const [showHtmlBottom, setShowHtmlBottom] = useState(false);
    const pathSegments = location.pathname.split('/');
    const [isActive, setInputSegment] = useState(pathSegments[2]);
    const [open, setOpen] = useState(true);
    const divRef = useRef(null);
    const divRef1 = useRef(null);
    const divRef2 = useRef(null);

    const [height, setHeight] = useState(0);
    const [width, setWidth] = useState(0);

    const handleClick1 = () => {
        setShowHtml(!showHtml);
    };

    useEffect(() => {
        if (divRef.current) {
            const divHeight = divRef.current.offsetHeight;
            setHeight(divHeight);
        }
    }, [showHtml]);

    useEffect(() => {
        if (divRef1.current) {
            const divWidth = divRef1.current.offsetWidth;
            setWidth(divWidth);
        }
    }, [open]);

    const handleClick = () => {
        setShowHtml(!showHtml);
    };

    const handleClickBottom = () => {
        setShowHtmlBottom(!showHtmlBottom);
    };

    const handleClickOpen = () => {
        setOpen(!open);
    };

    const navigate = useNavigate();
    return (
        <div className="bg-[#161A23] z-50 h-screen">
            <div className={` ${open ? "w-[292px]" : ""}  bg-[#161A23] font-sans`}>
                <header className="relative">
                    <div className="flex mt-[20px] justify-center ">
                        <img className={`h-[50px] ${open ? "mr-7" : ""} w-[50px] object-cover" `} src={avt}></img>
                        {open && (
                            <div>
                                <p className="text-[#8A8C91] text-base">PRODUCT MANAGER</p>
                                <p className="text-white text-14">Andrew Smith</p>
                            </div>
                        )}
                        {open && (
                            <button onClick={handleClickOpen} type="button" class={`focus:outline-none absolute right-[-40px]   hover:bg-white focus:ring-white font-medium rounded-lg text-sm dark:hover:bg-white dark:focus:ring-white`}>
                                <FontAwesomeIcon className="rounded-lg m-0 p-0 size-10 " icon={faSquareCaretLeft} />
                            </button>
                        )}
                        {!open && (
                            <button onClick={handleClickOpen} type="button" class={`focus:outline-none absolute right-[-40px]   hover:bg-white focus:ring-white font-medium rounded-lg text-sm dark:hover:bg-white dark:focus:ring-white`}>
                                <FontAwesomeIcon className="rounded-lg m-0 p-0 size-10 " icon={faSquareCaretRight} />
                            </button>
                        )}
                    </div>
                    <div className="flex justify-center items-center content-center">
                        <div className="w-[80%] mt-[20px] border-b-[5px] border-[#2D2F39] rounded-full"></div>
                    </div>
                </header>
                <div ref={divRef1} className="flex pr-4">
                    <div className={`container mx-auto ${open ? "w-[110px]" : ""} text-white `}>
                        <li className="flex py-7 relative content-center">
                            <label className="hidden">Main </label>
                        </li>
                        <ul className="border-r-4 border-[#8A8C91] rounded-[50%]">
                            <li>
                                <a
                                    className={`my-1 flex py-4 w-full px-4 rounded-lg ${!open ? "cursor-pointer transition delay-150 duration-300 ease-in-out hover:scale-[1.4]": ""}`}
                                    href={`${!open ? "/admin/dashboard": ""}`}
                                >
                                    <img className="pr-4 w-[50px]" src={home}></img>
                                </a>
                            </li>
                            <li>
                                <a onClick={handleClick} className={`my-1 flex py-4 relative w-full pl-4 rounded-lg ${!open ? "cursor-pointer transition delay-150 duration-300 ease-in-out hover:scale-[1.4]": ""}`}>
                                    <img className="pr-4 w-[50px]" src={audience}></img>
                                </a>
                                {showHtml && (
                                    <div style={{ height: `${height}px` }} className={`flex w-[20px] justify-center`}>
                                    </div>
                                )}
                            </li>

                            <li>
                                <a href={`${!open ? "/admin/post": ""}`} className={`my-1 flex py-4 w-full pl-4 rounded-lg  relative ${!open ? "cursor-pointer transition delay-150 duration-300 ease-in-out hover:scale-[1.4]": ""}`}>
                                    <img className="pr-4 w-[50px] relative" src={post}></img>
                                </a>
                            </li>

                            <li >
                                <div className={`my-1} `}>
                                    <a href={`${!open ? "/admin/input": ""}`} className={`flex z-50 py-4 bg-[none] w-full pl-2 rounded-lg content-center ${!open ? "cursor-pointer transition delay-150 duration-300 ease-in-out hover:scale-[1.4]": ""}`}>
                                        <FontAwesomeIcon className="pr-4 pt-1 w-[50px] text-[35px]" icon={faRightToBracket} />
                                    </a>
                                </div>
                            </li>
                            <li>
                                <a href={`${!open ? "/admin/schedules": ""}`} className={`flex py-4 my-2 w-full pl-4 rounded-lg ${!open ? "cursor-pointer transition delay-150 duration-300 ease-in-out hover:scale-[1.4]": ""}`}>
                                    <img className="pr-4 w-[50px]" src={schedule}></img>
                                </a>
                            </li>
                            <li>
                                <div className={`flex py-4 w-full my-3 bg-[none] relative pl-4 rounded-lg cursor-pointer`} onClick={() => {
                                    handleClickBottom();
                                }}>
                                    <img className="pr-4 w-[50px]" src={report}></img>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div className={`text-white font-sans transition-all duration-700 ease-in-out`}
                        style={{
                            width: open ? `${width - 100}px` : '0px',
                            overflow: open ? '' : 'hidden',
                            opacity: open ? 10000 : 0,
                        }}>
                        <ul>
                            <li className="flex py-7 relative content-center">
                                <label className="hidden">Main </label>
                            </li>
                            <li>
                                <a
                                    href={"/admin/dashboard"}
                                    className={`my-1 flex py-5 w-full pl-4 rounded-lg hover:bg-[#2D2F39] cursor-pointer ${isActive === "dashboard" ? 'bg-[#2D2F39] text-[#62fcaf]' : ''}`}
                                >
                                    <p className="text-[20px]">Dashboard</p>
                                </a>
                            </li>
                            <li >
                                <div >
                                    <a onClick={handleClick1}  className={`my-1 flex py-5 relative w-full pl-4 rounded-lg hover:bg-[#2D2F39] cursor-pointer items-center ${showHtml ? 'bg-[#2D2F39] text-[#62fcaf]' : ''}`}>
                                        <p className="text-[20px]">Audience</p>
                                        <button className="pr-4 absolute right-0 text-sm font-medium text-gray-900 dark:text-gray-400 dark:hover:bg-black">
                                            <FontAwesomeIcon icon={showHtml ? faChevronUp : faChevronDown} />
                                        </button>
                                    </a>
                                    {showHtml && (
                                        <div ref={divRef} >
                                            <div className="flex py-2 justify-center">
                                                <img className="h-[20px] w-[20px] mr-[20px] object-cover" src={avt} alt="Avatar" />
                                                <div>
                                                    <p className="text-[#8A8C91] text-[15px]">PRODUCT MANAGER</p>
                                                    <p className="text-white text-[15px]">Andrew Smith</p>
                                                </div>
                                            </div>
                                            <div className="flex py-2 justify-center">
                                                <img className="h-[20px] w-[20px] mr-[20px] object-cover" src={avt} alt="Avatar" />
                                                <div>
                                                    <p className="text-[#8A8C91] text-[15px]">PRODUCT MANAGER</p>
                                                    <p className="text-white text-[15px]">Andrew Smith</p>
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </li>

                            <li>
                                <a href={"/admin/post"} className={`my-1 flex py-5 w-full pl-4 rounded-lg hover:bg-[#2D2F39] relative cursor-pointer ${isActive === "post" ? 'bg-[#2D2F39] text-[#62fcaf]' : ''} `}>
                                    <p className="text-[20px]">Post</p>
                                </a>
                            </li>

                            <li >
                                <a href={"/admin/input"} className={`my-1 cursor-pointer ${isActive === "input" ? 'bg-[#2D2F39] text-[#62fcaf]' : ''} `}>
                                    {isActive !== "input" && (
                                        <a className="flex py-7 bg-[none] w-full pl-4 rounded-lg content-center hover:bg-[#2D2F39] cursor-pointer">
                                            <p className="text-[20px]">Add Item</p>
                                        </a>
                                    )}
                                    {isActive === "input" && (
                                        <a onClick={() => navigate(-1)} className="flex py-7 bg-[none] w-full pl-4 rounded-lg content-center hover:bg-[#2D2F39] cursor-pointer">
                                            <p className="text-[20px]">Add Item</p>
                                        </a>
                                    )}
                                </a>
                            </li>
                            <li>
                                <a href={"/admin/schedules"} className={`my-1 flex py-4 w-full pl-4 rounded-lg hover:bg-[#2D2F39] cursor-pointer ${isActive === "schedules" ? 'bg-[#2D2F39] text-[#62fcaf]' : ''} `}>
                                    <p className="text-[20px]">Schedules</p>
                                </a>
                            </li>
                            <li>
                                <a className={`my-1 flex py-6 w-full bg-[none] relative pl-4 rounded-lg hover:bg-[#2D2F39] cursor-pointer ${showHtmlBottom ? 'bg-[#2D2F39] text-[#62fcaf]' : ''} `} onClick={() => {
                                    handleClickBottom();
                                }}>
                                    <p className="text-[20px]">Income</p>
                                    {!showHtmlBottom && (
                                        <button className="pr-4 absolute bg-[none] hover:bg-[#2D2F39] right-0 text-sm font-medium text-gray-900 dark:text-gray-400"
                                            onClick={handleClickBottom}
                                        >
                                            <FontAwesomeIcon icon={faChevronDown} />
                                        </button>
                                    )}{showHtmlBottom && (
                                        <button className="pr-4 absolute bg-[none] hover:bg-[#2D2F39] right-0 text-sm font-medium text-gray-900 dark:text-gray-400"
                                            onClick={handleClickBottom}
                                        >
                                            <FontAwesomeIcon icon={faChevronUp} />
                                        </button>
                                    )}</a>
                            </li>
                            {showHtmlBottom && (
                                <div className="flex relative ml-[20px]">
                                    <div className="overflow-hidden h-[150px]">
                                        <img src={thang} className="w-[8px]"></img>
                                    </div>
                                    <ul className="absolute">
                                        <li className="mt-[15px] flex relative">
                                            <img src={Radius} className="w-[53px]"></img>
                                            <a className="absolute left-[60px] top-[3px] rounded-lg cursor-pointer hover:bg-[#2D2F39] p-[10px]"> Earnings</a>
                                        </li>
                                        <li className="mt-[15px] flex relative">
                                            <img src={Radius} className="w-[53px]"></img>
                                            <a className="absolute left-[60px] top-[3px] rounded-lg cursor-pointer hover:bg-[#2D2F39] p-[10px]">  Refunds</a>
                                        </li>
                                        <li className="mt-[15px] flex relative">
                                            <img src={Radius} className="w-[53px]"></img>
                                            <a className="absolute left-[60px] top-[3px] rounded-lg cursor-pointer hover:bg-[#2D2F39] p-[10px]">  Declines</a>
                                        </li>
                                        <li className="mt-[15px] flex relative">
                                            <img src={Radius} className="w-[53px]"></img>
                                            <a className="absolute left-[60px] top-[3px] rounded-lg cursor-pointer hover:bg-[#2D2F39] p-[10px]">  Payouts</a>
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </ul>
                    </div>
                </div>
            </div>

        </div>
    );
}
