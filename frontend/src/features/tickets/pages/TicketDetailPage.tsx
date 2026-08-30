import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  deleteTicket,
  getTicket,
  updateTicketStatus,
  type Ticket,
  type TicketStatus,
} from "../services/ticketService";

export default function TicketDetailPage() {
  const { ticketId } = useParams();
  const navigate = useNavigate();

  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusLoading, setStatusLoading] = useState(false);
const [deleteLoading, setDeleteLoading] = useState(false);



async function handleStatusChange(
  status: TicketStatus
) {
  if (!ticket) return;
  setStatusLoading(true);
  try {
    const updatedTicket = await updateTicketStatus(
      ticket.id,
      status
    );
    setTicket(updatedTicket);
  } catch (error) {
    console.error(error);
    setError("No se pudo cambiar el estado");
  } finally {
    setStatusLoading(false);
  }
}


async function handleDelete() {
  if (!ticket) return;

  const confirmed = window.confirm(
    `¿Seguro que quieres eliminar el ticket #${ticket.id}?`
  );

  if (!confirmed) return;

  setDeleteLoading(true);

  try {
    await deleteTicket(ticket.id);

    navigate("/tickets");
  } catch (error: any) {
  console.error("ERROR AL ELIMINAR:", error);
  console.error("STATUS:", error.response?.status);
  console.error("DATA:", error.response?.data);

  setError(
    error.response?.data?.detail ||
    "No se pudo eliminar el ticket"
  );
} finally {
    setDeleteLoading(false);
  }
}


  useEffect(() => {
    async function loadTicket() {
      if (!ticketId) {
        setError("Ticket inválido");
        setLoading(false);
        return;
      }

      try {
        const data = await getTicket(
          Number(ticketId)
        );

        setTicket(data);
      } catch (error) {
        console.error(error);
        setError("No se pudo cargar el ticket");
      } finally {
        setLoading(false);
      }
    }

    loadTicket();
  }, [ticketId]);

  if (loading) {
    return <div>Cargando ticket...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!ticket) {
    return <div>Ticket no encontrado</div>;
  }

  return (
    <div>
      <button onClick={() => navigate("/tickets")}>
        ← Volver a tickets
      </button>

      <h1>{ticket.title}</h1>

      <p>
        Ticket #{ticket.id}
      </p>

      <p>
        {ticket.description}
      </p>

      <label>Estado</label>

<select
  value={ticket.status}
  disabled={statusLoading}
  onChange={(event) =>
    handleStatusChange(
      event.target.value as TicketStatus
    )
  }
>
  <option value="open">
    Abierto
  </option>

  <option value="in_progress">
    En progreso
  </option>

  <option value="resolved">
    Resuelto
  </option>

  <option value="closed">
    Cerrado
  </option>
</select>

      <p>
        Prioridad: {ticket.priority}
      </p>

      <p>
        Creado por: {ticket.created_by}
      </p>

      <p>
        Asignado a:{" "}
        {ticket.assigned_to ?? "Sin asignar"}
      </p>

      <button
        onClick={handleDelete}
        disabled={deleteLoading}
      >
        {deleteLoading ? "Eliminando..." : "Eliminar ticket"}
      </button>
    </div>
  );
}