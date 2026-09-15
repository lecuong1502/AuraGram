// frontend/src/hooks/usePosts.js
import { useInfiniteQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { postsApi } from "@/api/postsApi";

export function useFeed() {
    return useInfiniteQuery({
        queryKey: ["feed"],
        queryFn: ({ pageParam }) => postsApi.getFeed(pageParam),
        getNextPageParam: (lastPage) => lastPage.has_more ? lastPage.next_cursor : undefined,
        initialPageParam: undefined,
    });
}

export function useToggleLike(postId) {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: () => postsApi.toggleLike(postId),
        onMutate: async () => {
            await queryClient.cancelQueries({ queryKey: ["feed"] });
            const prev = queryClient.getQueryData(["feed"]);
            queryClient.setQueryData(["feed"], (old) => ({
                ...old,
                pages: old.pages.map((page) => ({
                    ...page,
                    posts: page.posts.map((p) =>
                        p.id === postId
                            ? { ...p, like_count: p.liked ? p.like_count - 1 : p.like_count + 1, liked: !p.liked }
                            : p
                    ),
                })),
            }));
            return { prev };
        },
        onError: (_err, _vars, ctx) => {
            queryClient.setQueryData(["feed"], ctx.prev);
        },
    });
}

export function useCreatePost() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: ({ caption, files }) => postsApi.createPost(caption, files),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["feed"] }),
    });
}