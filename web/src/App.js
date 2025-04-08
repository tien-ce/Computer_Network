import React, { useState } from 'react';
import './App.css';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Admin } from './app/pages/Admin/index';

export function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route index element={<Admin />} />
          <Route path="admin/*" element={<Admin />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;