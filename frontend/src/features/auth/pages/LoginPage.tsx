import { useState } from "react";
import { login , getCurrentUser } from "../services/authService";
import { saveToken, removeToken  } from "../../../core/auth/authStorage";
import { useAuth } from "../../../core/auth/AuthContext";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { loginUser } = useAuth();
  const navigate = useNavigate();


  async function handleSubmit(

  event: React.FormEvent<HTMLFormElement>

) {

  event.preventDefault();

  setError("");

  setLoading(true);

  try {

    const data = await login({

      email,

      password,

    });

    saveToken(data.access_token);

    const user = await getCurrentUser();

    loginUser(user);

    navigate("/dashboard");

  } catch (error) {

    console.error(error);

    removeToken();

    setError("Correo o contraseña incorrectos");

  } finally {

    setLoading(false);

  }

}

  return (
    <div>
      <h1>AI Digital Office</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>

          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <div>
          <label>Password</label>

          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        {error && <p>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Iniciando sesión..." : "Iniciar sesión"}
        </button>
      </form>
    </div>
  );
}