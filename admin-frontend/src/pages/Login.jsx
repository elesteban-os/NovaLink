import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';
import './Login.css';

const AUTH_API_URL = 'http://localhost:8006'; // API de Auth

function Login({ onLogin }) {
  const [loginError, setLoginError] = useState('');

  const handleLogin = async (credentials) => {
    setLoginError('');
    try {
      // Hacemos la peticion POST al endpoint de auth
      const res = await fetch(`${AUTH_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password
        })
      });

      if (res.ok) {
        const data = await res.json(); 
        
        if (data.access_token) {
          localStorage.setItem('token', data.access_token);
          const payload = JSON.parse(atob(data.access_token.split('.')[1]));
          const email = credentials.email.toLowerCase();
          let role = 'user'; 
          let userId = payload.user_id;
          
          if (email.includes('@admin')) {
            role = 'admin';
          }

          onLogin({ role, userId });
        } else {
          setLoginError('Correo o contraseña incorrectos. Verifica tus credenciales.');
        }
      } else {
        setLoginError('Error del servidor al intentar iniciar sesión.');
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      setLoginError('No se pudo conectar con el servidor.');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>NovaLink</h1>
          <p>Ecosistema de Habilidades Sociales</p>
          <div style={{fontSize: "0.8rem", color: "#666", marginTop: "10px"}}>
            (Usa tunombre@admin.com para vista Admin. tunombre@user.com para vista Usuario)
          </div>
        </div>
        {loginError && (
          <div style={{ color: 'red', textAlign: 'center', marginBottom: '15px', fontWeight: 'bold' }}>
            {loginError}
          </div>
        )}
        <LoginForm onSubmit={handleLogin} />
      </div>
    </div>
  );
}

export default Login;
