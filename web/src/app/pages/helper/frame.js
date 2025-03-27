import './style/frame.css';
import React, { useRef, useEffect, useState } from 'react';

const Frame = ({ item, index, max_index, childWidth }) => {
    let totalView = [];
    let oneView = [];

    function formatPrice(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + 'đ';
    }

    const getImg = (img) => {
        const result = img.filter(ele => {
            const fileName = ele.split('/');
            const pathParts = fileName[fileName.length - 1].split("_");
            return pathParts.includes("0");
        });
        return result;
    };

    let count = 0;

    if (childWidth < 640) {
        count = 2;
    } else if (childWidth < 1280) {
        count = 3;
    } else if (childWidth < 1600) {
        count = 4;
    } else {
        count = 4;
    }

    const view = item.slice(index, index + max_index).map((element, idx) => {
        const imgs = getImg(element.img);
        if (idx % count === 0 && idx !== 0) {
            totalView.push(
                <ul className='flex w-full h-full mb-[50px] justify-center' key={`group-${idx}`}>
                    {oneView}
                </ul>
            );
            oneView = [];
        }
        const imgSrc = imgs.length > 0 ? imgs[0] : '';
        oneView.push(
            <li
                className='h-auto font-mono overflow-hidden w-full relative fix  m-0 mx-[15px] max-sm:mx-1'
                key={`item-${element.id}`}
            >   
                <div className='w-full transition duration-700 ease-in-out p-2 relative fix hover:shadow-2xl hover:bg-white'>
                    <a href={`/Product/${element.page}/${element.id}`} >
                        <div className='overflow-hidden fit object-cover'>
                            <img
                                src={imgSrc}
                                alt="Framed"
                            />
                        </div>
                        <p className='font-bold absolute flex justify-center items-center top-0 right-0 bg-[red] h-[50px] w-[50px] rounded-[50%] text-[white]'> -{element.giam_gia}%</p>
                        <div className='left-0 h-[100px] px-1 w-full right-0 py-1 bg-white relative'>
                            <div className='relative'>
                                <p className='font-bold h-[70px] block w-full overflow-hidden'>{element.name} - tap: {element.tap}</p>
                            </div>
                            <div className='text-[red] text-[15px] w-full absolute bottom-0'>
                                <div className='relative w-full'>
                                    <label className='z-10 left-0'>{formatPrice(element.gia)}</label>
                                    <label className='absolute text-gray-400 right-[10px] line-through'><strong>{formatPrice(element.gia_goc)}</strong></label>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
            </li>
        );
        return null;
    });

    if (oneView.length > 0) {
        totalView.push(
            <ul className='flex w-full mb-[50px] justify-center' key={`group-last`}>
                {oneView}
                {Array.from({ length: count - (oneView.length % count) }).map((_, ind) => (
                    oneView.length % count !== 0 && (
                        <li
                            className='w-[100%] relative fix  p-0 m-0 ml-[25px] mr-[25px]'
                            key={`placeholder-${ind}`}
                        >
                        </li>
                    )
                ))}
            </ul>
        );
    }

    return (
        <div className='flex min-h-[1000px] justify-center  content-center'>
            <div className={`2xl:w-[1200px] xl:w-[1200px] lg:w-[full]  md:w-[full]  sm:w-[full] max-sm:w-[400px] `}>
                <ul>
                    {totalView}
                </ul>
            </div>
        </div>
    );
};

export default Frame;