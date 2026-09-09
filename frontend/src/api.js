const API_BASE = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

export function fetchDashboard() {
  return request("/api/dashboard");
}

export function fetchAssessments() {
  return request("/api/assessments");
}

export function createAssessment(payload) {
  return request("/api/assessments", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
