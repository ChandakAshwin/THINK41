import React from 'react';
import { useNavigate } from 'react-router-dom';

const ProductCard = ({ product }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/product/${product.id}`);
  };

  const formatPrice = (price) => {
    if (!price) return 'Price not available';
    return `$${parseFloat(price).toFixed(2)}`;
  };

  return (
    <div className="product-card" onClick={handleClick}>
      <div className="product-image">
        📦 Product Image
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-category">{product.category}</p>
        {product.brand && (
          <p className="product-brand">Brand: {product.brand}</p>
        )}
        <p className="product-price">{formatPrice(product.retail_price)}</p>
      </div>
    </div>
  );
};

export default ProductCard; 