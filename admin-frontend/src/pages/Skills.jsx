import React, { useState, useEffect } from 'react';
import './Skills.css';

const SKILLS_API_URL = 'http://localhost:8001';
const ORDERS_API_URL = 'http://localhost:8005';

function Skills({ role, userId }) {
  const [skills, setSkills] = useState([]);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ skill_name: '', difficulty_level: 1, stock: 10 });
  const [modalType, setModalType] = useState(null); // 'purchase', 'create', 'edit'

  const fetchSkills = async () => {
    try {
      // GET /skills
      const res = await fetch(`${SKILLS_API_URL}/skills`);
      if (res.ok) {
        const data = await res.json();
        setSkills(data);
      }
    } catch (error) {
      console.error("Error obteniendo habilidades:", error);
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handlePurchaseClick = (skill) => {
    setSelectedSkill(skill);
    setModalType('purchase');
    setShowModal(true);
  };

  const confirmPurchase = async () => {
    try {
      // POST /orders
      const orderPayload = {
        user_id: userId,
        skill_name: selectedSkill.skill_name || selectedSkill.name,
        quantity: 1
      };
      
      const res = await fetch(`${ORDERS_API_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderPayload)
      });
      
      if (res.ok) {
        alert("¡Pedido creado exitosamente!");
        setShowModal(false);
        // Aquí opcionalmente podrías llamar al POST /notifications
      } else {
        alert("Error creando pedido");
      }
    } catch (error) {
      console.error("Error en purchase", error);
    }
  };

  const handleAdminSubmit = async (e) => {
    e.preventDefault();
    try {
      if (modalType === 'edit') {
        // PUT /skills/{skill_id}
        await fetch(`${SKILLS_API_URL}/skills/${selectedSkill.skill_id || selectedSkill.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
      } else if (modalType === 'create') {
        // POST /skills
        await fetch(`${SKILLS_API_URL}/skills`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
      }
      fetchSkills();
      setShowModal(false);
      setFormData({ skill_name: '', difficulty_level: 1, stock: 10 });
    } catch (error) {
      console.error("Error admin action", error);
    }
  };

  const handleDelete = async (skill) => {
    if (window.confirm("¿Seguro que quieres eliminar esta habilidad?")) {
      try {
        // DELETE /skills/{skill_id}
        await fetch(`${SKILLS_API_URL}/skills/${skill.skill_id || skill.id}`, {
          method: 'DELETE'
        });
        fetchSkills();
      } catch (error) {
        console.error("Error deleting", error);
      }
    }
  };

  const getDifficultyColor = (level) => {
    if (level === 1) return '#4CAF50'; // Básico
    if (level === 2) return '#FF9800'; // Intermedio
    if (level >= 3) return '#F44336'; // Avanzado
    return '#666';
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">{role === 'admin' ? "Catálogo Maestra (Admin)" : "Adquirir Habilidades"}</h1>
            <p className="page-subtitle">Explora y descubre nuevas capacidades.</p>
          </div>
          {role === 'admin' && (
            <button className="btn-add" onClick={() => { setModalType('create'); setFormData({ skill_name: '', difficulty_level: 1, stock: 10 }); setShowModal(true); }}>
              + Crear Habilidad (POST)
            </button>
          )}
        </div>

        <div className="skills-catalog">
          {skills.map((skill) => (
            <div key={skill.skill_id || skill.id} className="skill-item">
              <div className="skill-header">
                <h3>{skill.skill_name || skill.name}</h3>
                <span className="difficulty-badge" style={{ backgroundColor: getDifficultyColor(skill.difficulty_level) }}>
                  Nivel: {skill.difficulty_level}
                </span>
              </div>
              <p>Stock disponible: {skill.stock}</p>
              
              <div className="skill-footer">
                {role === 'user' ? (
                  <button className="btn-purchase" onClick={() => handlePurchaseClick(skill)}>Pedir (POST /orders)</button>
                ) : (
                  <div style={{display: 'flex', gap: '10px'}}>
                    <button className="btn-action btn-edit" onClick={() => { setModalType('edit'); setSelectedSkill(skill); setFormData(skill); setShowModal(true); }}>Editar</button>
                    <button className="btn-action btn-delete" onClick={() => handleDelete(skill)}>Eliminar(DELETE)</button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* MODAL UNIVERSAL PARA ADMIN Y USER */}
        {showModal && (
          <div className="modal-overlay">
            <div className="modal-content">
              {modalType === 'purchase' ? (
                <>
                  <h2>Confirmar Pedido de Habilidad</h2>
                  <p>Has seleccionado <strong>{selectedSkill.skill_name}</strong>.</p>
                  <div className="modal-actions">
                    <button className="btn-cancel" onClick={() => setShowModal(false)}>Cancelar</button>
                    <button className="btn-confirm" onClick={confirmPurchase}>Confirmar Adquisición</button>
                  </div>
                </>
              ) : (
                <form onSubmit={handleAdminSubmit}>
                  <h2>{modalType === 'create' ? 'Nueva Habilidad' : 'Editar Habilidad'}</h2>
                  <div className="form-group" style={{marginTop: '20px'}}>
                    <label>Nombre:</label>
                    <input type="text" value={formData.skill_name} onChange={e => setFormData({...formData, skill_name: e.target.value})} required/>
                  </div>
                  <div className="form-group">
                    <label>Nivel de dificultad (1=Básico, 2=Int, 3=Ava):</label>
                    <input type="number" value={formData.difficulty_level} onChange={e => setFormData({...formData, difficulty_level: parseInt(e.target.value)})} required/>
                  </div>
                  <div className="form-group">
                    <label>Stock:</label>
                    <input type="number" value={formData.stock} onChange={e => setFormData({...formData, stock: parseInt(e.target.value)})} required/>
                  </div>
                  <div className="modal-actions">
                    <button type="button" className="btn-cancel" onClick={() => setShowModal(false)}>Cancelar</button>
                    <button type="submit" className="btn-submit">{modalType === 'create' ? 'Crear (POST)' : 'Guardar (PUT)'}</button>
                  </div>
                </form>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Skills;
