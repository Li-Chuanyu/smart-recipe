import { get, post, put, del } from './client'
import type { Recipe, RecipeFormParams } from '@/types/recipe'
import type { PaginatedData, Category, RatingInfo } from '@/types/api'

export interface RecipeFilter {
  keyword?: string
  dietType?: string
  difficulty?: string
  categoryId?: number
  page?: number
  perPage?: number
}

export const recipeApi = {
  // AI generation
  generate: (params: RecipeFormParams) => post<Recipe[]>('/recipes/generate', params),

  // Recipe CRUD
  getList: (filter?: RecipeFilter) => get<PaginatedData<Recipe>>('/recipes', filter),
  getDetail: (id: number | string) => get<Recipe>(`/recipes/${id}`),
  create: (recipe: Partial<Recipe>) => post<Recipe>('/recipes', recipe),
  update: (id: number, recipe: Partial<Recipe>) => put<Recipe>(`/recipes/${id}`, recipe),
  delete: (id: number) => del<null>(`/recipes/${id}`),

  // Favorites
  favorite: (id: number) => post<null>(`/recipes/${id}/favorite`),
  unfavorite: (id: number) => del<null>(`/recipes/${id}/favorite`),
  getFavorites: (page = 1) => get<PaginatedData<Recipe>>('/recipes/favorites', { page }),

  // Ratings
  rate: (id: number, score: number) => post<RatingInfo>(`/recipes/${id}/rate`, { score }),
  getMyRating: (id: number) => get<{ score: number | null }>(`/recipes/${id}/my-rating`),
  deleteRating: (id: number) => del<RatingInfo>(`/recipes/${id}/rate`),

  // Categories
  getCategories: () => get<Category[]>('/recipes/categories'),
}
