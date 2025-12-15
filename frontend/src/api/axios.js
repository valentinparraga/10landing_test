import axios from 'axios';
import { API_BASE_URL, STORAGE_KEYS, AUTH_ENDPOINTS } from '../utils/constants';

// Crear instancia de axios
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
});

// Interceptor de Request: Agregar token automaticamente
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);

        if (token) {
            config.headers.Authorization = 'Bearer ${token}';
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor de Response: Manejar refresh de token
axiosInstance.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config;

        // Si el error es 401 y no se intento refrescar el token
        if (error.response?.status === 401 && !originalRequest._retry){
            originalRequest._retry =  true;
            
            const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)

            if (refreshToken) {
                try {
                    // Intentar refrescar token
                    const { data } = await axios.post(
                        '${API_BASE_URL}${AUTH_ENDPOINTS.TOKEN_RESFRESH}',
                        { refresh: refreshToken }
                    );

                    // Guardar nuevo access token
                    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, data.access);

                    // Actualizar header de autorización
                    axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ${data.access}';
                    originalRequest.headers['Authorization'] = 'Bearer ${data.access}';

                    // Reaintentar la petición original
                    return axiosInstance(originalRequest)
                } catch (refreshError) {
                    // Si falla el refresh, limpiar storage y redirigir a login
                    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
                    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
                    localStorage.removeItem(STORAGE_KEYS.USER);

                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            } else {
                // No hay refresh token, redirigir a login
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;