import React, { useState, useEffect } from 'react';

export function useData(img = [], url) {  
  const [data, setData] = useState([]);
  const [images, setImages] = useState([]);

  useEffect(() => {
      const fetchData = async () => {
          try {
              const response = await fetch(`https://localhost/BTL_web_1/src/app/BackEnd/php/uploads/${url}.php`);
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              const result = await response.json();
              setData(result);
          } catch (error) {
              console.error("Error fetching data: ", error);
          }
      };

      fetchData();
  }, [url]);

  function getTampNumber(item){
    const fileName = item.split('/').pop();
    return fileName.split('_')[0];
  }

  useEffect(() => {
    if (data.length > 0 && img.length > 0) {
        const getData = {};
        data.forEach((element) => {
            getData[element.id] = element;
        });

        const items = [];
        
        for (let i = 0; i < img.length; i++) {
            const fileName = img[i].split('/').pop();
            const tempNumber = fileName.split('_')[0];
            let tempImg = [];
            if (getData[parseInt(tempNumber)]) {
                tempImg.push(img[i]);

                while (i < img.length - 1 && getTampNumber(img[i]) === getTampNumber(img[i + 1])) {
                    i++;
                    tempImg.push(img[i]);
                }
                let tempItem = {
                    img: tempImg,
                    id: getData[parseInt(tempNumber)].id,
                    gia_goc: getData[parseInt(tempNumber)].gia_goc,
                    gia: getData[parseInt(tempNumber)].gia,
                    giam_gia: getData[parseInt(tempNumber)].giam_gia,
                    name: getData[parseInt(tempNumber)].name,
                    tap: getData[parseInt(tempNumber)].tap,
                    tac_gia: getData[parseInt(tempNumber)].tac_gia,
                    khuon_kho: getData[parseInt(tempNumber)].khuon_kho,
                    so_trang: getData[parseInt(tempNumber)].so_trang,
                    trong_luong: getData[parseInt(tempNumber)].trong_luong,
                    page: getData[parseInt(tempNumber)].Page,
                };
                items.push(tempItem);
                tempImg = [];
            }
        }
        if (JSON.stringify(images) !== JSON.stringify(items)) {
            setImages(items);
        }
    }
}, [data, img]);
  return images;
}