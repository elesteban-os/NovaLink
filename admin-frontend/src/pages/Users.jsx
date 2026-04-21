import React, { useState, useEffect } from 'react';
import { usersData } from '../data/mockData';
import './Users.css';

function Users() {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', role: 'Estudiante' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    // Simulamos carga de datos desde API
    setUsers(usersData);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingId) {
      setUsers(
        users.map((u) =>
          u.id === editingId ? { ...u, ...formData } : u
        )
      );
      setEditingId(null);
    } else {
      const newUser = {
        id: Math.max(...users.map((u) => u.id), 0) + 1,
        ...formData,
        skills: 0,
      };
      setUsers([...users, newUser]);
    }

    setFormData({ name: '', email: '', role: 'Estudiante' });
    setShowForm(false);
  };

  const handleEdit = (user) => {
    setFormData({ name: user.name, email: user.email, role: user.role });
    setEditingId(user.id);
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      setUsers(users.filter((u) => u.id !== id));
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Mi Perfil</h1>
          <button className="btn-add" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : 'Editar Perfil'}
          </button>
        </div>

        {showForm && (
          <form className="card form-container" onSubmit={handleSubmit}>
            <h2>{editingId ? 'Editar Usuario' : 'Crear Nuevo Usuario'}</h2>
            <div className="form-group">
              <label>Nombre</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Correo electrónico</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Rol</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              >
                <option>Estudiante</option>
                <option>Instructor</option>
                <option>Admin</option>
              </select>
            </div>
            <button type="submit" className="btn-submit">
              {editingId ? 'Actualizar' : 'Crear'}
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
                <th>Habilidades</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>#{user.id}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>{user.skills}</td>
                  <td>
                    <button
                      className="btn-action btn-edit"
                      onClick={() => handleEdit(user)}
                    >
                      Editar
                    </button>
                    <button
                      className="btn-action btn-delete"
                      onClick={() => handleDelete(user.id)}
                    >
                      Eliminar
                    </button>
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
