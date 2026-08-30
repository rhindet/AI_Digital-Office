import { useState } from "react";
import { createTicket } from "../services/ticketService";
import { useNavigate } from "react-router-dom";

export default function CreateTicketPage() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("normal");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      await createTicket({
        title,
        description,
        priority,
      });

      navigate("/tickets");
    } catch (error) {
      console.error(error);
      setError("No se pudo crear el ticket");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Crear ticket</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Título</label>

          <input
            type="text"
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label>Descripción</label>

          <textarea
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label>Prioridad</label>

          <select
            value={priority}
            onChange={(event) =>
              setPriority(event.target.value)
            }
          >
            <option value="low">Baja</option>
            <option value="normal">Normal</option>
            <option value="high">Alta</option>
          </select>
        </div>

        {error && <p>{error}</p>}

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Creando..."
            : "Crear ticket"}
        </button>
      </form>
    </div>
  );
}