// Mock data para usuarios
export const usersData = [
  { id: 1, name: 'Juan García', email: 'juan@example.com', role: 'Estudiante', skills: 5 },
  { id: 2, name: 'María López', email: 'maria@example.com', role: 'Estudiante', skills: 8 },
  { id: 3, name: 'Carlos Rodríguez', email: 'carlos@example.com', role: 'Instructor', skills: 15 },
];

// Mock data para habilidades sociales
export const skillsData = [
  { id: 1, name: 'Empatía', difficulty: 'Básico', stock: 50, xp: 10 },
  { id: 2, name: 'Liderazgo', difficulty: 'Intermedio', stock: 30, xp: 25 },
  { id: 3, name: 'Comunicación Asertiva', difficulty: 'Intermedio', stock: 40, xp: 20 },
  { id: 4, name: 'Escucha Activa', difficulty: 'Básico', stock: 60, xp: 15 },
  { id: 5, name: 'Creatividad', difficulty: 'Avanzado', stock: 20, xp: 35 },
  { id: 6, name: 'Resiliencia', difficulty: 'Avanzado', stock: 25, xp: 30 },
  { id: 7, name: 'Colaboración', difficulty: 'Intermedio', stock: 45, xp: 18 },
  { id: 8, name: 'Paciencia', difficulty: 'Básico', stock: 55, xp: 12 },
  { id: 9, name: 'Confianza', difficulty: 'Intermedio', stock: 35, xp: 22 },
  { id: 10, name: 'Adaptabilidad', difficulty: 'Avanzado', stock: 28, xp: 32 },
  { id: 11, name: 'Iniciativa', difficulty: 'Intermedio', stock: 38, xp: 24 },
  { id: 12, name: 'Amistad', difficulty: 'Básico', stock: 70, xp: 8 },
  { id: 13, name: 'Humor', difficulty: 'Básico', stock: 65, xp: 10 },
  { id: 14, name: 'Respeto', difficulty: 'Básico', stock: 80, xp: 12 },
  { id: 15, name: 'Sagacidad', difficulty: 'Avanzado', stock: 22, xp: 40 },
];

// Mock data para pedidos
export const ordersData = [
  { id: 1, userId: 1, skillId: 1, skillName: 'Empatía', status: 'Completado', date: '2024-04-15' },
  { id: 2, userId: 2, skillId: 3, skillName: 'Comunicación Asertiva', status: 'Completado', date: '2024-04-16' },
  { id: 3, userId: 1, skillId: 5, skillName: 'Creatividad', status: 'Pendiente', date: '2024-04-18' },
  { id: 4, userId: 3, skillId: 2, skillName: 'Liderazgo', status: 'Completado', date: '2024-04-17' },
  { id: 5, userId: 2, skillId: 6, skillName: 'Resiliencia', status: 'En progreso', date: '2024-04-18' },
];
