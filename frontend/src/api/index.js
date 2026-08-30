import api from "./client";

export const authApi = {
  login: (username, password) =>
    api.post("/auth/token/", { username, password }),
  register: (data) => api.post("/auth/register/", data),
  me: () => api.get("/auth/me/"),
};

export const benchmarkApi = {
  list: (params) => api.get("/benchmarks/", { params }),
  detail: (code) => api.get(`/benchmarks/${code}/`),
  create: (data) => api.post("/benchmarks/", data),
  rates: (code, params) => api.get(`/benchmarks/${code}/rates/`, { params }),
  createRate: (code, data) => api.post(`/benchmarks/${code}/rates/`, data),
  analytics: () => api.get("/benchmarks/analytics/"),
  types: () => api.get("/benchmarks/types/"),
};

export const reportApi = {
  list: (params) => api.get("/reports/", { params }),
  create: (data) => api.post("/reports/", data),
  detail: (id) => api.get(`/reports/${id}/`),
  generate: (id) => api.post(`/reports/${id}/generate/`),
  export: (id) => api.get(`/reports/${id}/export/`, { responseType: "blob" }),
};