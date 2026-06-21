import { ref } from 'vue'
import { recipeApi } from '@/api/recipe'
import { isAuthenticated } from '@/stores/auth'
import type { Recipe } from '@/types/recipe'
import { ElMessage } from 'element-plus'

const favorites = ref<Recipe[]>([])
const favoriteIds = ref<Set<number>>(new Set())
const isLoading = ref(false)

export function useFavorites() {

  async function fetchFavorites() {
    if (!isAuthenticated.value) return
    isLoading.value = true
    try {
      const response = await recipeApi.getFavorites()
      favorites.value = response.data?.items || []
      favoriteIds.value = new Set(favorites.value.map(r => r.dbId!).filter(Boolean))
    } catch { /* handled by interceptor */ }
    finally { isLoading.value = false }
  }

  async function toggleFavorite(recipe: Recipe) {
    if (!isAuthenticated.value) {
      ElMessage.warning('请先登录后再收藏食谱')
      return
    }
    const dbId = recipe.dbId
    if (!dbId) return

    try {
      if (favoriteIds.value.has(dbId)) {
        await recipeApi.unfavorite(dbId)
        favoriteIds.value.delete(dbId)
        favorites.value = favorites.value.filter(r => r.dbId !== dbId)
        ElMessage.success('已取消收藏')
      } else {
        await recipeApi.favorite(dbId)
        favoriteIds.value.add(dbId)
        favorites.value.unshift(recipe)
        ElMessage.success('已收藏')
      }
    } catch { /* handled by interceptor */ }
  }

  function isFavorite(dbId: number | undefined): boolean {
    if (!dbId) return false
    return favoriteIds.value.has(dbId)
  }

  return {
    favorites,
    favoriteIds,
    isLoading,
    fetchFavorites,
    toggleFavorite,
    isFavorite,
  }
}
