import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Usuarios
export const getUsersAPI = () => axiosInstance.get('/users');
export const getUserAPI = (id) => axiosInstance.get(`/users/${id}`);
export const createUserAPI = (data) => axiosInstance.post('/users', data);
export const updateUserAPI = (id, data) => axiosInstance.put(`/users/${id}`, data);
export const deleteUserAPI = (id) => axiosInstance.delete(`/users/${id}`);
export const getUserSkillsAPI = (id) => axiosInstance.get(`/users/${id}/skills`);

// Habilidades
export const getSkillsAPI = () => axiosInstance.get('/skills');
export const getSkillAPI = (id) => axiosInstance.get(`/skills/${id}`);
export const createSkillAPI = (data) => axiosInstance.post('/skills', data);
export const updateSkillAPI = (id, data) => axiosInstance.put(`/skills/${id}`, data);
export const deleteSkillAPI = (id) => axiosInstance.delete(`/skills/${id}`);

// Pedidos
export const getOrdersAPI = () => axiosInstance.get('/orders');
export const getOrderAPI = (id) => axiosInstance.get(`/orders/${id}`);
export const createOrderAPI = (data) => axiosInstance.post('/orders', data);
export const updateOrderAPI = (id, data) => axiosInstance.put(`/orders/${id}`, data);
export const deleteOrderAPI = (id) => axiosInstance.delete(`/orders/${id}`);

// Notificaciones
export const getNotificationsAPI = () => axiosInstance.get('/notifications');
export const createNotificationAPI = (data) => axiosInstance.post('/notifications', data);

export default axiosInstance;
