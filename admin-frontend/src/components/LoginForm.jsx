import React, { useState } from 'react';
import './LoginForm.css';

function LoginForm({ onSubmit }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Por favor completa todos los campos');
      return;
    }
    setError('');
    onSubmit({ email, password });
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Iniciar sesión</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-group">
        <label htmlFor="email">Correo electrónico</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="admin@novalink.com"
        />
      </div>

      <div className="form-group">
        <label htmlFor="password">Contraseña</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
        />
      </div>

      <button type="submit" className="btn-primary">
        Ingresar
      </button>

      <p className="demo-note">
        Demo: Usa cualquier usuario y contraseña
      </p>
    </form>
  );
}

export default LoginForm;
