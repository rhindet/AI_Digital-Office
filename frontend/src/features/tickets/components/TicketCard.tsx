import type { Ticket } from "../services/ticketService";

interface TicketCardProps {
  ticket: Ticket;
}

export default function TicketCard({
  ticket,
}: TicketCardProps) {
  return (
    <div>
      <h2>{ticket.title}</h2>

      <p>{ticket.description}</p>

      <p>
        Estado: {ticket.status}
      </p>

      <p>
        Prioridad: {ticket.priority}
      </p>

      <p>
        Ticket #{ticket.id}
      </p>
    </div>
  );
}