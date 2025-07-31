import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ProductList from './ProductList';
import api from '../services/api';

const DepartmentPage = () => {
  const { id } = useParams();
  const [department, setDepartment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepartment = async () => {
      try {
        const response = await api.get(`/departments/${id}`);
        setDepartment(response.data);
      } catch (err) {
        setError('Error loading department');
        console.error('Error fetching department:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDepartment();
  }, [id]);

  if (loading) {
    return <div>Loading department...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!department) {
    return <div>Department not found</div>;
  }

  return (
    <div className="department-page">
      <div className="department-header">
        <h1>{department.name}</h1>
        <p>{department.product_count} products</p>
      </div>
      
      <ProductList 
        products={department.products}
        departmentId={id}
      />
    </div>
  );
};

export default DepartmentPage;
