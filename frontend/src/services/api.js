/**
 * Q-Guard API Service Layer.
 * Interacts with FastAPI backend endpoints.
 */

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL || '';
const BASE_URL = rawBaseUrl.replace(/\/+$/, '');

function buildUrl(endpoint) {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${BASE_URL}${cleanEndpoint}`;
}

async function fetchJson(endpoint, options = {}) {
  const url = buildUrl(endpoint);
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    });

    if (!response.ok) {
      let errorMessage = `HTTP error ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (_) {}
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  getHealth: () => fetchJson('/api/health'),
  getProcessors: () => fetchJson('/api/processors'),
  getProcessor: (id) => fetchJson(`/api/processors/${id}`),
  getExperiments: (limit = 100) => fetchJson(`/api/experiments?limit=${limit}`),
  getExperimentById: (id) => fetchJson(`/api/experiments/${id}`),
  runExperiment: (payload) =>
    fetchJson('/api/experiments', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  runAllExperiments: () =>
    fetchJson('/api/experiments/run-all', {
      method: 'POST',
    }),
  getSummary: () => fetchJson('/api/results/summary'),
  getExportCsvUrl: () => buildUrl('/api/results/export'),
};
