import type { Recipe } from './recipe'

export type MealType = 'breakfast' | 'lunch' | 'dinner'
export type DayOfWeek = 0 | 1 | 2 | 3 | 4 | 5 | 6

export interface MealPlanEntry {
  id?: number
  mealPlanId?: number
  recipeId: number
  recipe?: Recipe
  dayOfWeek: DayOfWeek
  mealType: MealType
  notes?: string
}

export interface MealPlan {
  id: number
  userId?: number
  name: string
  weekStart: string
  entries: MealPlanEntry[]
  createdAt?: string
}

export const DAY_LABELS: Record<number, string> = {
  0: '周一', 1: '周二', 2: '周三', 3: '周四',
  4: '周五', 5: '周六', 6: '周日',
}

export const MEAL_LABELS: Record<MealType, string> = {
  breakfast: '早餐',
  lunch: '午餐',
  dinner: '晚餐',
}

export const MEAL_ICONS: Record<MealType, string> = {
  breakfast: '🌅',
  lunch: '☀️',
  dinner: '🌙',
}
