/**
 * API Service for Handicraft Image Recognition System
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * Search for similar products by uploading an image
 */
export const searchByImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await api.post('/api/v1/search', formData);
  return response.data;
};

/**
 * Get related products for a given product ID
 */
export const getRelatedProducts = async (productId) => {
  const response = await api.get(`/api/v1/products/${productId}/related`);
  return response.data;
};

/**
 * Get outlets selling a specific product
 */
export const getProductOutlets = async (productId) => {
  const response = await api.get(`/api/v1/products/${productId}/outlets`);
  return response.data;
};

/**
 * Get graph statistics
 */
export const getGraphStats = async () => {
  const response = await api.get('/api/v1/graph/stats');
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;


