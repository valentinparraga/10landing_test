import axiosInstance from './axios';
import { AUTH_ENDPOINTS, STORAGE_KEYS } from '../utils/constants';

const authService = {
  // Registro de usuario
  register: async (userData) => {
    const response = await axiosInstance.post(AUTH_ENDPOINTS.REGISTER, userData);
    
    if (response.data.tokens) {
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.tokens.access);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.tokens.refresh);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  // Login
  login: async (email, password) => {
    const response = await axiosInstance.post(AUTH_ENDPOINTS.LOGIN, {
      email,
      password,
    });
    
    if (response.data.tokens) {
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.tokens.access);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.tokens.refresh);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  // Logout
  logout: async () => {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    
    try {
      await axiosInstance.post(AUTH_ENDPOINTS.LOGOUT, {
        refresh_token: refreshToken,
      });
    } catch (error) {
      console.error('Error al hacer logout:', error);
    } finally {
      // Limpiar localStorage siempre
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
    }
  },

  // Obtener usuario actual
  getCurrentUser: async () => {
    const response = await axiosInstance.get(AUTH_ENDPOINTS.ME);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data));
    return response.data;
  },

  // Obtener perfil completo
  getProfile: async () => {
    const response = await axiosInstance.get(AUTH_ENDPOINTS.PROFILE);
    return response.data;
  },

  // Actualizar perfil
  updateProfile: async (profileData) => {
    const response = await axiosInstance.put(AUTH_ENDPOINTS.ME, profileData);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    return response.data;
  },

  // Cambiar contraseña
  changePassword: async (passwordData) => {
    const response = await axiosInstance.post(AUTH_ENDPOINTS.CHANGE_PASSWORD, passwordData);
    return response.data;
  },

  // Solicitar reseteo de contraseña
  requestPasswordReset: async (email) => {
    const response = await axiosInstance.post(AUTH_ENDPOINTS.PASSWORD_RESET, { email });
    return response.data;
  },

  // Confirmar reseteo de contraseña
  confirmPasswordReset: async (token, newPassword, newPasswordConfirm) => {
    const response = await axiosInstance.post(AUTH_ENDPOINTS.PASSWORD_RESET_CONFIRM, {
      token,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
    return response.data;
  },

  // Verificar si hay usuario logueado
  isAuthenticated: () => {
    return !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  },

  // Obtener usuario del localStorage
  getUserFromStorage: () => {
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    return user ? JSON.parse(user) : null;
  },
};

export default authService;