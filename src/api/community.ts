import { get, post, put, del } from './client'
import type { CommunityPost, Comment, PaginatedData } from '@/types/api'

export const communityApi = {
  getPosts: (params?: { page?: number; sort?: string; keyword?: string }) =>
    get<PaginatedData<CommunityPost>>('/community/posts', params),
  getPost: (id: number) => get<CommunityPost>(`/community/posts/${id}`),
  createPost: (data: { title: string; content: string; images?: string[]; recipe_id?: number }) =>
    post<CommunityPost>('/community/posts', data),
  updatePost: (id: number, data: Partial<CommunityPost>) => put<CommunityPost>(`/community/posts/${id}`, data),
  deletePost: (id: number) => del<null>(`/community/posts/${id}`),
  like: (id: number) => post<{ liked: boolean }>(`/community/posts/${id}/like`),
  getComments: (postId: number) => get<Comment[]>(`/community/posts/${postId}/comments`),
  createComment: (postId: number, content: string, parentId?: number) =>
    post<Comment>(`/community/posts/${postId}/comments`, { content, parent_id: parentId }),
  deleteComment: (commentId: number) => del<null>(`/community/comments/${commentId}`),
}
