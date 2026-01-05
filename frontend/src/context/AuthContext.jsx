import { createContext, useState, useEffect } from "react";
import authService from "../api/authService";

// Crear el contexto
export const AuthContext = createContext();

// Provider del contexto
export const AuthProvider =  ({ children }) => {
    const [User, setUser ] = useState(null);
    const [loading, setLoading] = useState(true);
    const[isAuthenticated, setIsAuthenticated] = useState(false);

    // Cargar usuario al iniciar la app
    useEffect(() => {
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            // Verificar si hay token
            if (authService.isAuthenticated()) {
                // Obtener usuario del servidor
                const userData = await authService.getCurrentUser();
                setUser(userData);
                setIsAuthenticated(true);
            }
        } catch (error){
            console.error('Error al cargar usuario: ', error);
            // Si falla limpiar todo
            await LogOut();
        } finally {
            setLoading(false);
        }
    };

    // Login
    const login = async (email, password) => {
        try {
            const response = await authService.login(email, password);
            setUser(response.user);
            setIsAuthenticated(true);
            return { succes: true, data: response};
        } catch (error) {
            console.error('Error en login: ', error);
            return {
                succes: false,
                error: error.response?.data?.error || 'Error al iniciar sesion'
            };
        }
    };

    // Registro
    const register = async (userData) => {
        try {
            const response = await authService.register(userData);
            setUser(response.user);
            setIsAuthenticated(true);
            return { succes: true, data: response };
        } catch (error) {
            console.error('Error en registro: ', error);
            return {
                succes: false,
                error: error.response?.data || 'Error al registrarse'
            };
        }
    };

    // Logout
    const logout = async () => {
        try {
            await authService.logout();
        } catch (error) {
            console.error('Error en logout: ', error);
        } finally {
            setUser(null);
            setIsAuthenticated(false);
        }
    };

    // Actualizar usuario
    const updateUser = async (userData) => {
        try {
            const response = await authService.updateUser(userData);
            setUser(response.user);
            return { succes: true, data: response };
        } catch (error) {
            console.error('Error al actualizar perfil: ', error);
            return { 
                succes: false, 
                error: error.response?.data || 'Error al actualizar perfil'
            };
        }
    };


    // Cambiar constraseña


    // Valores y funciones que se expondran
    const value = {
        user,
        loading,
        isAuthenticated,
        login,
        register,
        logout,
        updateUser,
        //changePAssword,
        loadUser,
    }; 

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};