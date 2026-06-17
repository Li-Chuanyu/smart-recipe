import { get, post, del } from './client'
import type { MealPlan, MealPlanEntry } from '@/types/mealPlan'
import type { PaginatedData } from '@/types/api'

export const mealPlanApi = {
  getPlans: (page = 1) => get<PaginatedData<MealPlan>>('/meal-plans', { page }),

  getPlanByWeek: (weekStart: string) => get<MealPlan | null>('/meal-plans', { week_start: weekStart }),

  getPlan: (id: number) => get<MealPlan>(`/meal-plans/${id}`),

  createPlan: (data: { name?: string; week_start: string }) =>
    post<MealPlan>('/meal-plans', data),

  deletePlan: (id: number) => del<null>(`/meal-plans/${id}`),

  addEntry: (planId: number, entry: { recipe_id: number; day_of_week: number; meal_type: string; notes?: string }) =>
    post<MealPlanEntry>(`/meal-plans/${planId}/entries`, entry),

  removeEntry: (planId: number, entryId: number) =>
    del<null>(`/meal-plans/${planId}/entries/${entryId}`),
}
