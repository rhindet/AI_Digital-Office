import "./App.css";

import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import LoginPage from "./features/auth/pages/LoginPage";
import DashboardPage from "./features/dashboard/pages/DashboardPage";

import { AuthProvider } from "./core/auth/AuthContext";
import ProtectedRoute from "./core/auth/ProtectedRoute";
import MainLayout from "./core/layouts/MainLayout";

import TicketsPage from "./features/tickets/pages/TicketsPage";

import CreateTicketPage from "./features/tickets/pages/CreateTicketPage";

import TicketDetailPage from "./features/tickets/pages/TicketDetailPage";



function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>

          {/* Pública */}
          <Route
            path="/login"
            element={<LoginPage />}
          />

          {/* Protegidas */}
          <Route element={<ProtectedRoute />}>

            <Route element={<MainLayout />}>

              <Route
                path="/dashboard"
                element={<DashboardPage />}
              />

               <Route
                  path="/tickets"
                  element={<TicketsPage />}
                />

                 <Route
                  path="/tickets/new"
                  element={<CreateTicketPage />}
                 />

                 <Route
                  path="/tickets/:ticketId"
                  element={<TicketDetailPage />}
                />

              

            </Route>

          </Route>

        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;