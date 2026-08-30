import { useAuth  } from "../../../core/auth/AuthContext";
import { useEffect, useState } from "react";

import { getDashboardSummary } from "../services/dashboardService";
import type { DashboardSummary } from "../services/dashboardService";


export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
useEffect(() => {
  async function loadDashboard() {
    const data = await getDashboardSummary();
    setSummary(data);
  }

  loadDashboard();
}, []);
  return (
    <div>
      <h1>AI Digital Office</h1>

      <h2>Dashboard</h2>

      <p>
        Bienvenido, {user?.name}
      </p>

      <p>
        Rol: {user?.role}
      </p>

      <button onClick={logout}>
        Cerrar sesión
      </button>

      <h2>Resumen de tickets</h2>

      <p>Total: {summary?.total_tickets}</p>
      <p>Abiertos: {summary?.open_tickets}</p>
      <p>En progreso: {summary?.in_progress_tickets}</p>
      <p>Resueltos: {summary?.resolved_tickets}</p>
      <p>Cerrados: {summary?.closed_tickets}</p>
      <p>Sin asignar: {summary?.unassigned_tickets}</p>
      <p>Alta prioridad: {summary?.high_priority_tickets}</p>
    </div>
  );
}