// frontend/src/api/usersApi.js
import client from "./client";

export const usersApi = {
    getMe: () => client.get("/users/me").then((r) => r.data),
    getProfile: (username) => client.get(`/users/${username}`).then((r) => r.data),
    updateProfile: (data) => client.patch("/users/me", data).then((r) => r.data),
    updateAvatar: (file) => {
        const form = new FormData();
        form.append("file", file);
        return client.post("/users/me/avatar", form).then((r) => r.data);
    },
    follow: (userId) => client.post(`/users/${userId}/follow`),
    unfollow: (userId) => client.delete(`/users/${userId}/follow`),
    search: (q) => client.get("/users/search", { params: { q } }).then((r) => r.data),
};