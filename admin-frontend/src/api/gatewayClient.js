import axiosInstance from './axiosConfig';

export const createGatewayRequest = (eventType, payload = {}) =>
  axiosInstance.post('/gateway/request', { event_type: eventType, payload });

export const getGatewayResult = (requestId) =>
  axiosInstance.get(`/gateway/result/${requestId}`);

export const requestAndWait = async (eventType, payload = {}, timeoutMs = 10000, interval = 500) => {
  const { data } = await createGatewayRequest(eventType, payload);
  const requestId = data?.request_id;
  if (!requestId) throw new Error('No request_id from gateway');

  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await getGatewayResult(requestId);
      const body = res.data;
      if (body && body.status && body.status !== 'pending') {
        return body; // { request_id, status, payload, created_at, completed_at }
      }
    } catch (err) {
      // ignore 404 while waiting
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error('Gateway request timed out');
};

export default { createGatewayRequest, getGatewayResult, requestAndWait };
