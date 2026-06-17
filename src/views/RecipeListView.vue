<template>
  <div class="recipe-list-page">
    <div class="container">
      <div class="page-header">
        <h1>📖 食谱浏览</h1>
        <p>探索 AI 生成的各种食谱</p>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <el-input v-model="filters.keyword" placeholder="搜索食谱名称、食材、标签..." clearable prefix-icon="Search" style="width: 300px;" @input="searchRecipes" />
        <el-select v-model="filters.dietType" placeholder="饮食类型" clearable style="width: 140px;" @change="searchRecipes">
          <el-option v-for="d in DIET_TYPES" :key="d.value" :label="d.label" :value="d.value" />
        </el-select>
        <el-select v-model="filters.difficulty" placeholder="难度" clearable style="width: 120px;" @change="searchRecipes">
          <el-option v-for="d in DIFFICULTY_OPTIONS" :key="d.value" :label="d.label" :value="d.value" />
        </el-select>
      </div>

      <!-- Results -->
      <div v-if="recipes.length && !loading" class="recipe-grid mt-xl">
        <RecipeCard
          v-for="recipe in recipes"
          :key="recipe.id"
          :recipe="recipe"
          :is-liked="isFavorite(recipe.dbId)"
          @click="$router.push(`/recipe/${recipe.dbId || recipe.id}`)"
          @toggle-favorite="toggleFavorite"
        />
      </div>

      <EmptyState
        v-if="!recipes.length && !loading"
        icon="🔍"
        title="暂无食谱"
        description="试试调整搜索条件或去生成新食谱"
        action-text="去生成食谱"
        @action="$router.push('/generate')"
      />

      <div v-if="total > perPage" class="pagination-wrap mt-xl text-center">
        <el-pagination
          v-model:current-page="page"
          :page-size="perPage"
          :total="total"
          layout="prev, pager, next"
          @current-change="searchRecipes"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { recipeApi } from '@/api/recipe'
import { useFavorites } from '@/composables/useFavorites'
import RecipeCard from '@/components/common/RecipeCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import type { Recipe } from '@/types/recipe'
import { DIET_TYPES, DIFFICULTY_OPTIONS } from '@/types/recipe'

const filters = reactive({ keyword: '', dietType: '', difficulty: '' })
const recipes = ref<Recipe[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = 12
const total = ref(0)
const { toggleFavorite, isFavorite } = useFavorites()

async function searchRecipes() {
  loading.value = true
  try {
    const { data } = await recipeApi.getList({
      keyword: filters.keyword || undefined,
      dietType: filters.dietType || undefined,
      difficulty: filters.difficulty || undefined,
      page: page.value,
      perPage,
    })
    recipes.value = data?.items || []
    total.value = data?.total || 0
  } catch { recipes.value = [] } finally { loading.value = false }
}

onMounted(() => searchRecipes())
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.recipe-list-page {
  padding: 32px 0 64px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;

  @media (max-width: $breakpoint-sm) {
    :deep(.el-input), :deep(.el-select) {
      width: 100% !important;
    }
  }
}

.pagination-wrap {
  display: flex;
  justify-content: center;
}
</style>
