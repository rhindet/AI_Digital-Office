import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function ProtectedRoute() {
  const {
    isAuthenticated,
    loading,
  } = useAuth();

  console.log("ProtectedRoute:", {
    isAuthenticated,
    loading,
  });

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    console.log("NO AUTENTICADO → LOGIN");

    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}