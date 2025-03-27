import React, { useRef, useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass, faBook, faAnglesDown } from '@fortawesome/free-solid-svg-icons';
import PaginationHelper from "../pages/Admin/pagination";

class Node {
    constructor() {
        this.Max = 256;
        this.children = new Array(this.Max).fill(null);
        this.countWord = 0;
        this.result = [];
        this.books = {};
    }
}

function removeAccents(str) {
    const accents = [
        { base: 'a', letters: /[áàảãạâầấẩẫậăằắẳẵặ]/g },
        { base: 'e', letters: /[éèẻẽẹêềếểễệ]/g },
        { base: 'i', letters: /[íìỉĩị]/g },
        { base: 'o', letters: /[óòỏõọôồốổỗộơờớởỡợ]/g },
        { base: 'u', letters: /[úùủũụưừứửữự]/g },
        { base: 'y', letters: /[ýỳỷỹỵ]/g },
        { base: 'd', letters: /[đ]/g }
    ];

    if(isNumber(str))
        return str;

    accents.forEach(({ base, letters }) => {
        str = str.replace(letters, base);
    });

    return str;
}

function isNumber(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}


class Trie {
    constructor() {
        this.root = new Node();
    }

    addWord(word, book) {
        let currentNode = this.root;
        let tempword = isNumber(word) ? word : word.toLowerCase();
        tempword = removeAccents(tempword);
        for (let char of tempword) {
            const index = char.charCodeAt(0);
            if (!currentNode.children[index]) {
                currentNode.children[index] = new Node();
            }
            currentNode = currentNode.children[index];

            if (!currentNode.books[book.id]) {
                currentNode.result.push(word);
                currentNode.books[book.id] = book;
            }
        }
        currentNode.countWord++;
    }

    findWord(prefix) {
        let currentNode = this.root;
        let result = [];
        prefix = prefix.toLowerCase();
        prefix = removeAccents(prefix);
        
        for (let char of prefix) {
            const index = char.charCodeAt(0);
            if (!currentNode.children[index]) {
                return [];
            }
            currentNode = currentNode.children[index];
        }
    
        result = Object.values(currentNode.books);
        return result;
    }
    clear() {
        this.root = new Node(); 
    }
}

const trie = new Trie();

export function Search(fetchedData, checkedItems, handleCheckboxChange, formatPrice, handleStatusChange, toggleModal, open, edit, setID) {
    const [results, setResults] = useState([]);
    const [currentCategory, setCurrentCategory] = useState('Tìm theo tên');
    const [index, setIndex] = useState(0);
    const resultsRef = useRef();
    const resultsRef1 = useRef();
    const data = fetchedData;
    const [Open, setOpen] = useState(false);

    useEffect(() => {
        if (Array.isArray(data) && data.length > 0 && currentCategory === "Tìm theo tên") {
            trie.clear();
            data.forEach(element => {
                if (element && element.name) {
                    trie.addWord(element.name, element);
                }
            });
        }else if (Array.isArray(data) && data.length > 0 && currentCategory === "Tìm theo ID") {
            trie.clear();
            data.forEach(element => {
                if (element && element.id.toString()) {
                    trie.addWord(element.id.toString(), element);
                }
            });
        }
    }, [data, currentCategory]);

    const test = (event) => {
        const { value } = event.target;
        const foundWords = trie.findWord(value);
        setResults(foundWords);
    };

    const categories = [
        "Tìm theo tên",
        "Tìm theo ID",
    ];

    function getHTML() {
        if (Array.isArray(results) && results.length > 0) {
            return (
                <PaginationHelper
                    data={results}
                    checkedItems={checkedItems}
                    handleCheckboxChange={handleCheckboxChange}
                    formatPrice={formatPrice}
                    handleStatusChange={handleStatusChange}
                    toggleModal={toggleModal}
                    open={open}
                    edit={edit}
                    setID={setID}
                    results={results}
                />
            );
        }
    }

    const SecrchResult = getHTML();

    const input = [];

    const handleClick = (index) => {
        setOpen(!Open);
        setIndex(index);
    };

    const listCategory = categories.map((element, index) => (
        <li
            key={index}
            className={`border-b border-black pt-[10px] bg-[#F8F8F8] hover:bg-[#F5ECD5] hover:text-[red]`}
            onClick={() => {
                setCurrentCategory(element);
                handleClick(index);
            }}
        >
            <span className="ml-[10px]">{element}</span>
        </li>
    ));

    input.push(
        <div className={"w-[600px] z-0"}>
            <div className='flex items-center z-50 bg-[#F8F8F8] w-[100%] relative'>
                <input
                    onKeyUp={test}
                    type="text"
                    className="form-control bg-[#F8F8F8] py-4 outline-none rounded-[10px] w-[75%] pl-[20px] text-[20px]"
                    name="name"
                    placeholder="Tìm kiếm sản phẩm"
                    aria-label="Tìm kiếm sản phẩm"
                />
                <ul ref={resultsRef1} className="items-center text-[15px] bold-900 cursor-pointer w-[25%]">
                    <li className="px-[15px] py-[10px] flex items-center border-l-2 border-[#8A8C91]" onClick={handleClick}>
                        {currentCategory}
                        <FontAwesomeIcon className={`absolute right-[10px]`} icon={faAnglesDown} />
                    </li>
                    <ul
                        className={`absolute w-[25%] text-black text-[15px] transition-all duration-300 ease-in-out ${Open ? "max-h-40 opacity-100" : "max-h-0 opacity-0"} overflow-hidden`}
                    >
                        {listCategory}
                    </ul>
                </ul>
            </div>
        </div>
    )
    return (
        [input, SecrchResult, results]
    );
}

