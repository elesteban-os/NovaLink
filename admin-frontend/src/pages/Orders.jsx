import React, { useState, useEffect } from 'react';
import './Orders.css';

const USERS_API_URL = 'http://localhost:8002';

function Orders({ userId }) {
  const [userSkills, setUserSkills] = useState([]);

  useEffect(() => {
    // GET /users/{user_id}/skills al backend de Usuarios
    fetchUserSkills();
  }, [userId]);

  const fetchUserSkills = async () => {
    try {
      const res = await fetch(`${USERS_API_URL}/users/${userId}/skills`);
      if (res.ok) {
        const data = await res.json();
        // El endpoint devuelve una lista de strings: ["Empatia", "Liderazgo"...]
        setUserSkills(data);
      }
    } catch (error) {
      console.error("Error obteniendo mis habilidades", error);
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Mis Habilidades Adquiridas (User)</h1>
          <p className="page-subtitle">Habilidades ligadas a tu perfil</p>
        </div>

        <div className="card">
          <table className="data-table">
            <thead>
              <tr>
                <th>Habilidad</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {userSkills.length > 0 ? (
                userSkills.map((skillName, index) => (
                  <tr key={index}>
                    <td>{skillName}</td>
                    <td>
                      <span className="badge badge-completado">Adquirida</span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr><td colSpan="2">Aún no tienes habilidades en tu perfil.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Orders;
