import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link to="/" className="logo">
            🛍️ E-commerce Products
          </Link>
          <nav className="nav-links">
            <Link to="/" className="nav-link">
              Products
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 