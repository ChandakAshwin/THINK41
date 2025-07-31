import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import DepartmentList from './components/DepartmentList';
import DepartmentPage from './components/DepartmentPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="main-container">
          <div className="sidebar">
            <DepartmentList />
          </div>
          <main className="content">
            <Routes>
              <Route path="/" element={<ProductList />} />
              <Route path="/product/:id" element={<ProductDetail />} />
              <Route path="/departments/:id" element={<DepartmentPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;