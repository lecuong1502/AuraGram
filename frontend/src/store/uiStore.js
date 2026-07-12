import { create } from "zustand";

export const useUiStore = create((set) => ({
    // Upload Modal
    uploadModalOpen: false,
    openUploadModal: () => set({ uploadModalOpen: true }),
    closeUploadModal: () => set({ uploadModalOpen: false }),

    // Toast notifications
    toasts: [],
    addToast: (message, type = "info") =>
        set((s) => ({
            toasts: [...s.toasts, { id: Date.now(), message, type }],
        })),
    removeToast: (id) =>
        set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}));