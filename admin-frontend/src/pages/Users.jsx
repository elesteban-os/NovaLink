import React, { useState, useEffect } from 'react';
import './Users.css';
import gateway from '../api/gatewayClient';

function Users() {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ first_name: '', last_name: '', email: '', role: 'user', password: '' });
  const [editingId, setEditingId] = useState(null);

  const fetchUsers = async () => {
    try {
      // Request users via API Gateway (usuarios.listar)
      const res = await gateway.requestAndWait('usuarios.listar', {});
      const payload = res?.payload || {};
      const result = payload.result || payload?.result || [];
      setUsers(result);
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
        // Excluimos email y dependemos si hay o no password en la DB
        const payload = {
          first_name: formData.first_name,
          last_name: formData.last_name
        };
        if (formData.password) {
            payload.password = formData.password;
        }

        await fetch(`${API_URL}/users/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      } else {
        // Create user via API Gateway event 'usuario.creado'
        const userPayload = {
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          password: formData.password,
        };
        try {
          const res = await gateway.requestAndWait('usuario.creado', userPayload);
          // Optionally inspect res.payload.result for created user
        } catch (err) {
          console.error('Error creando usuario via gateway', err);
        }
      }
      fetchUsers();
      setFormData({ first_name: '', last_name: '', email: '', role: 'user', password: '' });
      setShowForm(false);
      setEditingId(null);
    } catch (error) {
      console.error("Error guardando usuario", error);
    }
  };

  const handleEdit = (user) => {
    let currentRole = 'user';
    if (user.email.includes('@admin')) currentRole = 'admin';
    
    setFormData({ 
      first_name: user.first_name, 
      last_name: user.last_name, 
      email: user.email, 
      role: currentRole, 
      password: '' 
    });
    setEditingId(user.id);
    setShowForm(true);
  };

  const currentEmailLabel = editingId ? "Correo electrónico (No editable)" : "Correo electrónico";

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Gestión de Usuarios (Admin)</h1>
          <button className="btn-add" onClick={() => { setShowForm(!showForm); setEditingId(null); setFormData({ first_name: '', last_name: '', email: '', role: 'user', password: '' }); }}>
            {showForm ? 'Cancelar' : '+ Nuevo Usuario'}
          </button>
        </div>

        {showForm && (
          <form className="card form-container" onSubmit={handleSubmit}>
            <h2>{editingId ? 'Editar Usuario' : 'Crear Nuevo Usuario'}</h2>
            <div className="form-group">
              <label>Nombre(s)</label>
              <input type="text" value={formData.first_name} onChange={(e) => setFormData({ ...formData, first_name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Apellido(s)</label>
              <input type="text" value={formData.last_name} onChange={(e) => setFormData({ ...formData, last_name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>{currentEmailLabel}</label>
              <input type="email" disabled={!!editingId} value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required />
              {!editingId && <small>Nota: si deseas modo Admin, el correo debe contener '@admin.com'</small>}
            </div>
            {!editingId && (
                <div className="form-group">
                  <label>Rol (informativo via correo)</label>
                  <select disabled value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })}>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                  </select>
                </div>
            )}
            <div className="form-group">
              <label>{editingId ? "Nueva Contraseña (dejar en blanco para omitir)" : "Contraseña"}</label>
              <input type="password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} required={!editingId} />
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
                <th>Apellido</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>#{user.id}</td>
                  <td>{user.first_name}</td>
                  <td>{user.last_name}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`badge badge-${user.email.includes('@admin') ? 'admin' : 'completado'}`}>
                        {user.email.includes('@admin') ? 'Admin' : 'User'}
                    </span>
                  </td>
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
