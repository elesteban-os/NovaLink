import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar({ onLogout, role }) {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1>NovaLink</h1>
          <span>{role === 'admin' ? 'Admin Panel' : 'User Portal'}</span>
        </div>
        <ul className="navbar-menu">
          <li>
            <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
              Inicio
            </Link>
          </li>
          {role === 'admin' && (
            <li>
              <Link to="/usuarios" className={`nav-link ${isActive('/usuarios')}`}>
                Gestión de Usuarios
              </Link>
            </li>
          )}
          <li>
            <Link to="/habilidades" className={`nav-link ${isActive('/habilidades')}`}>
              {role === 'admin' ? 'Catálogo Maestras' : 'Comprar Habilidades'}
            </Link>
          </li>
          {role === 'user' && (
            <li>
              <Link to="/pedidos" className={`nav-link ${isActive('/pedidos')}`}>
                Mis Habilidades
              </Link>
            </li>
          )}
        </ul>
        <button className="btn-logout" onClick={onLogout}>
          Cerrar sesión
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
