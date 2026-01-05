import { useState } from "react";

import branchService from "../api/branchService";
import professionalService from "../api/professionalService";
import serviceService from "../api/serviceService";
import authService from "../api/authService";

const Test = () => {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const runTest = async () => {
    try {
      // ===============================
      // AUTH SERVICE
      // ===============================

      // 🔐 Registro
    //   const data = await authService.register({
    //     email: "test@test.com",
    //     password: "asdHGF123",
    //     password_confirm: "asdHGF123",
    //     first_name: "Test",
    //     last_name: "User",
    //     accepted_terms: true,
    //     accepted_privacy: true,
    //   });

      // 🔐 Login
      // const data = await authService.login("test@test.com", "asdHGF123");

      // 🔐 Usuario actual (requiere JWT)
      // const data = await authService.getCurrentUser();

      // 🔐 Perfil completo
      // const data = await authService.getProfile();

      // 🔐 Logout
      // const data = await authService.logout();


      // ===============================
      // BRANCH SERVICE
      // ===============================

      // 🏢 Listar sucursales
      // const data = await branchService.getAll();

      // 🏢 Detalle de sucursal 
      // const data = await branchService.getById(1);

      // 🏢 Profesionales de una sucursal 
      // const data = await branchService.getProfessionals(1);


      // ===============================
      // SERVICE SERVICE
      // ===============================

      // ✂️ Listar servicios
      // const data = await serviceService.getAll();

      // ✂️ Detalle de servicio 
      // const data = await serviceService.getById(1);

      // ✂️ Resumen de servicios
      // const data = await serviceService.getSummary();

      // ✂️ Profesionales que ofrecen un servicio 
      // const data = await serviceService.getProfessionals(1);

      // ✂️ Buscar servicios
      // const data = await serviceService.search("corte");


      // ===============================
      // PROFESSIONAL SERVICE
      // ===============================

      // 💈 Listar profesionales
      // const data = await professionalService.getAll();

      // 💈 Detalle de profesional
      // const data = await professionalService.getById(1);

      // 💈 Resumen de profesionales
      // const data = await professionalService.getSummary();

      // 💈 Profesionales por sucursal
      // const data = await professionalService.getByBranch(1);

      // 💈 Profesionales por servicio
      // const data = await professionalService.getByService(1);

      // 💈 Buscar profesionales
      // const data = await professionalService.search("F");


      // ⚠️ IMPORTANTE
      // Dejá UNA SOLA línea descomentada
      // y comentá el resto

      setResult(data);
      setError(null);

    } catch (err) {
      setError(err.response?.data || err.message);
      setResult(null);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🧪 Dev API Test</h2>

      <button onClick={runTest}>
        Ejecutar petición
      </button>

      {result && (
        <>
          <h3>✅ Resultado</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </>
      )}

      {error && (
        <>
          <h3 style={{ color: "red" }}>❌ Error</h3>
          <pre>{JSON.stringify(error, null, 2)}</pre>
        </>
      )}
    </div>
  );
};

export default Test;
