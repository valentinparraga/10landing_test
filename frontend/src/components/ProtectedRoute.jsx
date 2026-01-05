import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function ProtectedRoute({children}) {
    const { isAuthenticated, loading } = useAuth();

    // Mostrar loading mientras verifica autenticacion
    if (loading){ 
        return (
            <div className="loading-container">
                <p>Cargando...</p>
            </div>
        );
    }

    // Si no está autenticado, redirigir a login
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    // Si está autenticado, mostrar el contenido
    return children;
}

export default ProtectedRoute;