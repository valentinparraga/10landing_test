//componente creado para mostrar navbar y footer en secciones que lo ameriten
//y ocultarlo en rutass como login y register

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function MainLayout({ children }) {
  return (
    <>
      <Navbar />
      {children}
      <Footer />
    </>
  );
}