import client from "./client";

export const notificationsApi = {
    list: (params) => client.get("/notifications", { params }).then((r) => r.data),
    markAllRead: () => client.post("/notifications/read-all"),
};