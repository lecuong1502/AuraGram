// frontend/src/api/authApi.js
import client from "./client";

export const authApi = {
    register: (data) => client.post("/auth/register", data).then((r) => r.data),
    login: (data) => client.post("/auth/login", data).then((r) => r.data),
    logout: () => client.post("/auth/logout"),
    refresh: (token) => client.post("/auth/refresh", { refresh_token: token }).then((r) => r.data),
};