import React, { useState, useEffect } from 'react';
import { ordersData, usersData, skillsData } from '../data/mockData';
import './Orders.css';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    userId: 1, // Usuario actual (simulado)
    skillId: skillsData[0]?.id || 1,
  });
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    setOrders(ordersData);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const skill = skillsData.find((s) => s.id === parseInt(formData.skillId));

    if (skill) {
      const newOrder = {
        id: Math.max(...orders.map((o) => o.id), 0) + 1,
        userId: 1, // Usuario actual
        skillId: parseInt(formData.skillId),
        skillName: skill.name,
        status: 'Completado', // Automáticamente completado al adquirir
        date: new Date().toISOString().split('T')[0],
      };
      setOrders([...orders, newOrder]);
      setFormData({
        userId: 1,
        skillId: skillsData[0]?.id || 1,
      });
      setShowForm(false);
    }
  };

  const handleStatusChange = (id, status) => {
    setOrders(
      orders.map((o) =>
        o.id === id ? { ...o, status } : o
      )
    );
  };

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este pedido?')) {
      setOrders(orders.filter((o) => o.id !== id));
    }
  };

  const filteredOrders = filter === 'all' ? orders : orders.filter((o) => o.status === filter);

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Mis Habilidades Adquiridas</h1>
          <button className="btn-add" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : '+ Adquirir Habilidad'}
          </button>
        </div>

        {showForm && (
          <form className="card form-container" onSubmit={handleSubmit}>
            <h2>Adquirir Nueva Habilidad</h2>
            <div className="form-row">
              <div className="form-group">
                <label>Seleccionar Habilidad</label>
                <select
                  value={formData.skillId}
                  onChange={(e) => setFormData({ ...formData, skillId: e.target.value })}
                  required
                >
                  {skillsData.map((skill) => (
                    <option key={skill.id} value={skill.id}>
                      {skill.name} (+{skill.xp} XP)
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button type="submit" className="btn-submit">
              Adquirir Habilidad
            </button>
          </form>
        )}

        <div className="card">
          <div className="filter-container">
            <label>Filtrar por estado:</label>
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">Todas</option>
              <option value="Completado">Completadas</option>
              <option value="En progreso">En progreso</option>
            </select>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Habilidad</th>
                <th>Puntos XP</th>
                <th>Estado</th>
                <th>Fecha de Adquisición</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrders.map((order) => {
                const skill = skillsData.find((s) => s.id === order.skillId);
                return (
                  <tr key={order.id}>
                    <td>{order.skillName}</td>
                    <td>+{skill?.xp || 0} XP</td>
                    <td>
                      <span className={`badge badge-${order.status.toLowerCase().replace(' ', '')}`}>
                        {order.status}
                      </span>
                    </td>
                    <td>{order.date}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Orders;
