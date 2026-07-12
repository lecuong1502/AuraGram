import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { authApi } from "@/api/auth.api";
import { usersApi } from "@/api/users.api";
import { useAuthStore } from "@/store/authStore";

export function useMe() {
    const accessToken = useAuthStore((s) => s.accessToken);
    return useQuery({
        queryKey: ["me"],
        queryFn: usersApi.getMe,
        enabled: !!accessToken,
        staleTime: 5 * 60 * 1000,
    });
}

export function useLogin() {
    const { setTokens } = useAuthStore();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: authApi.login,
        onSuccess: (data) => {
            setTokens(data.access_token, data.refresh_token);
            queryClient.invalidateQueries({ queryKey: ["me"] });
        },
    });
}

export function useRegister() {
    const { setTokens } = useAuthStore();

    return useMutation({
        mutationFn: authApi.register,
        onSuccess: (data) => {
            setTokens(data.access_token, data.refresh_token);
        },
    });
}

export function useLogout() {
    const { logout } = useAuthStore();
    const queryClient = useQueryClient();
    const navigate = useNavigate();

    return useMutation({
        mutationFn: authApi.logout,
        onSettled: () => {
            logout();
            queryClient.clear();
            navigate("/login");
        },
    });
}