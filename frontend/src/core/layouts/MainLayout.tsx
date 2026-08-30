import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function MainLayout() {
  const { user, logout } = useAuth();

  return (
    <div>
      <aside>
        <h2>AI Digital Office</h2>

        <nav>
          <NavLink to="/dashboard">
            Dashboard
          </NavLink>

          <NavLink to="/tickets">
            Tickets
          </NavLink>

          <NavLink to="/users">
            Users
          </NavLink>

          <NavLink to="/notifications">
            Notifications
          </NavLink>
        </nav>

        <div>
          <p>{user?.name}</p>
          <p>{user?.role}</p>

          <button onClick={logout}>
            Cerrar sesión
          </button>
        </div>
      </aside>

      <main>
        <Outlet />
      </main>
    </div>
  );
}