import { useEffect, useState } from "react";
import {
  getTickets,
  type Ticket,
} from "../services/ticketService";
import { useNavigate } from "react-router-dom";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    async function loadTickets() {
      try {
        const data = await getTickets();

        setTickets(data);
      } catch (error) {
        console.error(error);
        setError("No se pudieron cargar los tickets");
      } finally {
        setLoading(false);
      }
    }

    loadTickets();
  }, []);

  if (loading) {
    return <div>Cargando tickets...</div>;
  }

  return (
    <div>
      <h1>Tickets</h1>

      <button onClick={() => navigate("/tickets/new")}>
        Crear ticket
      </button>

      {error && <p>{error}</p>}

      {tickets.length === 0 ? (
        <p>No tienes tickets.</p>
      ) : (
        <div>
          {tickets.map((ticket) => (
  <div key={ticket.id}>
    <h2>{ticket.title}</h2>

            <p>{ticket.description}</p>

            <p>
            Estado: {ticket.status}
            </p>

            <p>
            Prioridad: {ticket.priority}
            </p>

            <button
            onClick={() =>
                navigate(`/tickets/${ticket.id}`)
            }
            >
            Ver ticket
            </button>

            <hr />
        </div>
        ))}
        </div>
      )}
    </div>
  );
}