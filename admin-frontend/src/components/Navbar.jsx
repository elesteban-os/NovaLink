import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar({ onLogout }) {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1>NovaLink</h1>
          <span>Admin Panel</span>
        </div>
        <ul className="navbar-menu">
          <li>
            <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/usuarios" className={`nav-link ${isActive('/usuarios')}`}>
              Usuarios
            </Link>
          </li>
          <li>
            <Link to="/habilidades" className={`nav-link ${isActive('/habilidades')}`}>
              Catálogo
            </Link>
          </li>
          <li>
            <Link to="/pedidos" className={`nav-link ${isActive('/pedidos')}`}>
              Pedidos
            </Link>
          </li>
        </ul>
        <button className="btn-logout" onClick={onLogout}>
          Cerrar sesión
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
