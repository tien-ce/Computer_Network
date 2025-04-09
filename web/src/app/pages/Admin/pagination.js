
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBook } from '@fortawesome/free-solid-svg-icons';
import { faList } from '@fortawesome/free-solid-svg-icons';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import Modal from "../helper/modal";
import React, { useState } from 'react';
import "./style/style.css"
const PaginationHelper = ({ data = [], checkedItems, handleCheckboxChange, handleDownload, Action}) => {
    const [currentPage, setCurrentPage] = useState(1);
    const pagination = {
        totalItems: data.length,
        totalItemsPerPage: 10,
        pageRanges: 10
    };

    const totalItems = pagination.totalItems;
    const totalItemsPerPage = pagination.totalItemsPerPage;
    const totalPages = Math.ceil(totalItems / totalItemsPerPage);
    const pageRange = pagination.pageRanges;

    let xhtmlStart = [], xhtmlNext = [], xhtmlPrevious = [], xhtmlEnd = [], xhtmlPages = [];

    const countI = Math.ceil(pageRange / 2);
    let min = currentPage - countI + 1, max = totalPages;

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

    function handleClickStart(){
        setCurrentPage(1);
    }

    function handleClickPrev(){
        if(currentPage > 1){
            setCurrentPage(currentPage - 1);
        }
    }
    function handleClickEnd(){
        setCurrentPage(totalPages);
    }

    function handleClickNext(){
        if(currentPage < totalPages){
            setCurrentPage(currentPage + 1);
        }
    }

    function handleClickI(page) {
        setCurrentPage(page);
    }
    
    for (let i = 1; i <= max && i <= totalPages; i++) { 
        if (i !== currentPage) {
            xhtmlPages.push(
                <li key={i}>
                    <div 
                        onClick={() => handleClickI(i)} 
                        className="flex items-center justify-center p-5 m-3 h-8 leading-tight text-gray-500 bg-white border rounded-lg border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
                    >
                        {i}
                    </div>
                </li>
            );
        } else {
            xhtmlPages.push(
                <li key={i}>
                    <div 
                        onClick={() => handleClickI(i)}
                        aria-current="page" 
                        className="flex items-center justify-center p-5 m-3 h-8 text-blue-600 border border-gray-300 rounded-lg bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white"
                    >
                        {i}
                    </div>
                </li>
            );
        }
    }

    xhtmlStart.push(
        <li onClick={handleClickStart}>
            <div className="flex items-center max-sm:hidden justify-center p-5 m-3 h-8  leading-tight text-gray-500 bg-white border border-e-0 rounded-lg border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Start
            </div>
        </li>
    );
    xhtmlPrevious.push(
        <li onClick={handleClickPrev}>
            <div className="flex items-center justify-center p-5 m-3 h-8  leading-tight text-gray-500 bg-white rounded-lg border border-e-0 border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                &#60;
            </div>
        </li>
    );

    xhtmlNext.push(
        <li onClick={handleClickNext}>
            <div className="flex items-center justify-center p-5 m-3 h-8 leading-tight text-white bg-black border rounded-lg border-gray-300hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                &#62;
            </div>
        </li>
    );
    xhtmlEnd.push(
        <li onClick={handleClickEnd}>
            <div className="flex max-sm:hidden items-center max-sm:hiden justify-center p-5 m-3 h-8 leading-tight text-white bg-white border border-gray-300 rounded-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                End
            </div>
        </li>
    )


    if (max < totalPages) {
        xhtmlPages.push(<li key="end-ellipsis" className='flex items-center justify-center p-5 m-3 h-8 leading-tight text-white bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'>...</li>);
    }

    let index = (currentPage - 1) * totalItemsPerPage;
    let max_index = totalItemsPerPage;

    let type;

    function getData() {
        const itemsToRender = data.slice(index, index + max_index);
    
        const paddedItems = [...itemsToRender, ...Array(Math.max(0, max_index - itemsToRender.length)).fill({})];
    
        return (
            <ul>
                {paddedItems.map((element, index) => (
                    <ul key={index} className={`flex py-[10px] h-[50px] ${index % 2 === 0 ? "bg-[#E0E3E7]" : ""} text-[18px] border-b`}>
                        <li className="w-[2%] pl-[2%]">
                            {element.file_name &&  <input type="checkbox" className="size-4 cursor-pointer" checked={checkedItems[index]} onClick={() => handleCheckboxChange(index)} />} 
                        </li>
                        <li className="w-[25%]">
                            {element.file_name ? `${element.file_name}` : ''}
                        </li>
                        <li className="w-[10%]">{element.file_size || ''}</li>
                        <li className="w-[10%]">{element.piece_size || ''}</li>
                        <li className="w-[12%] px-[2%]">{element.piece_count || ''}</li>
                        <li className="w-[30%] px-[2%]">{element.file_hash || ''}</li>
                        <li className="checkbox-wrapper-8 w-[10%] cursor-pointer rounded-lg flex items-center justify-center" onClick={() => handleDownload(index)}>
                            {element.file_name &&  Action}
                        </li>
                    </ul>
                ))}
            </ul>
        );
    }

    return (
        <div className='shadow-lg rounded-lg'>
            {getData()}
            <div className='flex relative h-[70px] w-full border-t border-[#D0D1D3]'>
                <div className='flex  relative items-center text-[20px] '>
                    <p className='ml-[10px]'> Tổng số sản phẩm được tìm thấy: {data.length}</p>
                    <p className='ml-[50px]'> Active: </p>
                    <p className='ml-[50px]'> Inactive: </p>
                </div>
                <nav className='absolute right-0'>
                    <ul className="inline-flex text-[30px] max-sm:text-[15px] max-sm:w-[30]">
                        {xhtmlStart}
                        {xhtmlPrevious}
                        {xhtmlPages}
                        {xhtmlNext}
                        {xhtmlEnd}
                    </ul>
                </nav>
            </div>
        </div>
    );
}

export default PaginationHelper;
