import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuración de la prueba de estrés
export const options = {
  stages: [
    { duration: '20s', target: 40 }, // Sube poco a poco a 40 usuarios virtuales
    { duration: '60s', target: 100 }, // Mantiene 100 usuarios atacando durante 60s
    { duration: '10s', target: 0 },  // Reduce a 0 usuarios (enfriamiento)
  ],
};

export default function () {
  let resOrders = http.get('http://localhost:8005/docs');
  check(resOrders, { 'Orders respondió bien': (r) => r.status === 200 })
  let resAuth = http.get('http://localhost:8006/health');
  check(resAuth, { 'Auth respondió bien': (r) => r.status === 200 });
  sleep(0.1); 
}