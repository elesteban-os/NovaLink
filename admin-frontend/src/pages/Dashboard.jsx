import React, { useState, useEffect } from 'react';
import { usersData, skillsData, ordersData } from '../data/mockData';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalSkills: 0,
    completedOrders: 0,
    pendingOrders: 0,
  });

  useEffect(() => {
    // Simulamos carga de datos
    const completed = ordersData.filter((o) => o.status === 'Completado').length;
    const pending = ordersData.filter((o) => o.status === 'Pendiente').length;

    setStats({
      totalUsers: usersData.length,
      totalSkills: skillsData.length,
      completedOrders: completed,
      pendingOrders: pending,
    });
  }, []);

  return (
    <div className="app-container">
      <div className="main-content">
        <h1 className="page-title">NovaLink - Habilidades Sociales</h1>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Usuarios Registrados</h3>
            <div className="number">{stats.totalUsers}</div>
          </div>
          <div className="stat-card">
            <h3>Habilidades Disponibles</h3>
            <div className="number">{stats.totalSkills}</div>
          </div>
          <div className="stat-card">
            <h3>Pedidos Completados</h3>
            <div className="number">{stats.completedOrders}</div>
          </div>
          <div className="stat-card">
            <h3>Pedidos Pendientes</h3>
            <div className="number">{stats.pendingOrders}</div>
          </div>
        </div>

        <div className="card">
          <h2>Últimos Pedidos</h2>
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuario</th>
                <th>Habilidad</th>
                <th>Estado</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {ordersData.slice(0, 5).map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>Usuario {order.userId}</td>
                  <td>{order.skillName}</td>
                  <td>
                    <span className={`badge badge-${order.status.toLowerCase()}`}>
                      {order.status}
                    </span>
                  </td>
                  <td>{order.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
