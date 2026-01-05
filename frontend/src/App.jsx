import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./components/MainLayout";

import Hero from './components/Hero'
import Main from './components/Main'
import FindUs from './components/FindUs'
import Turnos from './components/Turnos'
import Login from './components/Login'
import { Register } from './components/Register'
import Test from './components/Test'

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Rutas que SI muestran el Navbar */}
        <Route
          path="/"
          element={
            <MainLayout>
              <Hero />
              <Main />
              <FindUs />
            </MainLayout>
          }
        />

        <Route
          path="/turnos"
          element={
            <MainLayout>
              <Turnos />
            </MainLayout>
          }
        />

        {/* Rutas sin navbar */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;