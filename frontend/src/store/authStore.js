import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useAuthStore = create(
    persist(
        (set) => ({
            accessToken: null,
            refreshToken: null,
            user: null,

            setTokens: (accessToken, refreshToken) =>
                set({ accessToken, refreshToken }),

            setUser: (user) => set({ user }),

            logout: () =>
                set({ accessToken: null, refreshToken: null, user: null }),
        }),
        {
            name: "auragram-auth",
            // Only persist tokens — user data is always re-fetched
            partialize: (state) => ({
                accessToken: state.accessToken,
                refreshToken: state.refreshToken,
            }),
        }
    )
);