import axios from "axios";
import { useAuthStore } from "@/store/authStore";

const client = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "/api/v1",
    timeout: 15000,
});

client.interceptors.request.use((config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

client.interceptors.response.use(
    (res) => res,
    async (error) => {
        const original = error.config;
        if (error.response?.status === 401 && !original._retry) {
            original._retry = true;
            try {
                const { refreshToken, setTokens } = useAuthStore.getState();
                const { data } = await axios.post(
                    `${import.meta.env.VITE_API_URL}/auth/refresh`,
                    { refresh_token: refreshToken }
                );
                setTokens(data.access_token, data.refresh_token);
                original.headers.Authorization = `Bearer ${data.access_token}`;
                return client(original);
            } catch {
                useAuthStore.getState().logout();
            }
        }
        return Promise.reject(error);
    }
);

export default client;