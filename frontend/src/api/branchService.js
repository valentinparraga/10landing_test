import axiosInstance from "./axios";
import { API_ENDPOINTS } from "../utils/constants";

const branchService = {
    // Listar todas las sucursales
    getAll: async() => {
        const response = await axiosInstance.get(API_ENDPOINTS.BRANCHES);
        return response.data;
    },

    // Obtener detalle de una sucursal
    getById: async(id) => {
        const response = await axiosInstance.get(API_ENDPOINTS.BRANCH_DETAIL(id));
        return response.data;
    },

    // Obtener profesionales de una sucursal
    getProfessionals: async(branchId) => {
        const response = await axiosInstance.get(API_ENDPOINTS.BRANCHES_PROFESSIONALS(branchId));
        return response.data;
    }
};

export default branchService;