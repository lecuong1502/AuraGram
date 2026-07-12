import client from "./client";

export const postsApi = {
    getFeed: (cursor) =>
        client.get("/posts/feed", { params: { cursor } }).then((r) => r.data),
    getPost: (postId) => client.get(`/posts/${postId}`).then((r) => r.data),
    createPost: (caption, files) => {
        const form = new FormData();
        form.append("caption", caption);
        files.forEach((f) => form.append("files", f));
        return client.post("/posts", form).then((r) => r.data);
    },
    deletePost: (postId) => client.delete(`/posts/${postId}`),
    toggleLike: (postId) => client.post(`/posts/${postId}/like`).then((r) => r.data),
};