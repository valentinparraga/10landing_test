import axiosInstance from "./axios";
import { API_ENDPOINTS } from "../utils/constants";

const serviceService = {
    // Listar todos los servicios
    getAll: async (params = {}) => {
        const response = await axiosInstance.get(API_ENDPOINTS.SERVICES, { params });
        return response.data;
    },

    // Obtener detalle de un servicio
    getById: async (id) => {
        const response = await axiosInstance.get(API_ENDPOINTS.SERVICE_DETAIL(id));
        return response.data;
    },

    // Obtener resumen de servicios
    getSummary: async () => {
        const response = await axiosInstance.get(API_ENDPOINTS.SERVICE_SUMMARY);
        return response.data;
    },

    // Obtener profesionales que ofrecen un servicio
    getProfessionals: async (serviceId) => {
        const response = await axiosInstance.get(API_ENDPOINTS.SERVICE_PROFESSIONALS(serviceId));
        return response.data;
    },

    // Buscar servicios
    search: async (searchTerm) => {
        const response = await axiosInstance.get(API_ENDPOINTS.SERVICES, {
            params: { search: searchTerm },
        });
        return response.data;
    },

};

export default serviceService;