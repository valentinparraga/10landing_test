// URL base de la API
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Endpoints de autenticación
export const AUTH_ENDPOINTS = {
    REGISTER: '/auth/register/',
    LOGIN: '/auth/login/',
    LOGOUT: '/auth/logout/',
    ME: '/auth/me/',
    PROFILE: '/auth/profile/',
    CHANGE_PASSWORD: '/auth/change-password/',
    PASSWORD_RESET: '/auth/password-reset/',
    PASSWORD_RESET_CONFIRM: '/auth/password-reset-confirm/',
    TOKEN_REFRESH: '/auth/token/refresh',
};

// Endpoints principales
export const API_ENDPOINTS = {
    // Home
    HOME: '/home/',

    // Sucursales
    BRANCHES: '/branches/',
    BRANCH_DETAIL: (id) => '/branches/${id}/',
    BRANCHES_PROFESSIONALS: (id) => '/branches/${id}/professionals/',

    // Servicios
    SERVICES: '/services/',
    SERVICE_DETAIL: (id) => '/services/${id}/',
    SERVICE_SUMMARY: '/services/summary/',
    SERVICE_PROFESSIONALS: (id) => '/services/${id}/professionals/',

    // Profesionales
    PROFESSIONALS: '/professionals/',
    PROFESSIONALS_DETAIL: (id) => '/professionals/${id}/',
    PROFESSIONALS_SUMMARY: '/professionals/summary/',
};

// Keys para localStorage
export const STORAGE_KEYS = {
    ACCESS_TOKEN: 'access_token',
    REFRESH_TOKEN: 'refresh_token',
    USER: 'user',    
};