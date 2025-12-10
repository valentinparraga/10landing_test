import { Link } from "react-router-dom";
import  navLogo  from "../assets/logo10.png";

export const Register = () => {
  return (
    <section id="register" className="w-full space-y-2 mt-12 flex flex-col align-center justify-center">
            
      <Link to="/"> 
        <img src={navLogo} alt="Logo 10" className="h-25 w-25 place-self-center"/>
      </Link>

      <div className="w-full flex flex-col align-center justify-center">
        <h2 className="font-bold text-2xl my-12">Registrarse</h2>
        <form className="flex flex-col px-20 gap-2">
          <input
            className="border-1 rounded-md border-gray-600 p-2"
            type="Nombre"
            id="name"
            name="name"
            placeholder="Nombre"
            required
          />
          <input
            className="border-1 rounded-md border-gray-600 p-2"
            type="Apellido"
            id="surname"
            name="surname"
            placeholder="Apellido"
            required
          />
          <input
            className="border-1 rounded-md border-gray-600 p-2"
            type="email"
            id="email"
            name="email"
            placeholder="Email"
            required
          />
          <input
            className="border-1 rounded-md border-gray-600 p-2"
            type="tel"
            id="phone"
            name="phone"
            pattern="[0-9]{3}[0-9]{3}[0-9]{4}"
            placeholder="Telefono"
            required 
          />
          <input
            className="border-1 rounded-md border-gray-600 p-2"
            type="passsword"
            id="password"
            name="passsword"
            placeholder="Contraseña"
            required
          />
          <button type="submit">Registrarse</button>
        </form>
      </div>
    </section>
  );
};
