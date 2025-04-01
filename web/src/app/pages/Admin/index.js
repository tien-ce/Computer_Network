import { useState } from 'react';
import React from 'react';
import { Input } from "./../../BackEnd/input";
import { Post } from "./../../BackEnd/post";
import { Navbar } from "./navbar";
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { TorrentFileReader } from "./../../BackEnd/edit";

export function Admin() {
    return (
        
        <div className="flex w-[100%]">
            <Navbar/>
            <Routes>
                <Route path="/" element={<div className=' w-full '></div>} />
                <Route path="input" element={<Input />} />  
                <Route path="/post/:Status?" element={<Post />} />
                <Route path="/post/edit/:number?" element={<TorrentFileReader />} />
            </Routes>
        </div>
    );
}