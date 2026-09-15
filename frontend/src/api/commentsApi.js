// frontend/src/api/commentsApi.js
import client from "./client";

export const commentsApi = {
  list: (postId, params) => client.get(`/posts/${postId}/comments`, { params }).then((r) => r.data),
  add: (postId, content) => client.post(`/posts/${postId}/comments`, { content }).then((r) => r.data),
  remove: (postId, commentId) => client.delete(`/posts/${postId}/comments/${commentId}`),
  addReply: (postId, commentId, data) =>
    client.post(`/posts/${postId}/comments/${commentId}/replies`, data).then((r) => r.data),
};