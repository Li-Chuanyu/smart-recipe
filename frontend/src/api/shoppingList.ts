import { get, post, put, del } from './client'
import type { ShoppingList, ShoppingItem } from '@/types/shoppingList'

export const shoppingListApi = {
  getLists: () => get<ShoppingList[]>('/shopping-lists'),

  getList: (id: number) => get<ShoppingList>(`/shopping-lists/${id}`),

  createList: (data: { name: string }) => post<ShoppingList>('/shopping-lists', data),

  deleteList: (id: number) => del<null>(`/shopping-lists/${id}`),

  toggleCheck: (listId: number, itemId: number) =>
    put<ShoppingItem>(`/shopping-lists/${listId}/items/${itemId}/check`),

  removeItem: (listId: number, itemId: number) =>
    del<null>(`/shopping-lists/${listId}/items/${itemId}`),

  generateFromMealPlan: (mealPlanId: number, listName?: string) =>
    post<ShoppingList>('/shopping-lists/generate-from-meal-plan', {
      meal_plan_id: mealPlanId,
      list_name: listName,
    }),

  generateFromRecipes: (recipeIds: number[], listName?: string) =>
    post<ShoppingList>('/shopping-lists/generate-from-recipes', {
      recipe_ids: recipeIds,
      list_name: listName,
    }),
}
