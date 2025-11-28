import { useState } from "react";
import { Menu, X } from "lucide-react";
import navLogo from "../assets/logo10.png";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const links = [
    { name: "Inicio", href: "#" },
    { name: "Turnos", href: "#" },
    { name: "Cursos", href: "#" },
    { name: "Contacto", href: "#" },
  ];
  return (
    <nav className="bg-neutral-900">
      {/* 📱 MENÚ HAMBURGUESA */}
      <div className="flex justify-between items-center space-x-5 px-2">
        {/* 📱 LOGO 10 */}
        <img src={navLogo} className="w-[80px] sm:inline-flex md:hidden"></img>
        <img
          src={navLogo}
          className="w-[120px] sm:hidden hidden md:inline-flex"
        ></img>
        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X size={28} /> : <Menu size={28} />}
        </button>
        <ul className="hidden md:flex space-x-5">
          {links.map((link) => (
            <li key={link.name}>
              <a className="text-xl font-semibold" href={link.href}>
                {link.name}
              </a>
            </li>
          ))}
        </ul>
        <span className="flex gap-x-2 hidden md:flex">
          <button> Iniciar sesión </button>
          <button> Registrarse </button>
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
            <button> Iniciar sesión </button>
            <button> Registrarse </button>
          </span>
        </ul>
      )}
    </nav>
  );
}
