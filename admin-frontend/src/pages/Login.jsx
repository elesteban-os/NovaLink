import React from 'react';
import LoginForm from '../components/LoginForm';
import './Login.css';

function Login({ onLogin }) {
  const handleLogin = (credentials) => {
    // Simulamos validación (en real usarías la API)
    console.log('Credenciales:', credentials);
    onLogin();
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>NovaLink</h1>
          <p>Ecosistema de Habilidades Sociales</p>
        </div>
        <LoginForm onSubmit={handleLogin} />
      </div>
    </div>
  );
}

export default Login;
