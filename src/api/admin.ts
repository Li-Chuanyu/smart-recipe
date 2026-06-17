import { get, post, put, del } from './client'
import type { AdminStats, Category, UserInfo, PaginatedData } from '@/types/api'
import type { Recipe } from '@/types/recipe'

export const adminApi = {
  getStats: () => get<AdminStats>('/admin/dashboard/stats'),
  getPendingRecipes: (page = 1) => get<PaginatedData<Recipe>>('/admin/recipes/pending', { page }),
  updateRecipeStatus: (id: number, status: string) => put<null>(`/admin/recipes/${id}/status`, { status }),
  setFeatured: (recipeIds: number[]) => post<null>('/admin/recipes/featured', { recipe_ids: recipeIds }),
  getCategories: () => get<Category[]>('/admin/categories'),
  createCategory: (data: Partial<Category>) => post<Category>('/admin/categories', data),
  updateCategory: (id: number, data: Partial<Category>) => put<Category>(`/admin/categories/${id}`, data),
  deleteCategory: (id: number) => del<null>(`/admin/categories/${id}`),
  getUsers: (page = 1) => get<PaginatedData<UserInfo>>('/admin/users', { page }),
  updateUserStatus: (id: number, isActive: boolean) =>
    put<null>(`/admin/users/${id}/status`, { is_active: isActive }),
}
