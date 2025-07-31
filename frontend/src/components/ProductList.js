import React, { useState, useEffect } from 'react';
import { productAPI } from '../services/api';
import ProductCard from './ProductCard';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const pageSize = 12;

  const fetchProducts = async (page, search = null) => {
    try {
      setLoading(true);
      setError(null);
      
      let data;
      if (search) {
        data = await productAPI.searchProducts(search, page, pageSize);
        setIsSearching(true);
      } else {
        data = await productAPI.getProducts(page, pageSize);
        setIsSearching(false);
      }
      
      setProducts(data.products);
      setTotalCount(data.total_count);
      setCurrentPage(data.page || page);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(1);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      fetchProducts(1, searchTerm.trim());
    } else {
      fetchProducts(1);
    }
  };

  const handlePageChange = (newPage) => {
    if (searchTerm.trim()) {
      fetchProducts(newPage, searchTerm.trim());
    } else {
      fetchProducts(newPage);
    }
  };

  const handleClearSearch = () => {
    setSearchTerm('');
    setIsSearching(false);
    fetchProducts(1);
  };

  const totalPages = Math.ceil(totalCount / pageSize);

  if (loading) {
    return <div className="loading">Loading products...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div>
      <h1>Products</h1>
      
      {/* Search Form */}
      <div className="search-container">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            className="search-input"
            placeholder="Search products by name, category, or brand..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">
            Search
          </button>
          {isSearching && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleClearSearch}
              style={{ marginLeft: '10px' }}
            >
              Clear Search
            </button>
          )}
        </form>
      </div>

      {/* Search Results Info */}
      {isSearching && (
        <div style={{ marginBottom: '20px', color: '#666' }}>
          Found {totalCount} products matching "{searchTerm}"
        </div>
      )}

      {/* Products Grid */}
      {products.length > 0 ? (
        <div className="products-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : (
        <div className="loading">
          {isSearching ? 'No products found matching your search.' : 'No products available.'}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          
          <span className="pagination-info">
            Page {currentPage} of {totalPages} ({totalCount} total products)
          </span>
          
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ProductList; 