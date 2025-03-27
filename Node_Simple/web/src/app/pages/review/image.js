import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/swiper-bundle.css';
import image1 from './../images/ms_banner_img1.webp';
import image2 from './../images/ms_banner_img2.webp';
import image3 from './../images/ms_banner_img3.webp';
import image4 from './../images/ms_banner_img4.webp';
import image5 from './../images/ms_banner_img5.webp';
import { Autoplay, Pagination, Navigation } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/pagination';

let images = [
    image1,
    image2,
    image3,
    image4,
    image5,
];

export function Images() {
    return (
        <header className=''>
            <Swiper
                spaceBetween={30}
                centeredSlides={true}
                autoplay={{
                  delay: 2500,
                  disableOnInteraction: false,
                }}
                pagination={{
                  clickable: true,
                }}
                navigation={true}
                modules={[Autoplay, Pagination, Navigation]}
                className="w-screen"
            >
                {images.map((image, index) => (
                    <SwiperSlide key={index}>
                        <img className="w-screen" src={image} alt={`Slide ${index + 1}`} />
                    </SwiperSlide>
                ))}
            </Swiper>
        </header>
    );
}