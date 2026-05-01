import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Users from './pages/Users';
import Skills from './pages/Skills';
import Orders from './pages/Orders';
import Navbar from './components/Navbar';
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState(null); // 'admin' o 'user'
  const [currentUserId, setCurrentUserId] = useState(null); 

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUserRole(userData.role);
    setCurrentUserId(userData.userId);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserRole(null);
    setCurrentUserId(null);
    localStorage.removeItem('token');
  };

  return (
    <Router>
      {isAuthenticated && <Navbar onLogout={handleLogout} role={userRole} />}
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/habilidades" />
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />
        <Route
          path="/usuarios"
          element={isAuthenticated && userRole === 'admin' ? <Users /> : <Navigate to="/habilidades" />}
        />
        <Route
          path="/habilidades"
          element={isAuthenticated ? <Skills role={userRole} userId={currentUserId} /> : <Navigate to="/login" />}
        />
        <Route
          path="/pedidos"
          element={isAuthenticated && userRole === 'user' ? <Orders userId={currentUserId} /> : <Navigate to="/habilidades" />}
        />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
