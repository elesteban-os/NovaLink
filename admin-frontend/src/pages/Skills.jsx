import React, { useState, useEffect } from 'react';
import { skillsData } from '../data/mockData';
import './Skills.css';

function Skills() {
  const [skills, setSkills] = useState([]);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [showPurchaseModal, setShowPurchaseModal] = useState(false);

  useEffect(() => {
    setSkills(skillsData);
  }, []);

  const handlePurchase = (skill) => {
    setSelectedSkill(skill);
    setShowPurchaseModal(true);
  };

  const confirmPurchase = () => {
    // Simular compra
    alert(`¡Has adquirido la habilidad "${selectedSkill.name}"!`);
    setShowPurchaseModal(false);
    setSelectedSkill(null);
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'básico': return '#4CAF50';
      case 'intermedio': return '#FF9800';
      case 'avanzado': return '#F44336';
      default: return '#666';
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <h1 className="page-title">Catálogo de Habilidades</h1>
        <p className="page-subtitle">Descubre y adquiere nuevas habilidades sociales</p>

        <div className="skills-catalog">
          {skills.map((skill) => (
            <div key={skill.id} className="skill-item">
              <div className="skill-header">
                <h3>{skill.name}</h3>
                <span
                  className="difficulty-badge"
                  style={{ backgroundColor: getDifficultyColor(skill.difficulty) }}
                >
                  {skill.difficulty}
                </span>
              </div>

              <div className="skill-description">
                <p>Desarrolla tu capacidad de {skill.name.toLowerCase()} y mejora tus relaciones interpersonales.</p>
              </div>

              <div className="skill-footer">
                <div className="xp-info">
                  <span className="xp-points">+{skill.xp} XP</span>
                  <span className="xp-label">puntos de experiencia</span>
                </div>

                <button
                  className="btn-purchase"
                  onClick={() => handlePurchase(skill)}
                  disabled={skill.stock <= 0}
                >
                  {skill.stock > 0 ? 'Adquirir' : 'Agotado'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {showPurchaseModal && selectedSkill && (
          <div className="modal-overlay">
            <div className="modal-content">
              <h2>Confirmar Adquisición</h2>
              <div className="purchase-details">
                <h3>{selectedSkill.name}</h3>
                <p><strong>Dificultad:</strong> {selectedSkill.difficulty}</p>
                <p><strong>Puntos de Experiencia:</strong> +{selectedSkill.xp} XP</p>
                <p className="purchase-note">
                  Al adquirir esta habilidad, fortalecerás tus capacidades sociales y ganarás experiencia valiosa.
                </p>
              </div>

              <div className="modal-actions">
                <button className="btn-cancel" onClick={() => setShowPurchaseModal(false)}>
                  Cancelar
                </button>
                <button className="btn-confirm" onClick={confirmPurchase}>
                  Confirmar Adquisición
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Skills;
