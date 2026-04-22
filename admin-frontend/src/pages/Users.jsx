import React, { useState, useEffect } from 'react';
import './Users.css';

// URL base provisional. Asegúrate de tener expuesto tu servicio en K8s o usar el proxy adecuado
const API_URL = 'http://localhost:8002'; 

function Users() {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', role: 'Estudiante', password: '123' });
  const [editingId, setEditingId] = useState(null);

  const fetchUsers = async () => {
    try {
      // GET /users
      const res = await fetch(`${API_URL}/users`);
      if (res.ok) {
        const data = await res.json();
        setUsers(data);
      }
    } catch (error) {
      console.error("Error obteniendo usuarios", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingId) {
        // PUT /users/{user_id}
        await fetch(`${API_URL}/users/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
      } else {
        // POST /users
        await fetch(`${API_URL}/users`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
      }
      fetchUsers();
      setFormData({ name: '', email: '', role: 'Estudiante', password: '123' });
      setShowForm(false);
      setEditingId(null);
    } catch (error) {
      console.error("Error guardando usuario", error);
    }
  };

  const handleEdit = (user) => {
    setFormData({ name: user.name, email: user.email, role: user.role, password: '' });
    setEditingId(user.id);
    setShowForm(true);
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Gestión de Usuarios (Admin)</h1>
          <button className="btn-add" onClick={() => { setShowForm(!showForm); setEditingId(null); }}>
            {showForm ? 'Cancelar' : '+ Nuevo Usuario'}
          </button>
        </div>

        {showForm && (
          <form className="card form-container" onSubmit={handleSubmit}>
            <h2>{editingId ? 'Editar Usuario' : 'Crear Nuevo Usuario'}</h2>
            <div className="form-group">
              <label>Nombre</label>
              <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Correo electrónico</label>
              <input type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Rol</label>
              <select value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })}>
                <option>Estudiante</option>
                <option>Instructor</option>
                <option>Admin</option>
              </select>
            </div>
            <button type="submit" className="btn-submit">
              {editingId ? 'Actualizar (PUT)' : 'Crear (POST)'}
            </button>
          </form>
        )}

        <div className="card">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id || user.user_id}>
                  <td>#{user.id || user.user_id}</td>
                  <td>{user.name || user.full_name}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>
                    <button className="btn-action btn-edit" onClick={() => handleEdit(user)}>Editar (PUT)</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Users;
