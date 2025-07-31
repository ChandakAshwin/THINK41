import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productAPI } from '../services/api';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await productAPI.getProductById(id);
        setProduct(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const formatPrice = (price) => {
    if (!price) return 'Price not available';
    return `$${parseFloat(price).toFixed(2)}`;
  };

  const formatCost = (cost) => {
    if (!cost) return 'Cost not available';
    return `$${parseFloat(cost).toFixed(2)}`;
  };

  const getDepartmentDisplay = () => {
    // Prefer the new department_name, fall back to old department field
    return product.department_name || product.department || 'Department not available';
  };

  if (loading) {
    return <div className="loading">Loading product details...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error</h2>
        <p>{error}</p>
        <Link to="/" className="btn btn-primary" style={{ marginTop: '20px' }}>
          Back to Products
        </Link>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="error">
        <h2>Product Not Found</h2>
        <p>The product you're looking for doesn't exist.</p>
        <Link to="/" className="btn btn-primary" style={{ marginTop: '20px' }}>
          Back to Products
        </Link>
      </div>
    );
  }

  return (
    <div className="product-detail">
      <div className="product-detail-header">
        <Link to="/" className="back-button">
          ← Back to Products
        </Link>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        <div className="product-detail-image">
          📦 Product Image
        </div>

        <div className="product-detail-info">
          <h1 className="product-detail-name">{product.name}</h1>
          <p className="product-detail-category">Category: {product.category}</p>
          {product.brand && (
            <p className="product-detail-brand">Brand: {product.brand}</p>
          )}
          <p className="product-detail-department">
            Department: {getDepartmentDisplay()}
          </p>
          <p className="product-detail-price">
            Price: {formatPrice(product.retail_price)}
          </p>
          {product.sku && (
            <p className="product-detail-sku">SKU: {product.sku}</p>
          )}
          {product.department && product.department !== getDepartmentDisplay() && (
            <p className="product-detail-department">
              Original Department: {product.department}
            </p>
          )}
          {product.cost && (
            <p className="product-detail-cost">
              Cost: {formatCost(product.cost)}
            </p>
          )}
          {product.distribution_center_id && (
            <p className="product-detail-cost">
              Distribution Center ID: {product.distribution_center_id}
            </p>
          )}
          {product.department_id && (
            <p className="product-detail-cost">
              Department ID: {product.department_id}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductDetail; 