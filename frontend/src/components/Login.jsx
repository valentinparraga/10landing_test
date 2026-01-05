import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from '../hooks/useAuth'
import  navLogo  from "../assets/logo10.png";

function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const result = await login(formData.email, formData.password);

            if (result.success) {
                console.log('Login exitoso: ', result.data);
                navigate('/');
            }   else {
                setError(result.error);
            }
        }   catch (err) {
            console.error('Error inesperado: ', err);
            setError('Error inesperado. Intenta nuevamente.');
        }   finally {
            setLoading(false);
        }
    };

return (
    <section
      id="login"
      className="w-full mt-12 flex flex-col items-center justify-center space-y-6"
    >
      {/* Logo */}
      <Link to="/">
        <img
          src={navLogo}
          alt="Logo"
          className="h-24 w-24"
        />
      </Link>

      {/* Card */}
      <div className="w-full max-w-md flex flex-col items-center">
        <h2 className="font-bold text-2xl my-6">Iniciar sesión</h2>

        <form
          onSubmit={handleSubmit}
          className="w-full flex flex-col gap-3 px-6"
        >
          {error && (
            <div className="text-red-600 text-sm text-center">
              {error}
            </div>
          )}

          <input
            className="border rounded-md border-gray-600 p-2"
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <input
            className="border rounded-md border-gray-600 p-2"
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-2 bg-black text-white rounded-md p-2 hover:opacity-90 disabled:opacity-50"
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>

        <div className="mt-4 text-sm text-center">
          <p>
            ¿No tenés cuenta?{' '}
            <Link to="/register" className="underline">
              Registrate
            </Link>
          </p>
        </div>
      </div>
    </section>
  );
}

export default Login;