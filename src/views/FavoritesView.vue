<template>
  <div class="favorites-page">
    <div class="container">
      <div class="page-header">
        <h1>⭐ 我的收藏</h1>
        <p>你收藏的所有食谱</p>
      </div>

      <!-- Filter -->
      <RecipeFilterBar
        v-if="favorites.length"
        v-model:keyword="keyword"
        v-model:dietType="dietType"
        v-model:difficulty="difficulty"
        :sortBy="sortBy"
        @update:sortBy="sortBy = $event"
      />

      <!-- Recipe Grid -->
      <div v-if="filteredRecipes.length" class="recipe-grid mt-xl">
        <RecipeCard
          v-for="recipe in filteredRecipes"
          :key="recipe.id"
          :recipe="recipe"
          :is-liked="true"
          @click="$router.push(`/recipe/${recipe.dbId || recipe.id}`)"
          @toggle-favorite="toggleFavorite"
        />
      </div>

      <EmptyState
        v-if="!favorites.length && !isLoading"
        icon="⭐"
        title="还没有收藏食谱"
        description="浏览或生成食谱后，点击收藏即可保存到这里"
        action-text="去生成食谱"
        @action="$router.push('/generate')"
      />

      <EmptyState
        v-if="favorites.length && !filteredRecipes.length"
        icon="🔍"
        title="没有匹配的食谱"
        description="试试调整筛选条件"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useFavorites } from '@/composables/useFavorites'
import RecipeCard from '@/components/common/RecipeCard.vue'
import RecipeFilterBar from '@/components/recipe/RecipeFilterBar.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const keyword = ref('')
const dietType = ref('')
const difficulty = ref('')
const sortBy = ref('newest')

const { favorites, isLoading, fetchFavorites, toggleFavorite } = useFavorites()

const filteredRecipes = computed(() => {
  let result = [...favorites.value]
  if (keyword.value) {
    const kw = keyword.value.toLowerCase()
    result = result.filter(r =>
      r.title.toLowerCase().includes(kw) ||
      r.tags?.some(t => t.toLowerCase().includes(kw)) ||
      r.ingredients?.some(i => i.name.toLowerCase().includes(kw))
    )
  }
  if (dietType.value) {
    result = result.filter(r => r.dietType === dietType.value)
  }
  if (difficulty.value) {
    result = result.filter(r => r.difficulty === difficulty.value)
  }
  if (sortBy.value === 'newest') {
    result.sort((a, b) => new Date(b.savedAt || 0).getTime() - new Date(a.savedAt || 0).getTime())
  } else if (sortBy.value === 'oldest') {
    result.sort((a, b) => new Date(a.savedAt || 0).getTime() - new Date(b.savedAt || 0).getTime())
  } else if (sortBy.value === 'title') {
    result.sort((a, b) => a.title.localeCompare(b.title))
  }
  return result
})

onMounted(() => fetchFavorites())
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.favorites-page {
  padding: 32px 0 64px;
}
</style>
