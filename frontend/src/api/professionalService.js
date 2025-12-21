import axiosInstance from "./axios";
import { API_ENDPOINTS } from "../utils/constants";

const professionalService = {
    // Listar todos los profesionales
    getAll: async (params = {}) => {
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS, { params });
        return response.data;
    },

    // Obtener detalle de un profesional
    getById: async (id) => {
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS_DETAIL(id));
        return response.data;
    },

    // Obtener resumen de profesionales
    getSummary: async () =>{
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS_SUMMARY);
        return response.data;
    },

    // Filtrar por sucursal
    getByBranch: async (branchId) => {
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS, {
            params: { branch: branchId },
        });
        return response.data;
    },

    // Filtrar por servicio
    getByService: async (serviceId) => {
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS, {
            params: { service: serviceId },
        });
        return response.data;
    },

    // Buscar profesionales 
    search: async (searchTerm) => {
        const response = await axiosInstance.get(API_ENDPOINTS.PROFESSIONALS, {
            params: { search: searchTerm },
        });
        return response.data;
    },
};

export default professionalService;