import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useData } from './../helper/getData';
import Frame from '../helper/frame';
import FFrame from '../helper/frameFavorite';
import Select from 'react-select'
import { faList } from '@fortawesome/free-solid-svg-icons';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { faMinus } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import './style/style.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export const Test = (item) => {
    const { currentPage, location, images: images, childWidth, favourite } = item; 
    const [test, setTest] = useState();
    const pagination = {
        totalItems: images.length,
        totalItemsPerPage: 16,
        pageRanges: 10
    };
    const totalItems = pagination.totalItems;
    const totalItemsPerPage = pagination.totalItemsPerPage;
    const totalPages = Math.ceil(totalItems / totalItemsPerPage);
    const pageRange = pagination.pageRanges;
    let xhtmlStart = [], xhtmlNext = [], xhtmlPrevious = [], xhtmlEnd = [], xhtmlPages = [];
    const countI = Math.ceil(pageRange / 2);
    let min = currentPage - countI + 1, max = totalPages;
    const [action, setAction] = useState({ value: '1', label: 'Bán chạy nhất' });
    const [open, setOpen] = useState(true);
    const [open1, setOpen1] = useState(true);
    const Location = useLocation();
    const pathParts = Location.pathname;
    const [checkbox, setCheckbox] = useState(Array(7).fill(false));
    const [checkbox1, setCheckbox1] = useState(Array(7).fill(false));
    const listImage = [];
    const [total, setTotal] = useState(true);
    const [isVisible, setIsVisible] = useState(true);
    const lastScrollY = useRef(0);

    let linkCategory = {
        "/main": "Tất cả sản phẩm",
        "/main/Tat_ca_san_pham": "Tất cả sản phẩm",
        "/main/Lich_su_truyen_thong": "Lịch sử truyền thống",
        "/main/Van_hoc_Viet_Nam": "Văn học Việt Nam",
        "/main/Van_hoc_nuoc_ngoai": "Văn học nước ngoài",
        "/main/Kien_thuc_khoa_hoc": "Kiến thức khoa học",
        "/main/Truyen_tranh": "Truyện tranh",
        "/main/Wings_book": "Wings book",
        "/main/Favorite": "Wishlist"
    };

    const category = [
        "Tất cả",
        "Nhỏ hơn 100,000₫",
        "Từ 100,000₫ - 200,000₫",
        "Từ 200,000₫ - 300,000₫",
        "Từ 300,000₫ - 400,000₫",
        "Từ 400,000₫ - 500,000₫",
        "Lớn hơn 500,000₫"
    ];

    const value = [
        [0, 1000000000],
        [0, 100000],
        [100000, 200000],
        [200000, 300000],
        [300000, 400000],
        [400000, 500000],
        [500000, 1000000000]
    ];

    value.forEach((ele) => {
        let temp = [];
        images.forEach((element) => {
            if(Number(element.gia) >= ele[0] && Number(element.gia) <= ele[1]){
                temp.push(element);
            }
        })
        listImage.push(temp);
    })

    const handleList = (index) => {
        setCheckbox((prev) => {
            const newCheckbox = [...prev];
            const tempSet = new Set(); 
        
            if (index === 0) {
                setTotal(true);
                newCheckbox[0] = !prev[0]; 
                newCheckbox.fill(false, 1);
            } else {
                setTotal(false);
                newCheckbox[index] = !prev[index]; 
                newCheckbox[0] = false; 
                if(newCheckbox.every(item => item === false)){
                    setTotal(true);
                    newCheckbox[0] = true; 
                }
            }
        
            Object.keys(newCheckbox).forEach((key) => {
                if (newCheckbox[key]) {
                    listImage[key]?.forEach((item) => tempSet.add(item)); 
                }
            });
        
            const temp = Array.from(tempSet); 
            setTest(temp);
            
            return newCheckbox; 
        });
    };

    const handleChange = (option) => {
        setAction(option);
    };

    const handleSort = (element, index) => {
        setCheckbox1((prev) => {
            const newCheckbox = prev.map((item, i) => (i === index ? !item : false));
            const tempSet = new Set();
    
            newCheckbox.forEach((isChecked, key) => {
                if (isChecked) {
                    listImage[key]?.forEach((item) => tempSet.add(item));
                }
            });

            setAction(element);
    
            const temp = Array.from(tempSet);
            setTest(temp);
            return newCheckbox;
        });
    };

    const options = [
        { value: '1', label: 'Bán chạy nhất' },
        { value: '2', label: 'Tên A - Z' },
        { value: '3', label: 'Tên Z - A' },
        { value: '4', label: 'Giá tăng dần' },
        { value: '5', label: 'Giá giảm dần' },
        { value: '6', label: 'Mới nhất' },
        { value: '7', label: 'Cũ nhất' },
    ]
    
    const listCategory = category.map((element, index) => {
        return (
            <li
                key={index}
                onClick={() => handleList(index)}
                className="list-none pt-[10px] flex text-center cursor-pointer items-center py-[10px] pl-[10px] pr-[30px] border-b border-[#D0D1D3] hover:bg-[#F5ECD5]"
            >
                <div class="checkbox-wrapper-39">
                    <label>
                        <input 
                            name={index}
                            checked={checkbox[index] || false}
                            onChange={() => handleList(index)} 
                            className="size-5"
                            type="checkbox"/>
                        <span class="checkbox"></span>
                    </label>
                </div>
                <span className="pl-5 text-[14px]">{element}</span>
            </li>
        );
    });

    const listSort = options.map((element, index) => {
        return (
            <li
                key={index}
                onClick={() => handleSort(element ,index)}
                className="list-none pt-[10px] flex text-center cursor-pointer items-center py-[10px] pl-[10px] pr-[30px] border-b border-[#D0D1D3] hover:bg-[#F5ECD5]"
            >
                <div class="checkbox-wrapper-39">
                    <label>
                        <input 
                            name={index}
                            checked={checkbox1[index] || false}
                            onChange={() => handleSort(element, index)} 
                            className="size-5"
                            type="checkbox"/>
                        <span class="checkbox"></span>
                    </label>
                </div>
                <span className="pl-5 text-[14px]">{element.label}</span>
            </li>
        );
    });

    if (min <= 1) {
        min = 1;
    }
    max = min + pageRange;
    if (max > totalPages) {
        max = totalPages;
    }

    if (min > 1) {
        xhtmlPages.push(<li key="start-ellipsis" className="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border rounded-e-lg border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">...</li>);
    }

    let i = 1;

    if (min + countI >= totalPages) {
        i = totalPages - pageRange + 1;
    } else {
        i = min;
    }

    if (i <= 0) i = 1;

    for (i; i <= max && i <= totalPages; i++) {
        let temp = location + "/" + i;
        if (i !== currentPage) {
            xhtmlPages.push(
                <li key={i}>
                    <a href={`${temp}`} className="flex items-center justify-center p-5 m-3 h-8  leading-tight text-gray-500 bg-white border rounded-lg border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        {i}
                    </a>
                </li>
            );
        } else {
            xhtmlPages.push(
                <li key={i}>
                    <a href={`${temp}`} aria-current="page" className="flex items-center justify-center p-5 m-3 h-8  text-blue-600 border border-gray-300 rounded-lg bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white">
                        {i}
                    </a>
                </li>
            );
        }
    }

    xhtmlStart.push(<li>
        <a href={`${location}/1`} className="flex items-center max-sm:hidden justify-center p-5 m-3 h-8  leading-tight text-gray-500 bg-white border border-e-0 rounded-lg border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
            Start
        </a>
    </li>);
    xhtmlPrevious.push(<li>
        <a href={`${location}/1`} className="flex items-center justify-center p-5 m-3 h-8  leading-tight text-gray-500 bg-white rounded-lg border border-e-0 border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
            &#60;
        </a>
    </li>);


    xhtmlNext.push(<li>
        <a href={`${location}/${totalPages}`} className="flex items-center justify-center p-5 m-3 h-8 leading-tight text-white bg-black border rounded-lg border-gray-300hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
            &#62;
        </a>
    </li>);
    xhtmlEnd.push(<li>
        <a href={`${location}/${totalPages}`} className="flex max-sm:hidden items-center max-sm:hiden justify-center p-5 m-3 h-8 leading-tight text-white bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
            End
        </a>
    </li>)


    if (max < totalPages) {
        xhtmlPages.push(<li key="end-ellipsis" className='flex items-center justify-center p-5 m-3 h-8 leading-tight text-white bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'>...</li>);
    }

    if(test && test.length > 0)
        test.sort((a, b) => {
            let nameA;
            let nameB;
            if (action.value === "2" || action.value === "3") {
                nameA = a.name.toUpperCase();
                nameB = b.name.toUpperCase();
            }else if (action.value === "4" || action.value === "5"){
                nameA = Number(a.gia);
                nameB = Number(b.gia);
            }else{
                nameA = Number(a.id);
                nameB = Number(b.id);
            }
            if (action.value % 2 === 0) {
                if (nameA < nameB) {
                    return -1;
                }
                if (nameA > nameB) {
                    return 1;
                }
            }else{
                if (nameA < nameB) {
                    return 1;
                }
                if (nameA > nameB) {
                    return -1;
                }
            }
            return 0;
        });

    if(images && images.length > 0)
        images.sort((a, b) => {
            let nameA;
            let nameB;
            if (action.value === "2" || action.value === "3") {
                nameA = a.name.toUpperCase();
                nameB = b.name.toUpperCase();
            }else if (action.value === "4" || action.value === "5"){
                nameA = Number(a.gia);
                nameB = Number(b.gia);
            }else{
                nameA = Number(a.id);
                nameB = Number(b.id);
            }
            if (action.value % 2 === 0) {
                if (nameA < nameB) {
                    return -1;
                }
                if (nameA > nameB) {
                    return 1;
                }
            }else{
                if (nameA < nameB) {
                    return 1;
                }
                if (nameA > nameB) {
                    return -1;
                }
            }
            return 0;
        });
    function handleClick() {
        setOpen(!open);
    }

    function handleClick1() {
        setOpen1(!open1);
    }

    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > -200) {
                setIsVisible(true);
            } else {
                setIsVisible(false);
            }
            lastScrollY.current = window.scrollY;
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const isWishlist = linkCategory[location] === "Wishlist";
    const hasFavourites = favourite && favourite.length > 0;
    const displayItems = total ? images : test;

    return (
        <div>
            <div className={`w-[299px]  ${childWidth >= 1024 ? 'block' : 'hidden'} relative`}>
                <header className={`fixed right-[80%] transition-all duration-700 ease-in-out ${
                    lastScrollY.current <= 500 ? 'opacity-0 transform translate-y-10' :
                    lastScrollY.current <= 600 ? 'top-[45%] opacity-100 transform translate-y-0' :
                    lastScrollY.current <= 700 ? 'top-[40%] opacity-100 transform translate-y-0' :
                    lastScrollY.current <= 800 ? 'top-[30%] opacity-100 transform translate-y-0' :
                    lastScrollY.current <= 900 ? 'top-[20%] opacity-100 transform translate-y-0' :
                    'top-[10%] opacity-100 transform translate-y-0'
                }`}>     
   
                    <div className="font-medium bg-white mb-[40px]">
                        <div>
                            <p className="flex pt-[10px] pl-[10px] bg-[red] pb-[10px] relative text-[20px] items-center text-[white]">
                                Khoảng giá
                                <FontAwesomeIcon className={`text-[30px] font-bold absolute right-3 cursor-pointer `} onClick={handleClick} icon={open ? faMinus : faPlus}></FontAwesomeIcon>
                            </p>
                            <ul className={`${open ? "max-h-[400px] opacity-100" : "max-h-0 opacity-0"} transition-all duration-300 ease-in-out overflow-hidden`}>
                                {listCategory}
                            </ul>
                        </div>
                    </div>
                    <div className="font-medium bg-white">
                        <div>
                            <p className="flex pt-[10px] pl-[10px] bg-[red] pb-[10px] relative text-[20px] items-center text-[white]">
                                Sắp xếp
                                <FontAwesomeIcon className={`text-[30px] font-bold absolute right-3 cursor-pointer `} onClick={handleClick1} icon={open1 ? faMinus : faPlus}></FontAwesomeIcon>
                            </p>
                            <ul className={`${open1 ? "max-h-[400px] opacity-100" : "max-h-0 opacity-0"} transition-all duration-300 ease-in-out overflow-hidden`}>
                                {listSort}
                            </ul>
                        </div>
                    </div>
                </header>
            </div>
            <div className='2xl:w-[full] xl:w-[full] flex px-6 lg:w-[full] items-center md:w-[full]  sm:w-[full] max-sm:w-[400px] relative mb-[50px] text-[30px]'>
                {linkCategory[location]}
                <div className='absolute right-0 h-full flex items-center'>
                    <p className='text-[20px] mr-2'>Sắp xếp</p>
                    <Select
                        className='h-full text-[15px] w-[170px] border-0 focus:outline-none focus:border-0 rounded-none'
                        placeholder="Mới nhất"
                        options={options}
                        onChange={handleChange}
                    />
                </div>
            </div>
            {isWishlist ? (
                hasFavourites ? (
                    <FFrame 
                        item={displayItems} 
                        index={(currentPage - 1) * totalItemsPerPage} 
                        max_index={totalItemsPerPage} 
                        childWidth={childWidth} 
                    />
                ) : (
                    "Không có sản phẩm nào"
                )
            ) : (
                <Frame 
                    item={displayItems} 
                    index={(currentPage - 1) * totalItemsPerPage} 
                    max_index={totalItemsPerPage} 
                    childWidth={childWidth} 
                />
            )}            
            <div aria-label="Page navigation example" className='flex justify-center'>
                <ul className="inline-flex text-[30px] max-sm:text-[15px] max-sm:w-[30]">
                    {xhtmlStart}
                    {xhtmlPrevious}
                    {xhtmlPages}
                    {xhtmlNext}
                    {xhtmlEnd}
                </ul>
            </div>
        </div>

    );
}