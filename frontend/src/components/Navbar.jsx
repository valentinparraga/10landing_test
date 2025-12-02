import { useState } from "react";
import { Menu, X } from "lucide-react";
import navLogo from "../assets/logo10.png";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const links = [
    { name: "Inicio", href: "/" },
    { name: "Turnos", href: "/turnos" },
    { name: "Cursos", href: "/cursos" },
    { name: "Tienda", href: "/tienda" },
  ];
  return (
    <nav className="bg-neutral-900">
      {/* 📱 MENÚ HAMBURGUESA */}
      <div className="flex justify-around items-center space-x-5 px-2">
        {/* 📱 LOGO 10 */}
      
      <Link to="/">              
        <img 
          src={navLogo} 
          className="w-[80px] sm:inline-flex md:hidden">
        </img>
      </Link>

      <Link to="/">  
        <img
          src={navLogo}
          className="w-[120px] sm:hidden hidden md:inline-flex">
        </img>
      </Link>


        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X size={28} /> : <Menu size={28} />}
        </button>
        <ul className="hidden md:flex space-x-5">
          {links.map((link) => (
            <li key={link.name}>
              <Link className="text-xl font-semibold"to={link.href}>
                {link.name}
              </Link>
            </li>
          ))}
        </ul>
        <span className="flex gap-x-2 hidden md:flex">
            <Link
              onClick={() => setOpen(false)}
              to="/login"
              className="text-xl font-semibold p-2 rounded bg-neutral-700 hover:bg-neutral-600"
            >
              Iniciar sesión
            </Link>
                    
            <Link
              onClick={() => setOpen(false)}
              to="/register"
              className="text-xl font-semibold p-2 rounded bg-neutral-700 hover:bg-neutral-600"
            >
              Registrarse
            </Link>
        </span>
      </div>
      {/* 📱 MENU MOBILE */}
      {open && (
        <ul className="md:hidden flex flex-col items-center space-y-4 bg-neutral-900 py-6 shadow-md">
          {links.map((link) => (
            <li key={link.name}>
              <a
                className="text-xl font-semibold"
                href={link.href}
                onClick={() => setOpen(false)}
              >
                {link.name}
              </a>
            </li>
          ))}
          <span className="flex gap-x-2">
            <Link
              onClick={() => setOpen(false)}
              to="/login"
              className="text-xl font-semibold px-3 py-2 rounded bg-neutral-700 hover:bg-neutral-600"
            >
              Iniciar sesión
            </Link>

            <Link
              onClick={() => setOpen(false)}
              to="/register"
              className="text-xl font-semibold px-3 py-2 rounded bg-neutral-700 hover:bg-neutral-600"
            >
              Registrarse
            </Link>
          </span>
        </ul>
      )}
    </nav>
  );
}
