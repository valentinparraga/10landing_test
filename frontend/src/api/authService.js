import axiosInstance from "./axios";
import { AUTH_ENDPOINTS, STORAGE_KEYS } from "../utils/constants";

const authService  = {
    // Registro de usuario
    register: async (userData) => {
        const response = await axiosInstance.get(AUTH_ENDPOINTS.REGISTER, userData);

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
            console.error('Error al hacer logout: ', error);
        } finally {
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

    // Cambiar contraseña

    // Solicitar reseteo de constraseña

    // Confirmar reseteo de constraseña

    // Verificar si hay usuario logueado
    idAuthenticated: () => {
        return !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    },

    // Obtener usuario del localStorage
    getUserFromStorage: () => {
        const user = localStorage.getItem(STORAGE_KEYS.USER);
        return user ? JSON.parse(user) : null;
    },
};

export default authService;