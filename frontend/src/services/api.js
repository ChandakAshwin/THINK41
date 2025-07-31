import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const productAPI = {
  // Get all products with pagination and optional search
  getProducts: async (page = 1, pageSize = 12, search = null) => {
    try {
      const params = {
        page,
        page_size: pageSize,
      };
      
      if (search) {
        params.search = search;
      }
      
      const response = await api.get('/api/products', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch products');
    }
  },

  // Get a specific product by ID
  getProductById: async (id) => {
    try {
      const response = await api.get(`/api/products/${id}`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        throw new Error('Product not found');
      }
      throw new Error(error.response?.data?.detail || 'Failed to fetch product');
    }
  },

  // Search products
  searchProducts: async (searchTerm, page = 1, pageSize = 12) => {
    try {
      const params = {
        search: searchTerm,
        page,
        page_size: pageSize,
      };
      
      const response = await api.get('/api/products/search', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to search products');
    }
  },

  // Get API information
  getAPIInfo: async () => {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch API information');
    }
  },
};

export default api; 