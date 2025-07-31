import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const DepartmentList = () => {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await api.get('/departments');
        setDepartments(response.data);
      } catch (error) {
        console.error('Error fetching departments:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDepartments();
  }, []);

  if (loading) {
    return <div>Loading departments...</div>;
  }

  return (
    <div className="department-list">
      <h2>Departments</h2>
      <div className="department-grid">
        {departments.map((dept) => (
          <Link 
            key={dept.id}
            to={`/departments/${dept.id}`}
            className="department-item"
          >
            <div className="department-content">
              <h3>{dept.name}</h3>
              <p>{dept.product_count} products</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default DepartmentList;
