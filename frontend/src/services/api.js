import axios from 'axios';

// Define a URL base da API
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Cria uma instância do axios com a URL base
const api = axios.create({
  baseURL: API_URL,
});

// Serviço para buscar produtos
export const searchProducts = async (term) => {
  const response = await api.get('/api/products/search', {
    params: { q: term }
  });
  return response.data;
};

// Serviço para obter um produto pelo ID
export const getProduct = async (id) => {
  const response = await api.get(`/api/products/${id}`);
  return response.data;
};

// Serviço para obter as regiões
export const getRegions = async () => {
  const response = await api.get('/api/regions');
  return response.data;
};

// Serviço para obter os municípios
export const getMunicipalities = async (regionCode = null) => {
  const response = await api.get('/api/municipalities', {
    params: regionCode ? { region_code: regionCode } : {}
  });
  return response.data;
};

// Serviço para obter o histórico de preços
export const getPriceHistory = async (params) => {
  const response = await api.get('/api/prices/history', { params });
  return response.data;
};

// Serviço para criar a URL de download do Excel
export const createExcelDownloadUrl = (params) => {
  const queryParams = new URLSearchParams();
  
  Object.entries(params).forEach(([key, value]) => {
    if (Array.isArray(value)) {
      value.forEach(val => queryParams.append(key, val));
    } else if (value !== null && value !== undefined) {
      queryParams.append(key, value);
    }
  });
  
  return `${API_URL}/api/prices/export?${queryParams.toString()}`;
};

export default api; 