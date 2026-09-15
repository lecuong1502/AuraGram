// frontend/src/hooks/useProfile.js
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { usersApi } from "@/api/usersApi";

export function useProfile(username) {
    return useQuery({
        queryKey: ["profile", username],
        queryFn: () => usersApi.getProfile(username),
        enabled: !!username,
    });
}

export function useFollow(userId) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ isFollowing }) =>
            isFollowing ? usersApi.unfollow(userId) : usersApi.follow(userId),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["profile"] }),
    });
}

export function useUpdateProfile() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: usersApi.updateProfile,
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["me"] }),
    });
}