<template>
  <div class="generate-page">
    <div class="container">
      <div class="page-header">
        <h1>🤖 AI 智能食谱生成</h1>
        <p>填写你的需求，让 AI 为你定制专属食谱</p>
      </div>

      <div class="generate-layout">
        <!-- Left: Form -->
        <div class="generate-form-col">
          <RecipeForm
            :form-params="formParams"
            :is-generating="generationState === 'generating'"
            @submit="generate"
          />
        </div>

        <!-- Right: Results -->
        <div class="generate-result-col">
          <!-- Idle state -->
          <div v-if="generationState === 'idle'" class="result-placeholder">
            <div class="placeholder-icon">🍽️</div>
            <h3>填写左侧表单</h3>
            <p>AI 将根据你的需求生成专属食谱</p>
          </div>

          <!-- Generating -->
          <div v-else-if="generationState === 'generating'" class="generating-state">
            <el-skeleton animated>
              <template #template>
                <div v-for="i in formParams.recipeCount" :key="i" style="margin-bottom: 16px;">
                  <el-skeleton-item variant="image" style="width: 100%; height: 160px;" />
                  <div style="padding: 14px;">
                    <el-skeleton-item variant="text" style="width: 60%;" />
                    <el-skeleton-item variant="text" style="width: 80%;" />
                  </div>
                </div>
              </template>
            </el-skeleton>
            <p class="generating-hint">
              <el-icon class="is-loading"><Loading /></el-icon> AI 正在为你创作食谱，请稍候...
            </p>
          </div>

          <!-- Success -->
          <div v-else-if="generationState === 'success'" class="result-success">
            <div class="result-header">
              <span>✨ 为你生成了 {{ generatedRecipes.length }} 份食谱</span>
              <el-button text type="primary" @click="resetForm">重新生成</el-button>
            </div>
            <div class="recipe-grid">
              <RecipeCard
                v-for="recipe in generatedRecipes"
                :key="recipe.id"
                :recipe="recipe"
                :is-liked="isFavorite(recipe.dbId)"
                @click="openDetail(recipe)"
                @toggle-favorite="toggleFavorite"
              />
            </div>
          </div>

          <!-- Error -->
          <div v-else-if="generationState === 'error'" class="result-error">
            <ErrorState
              icon="error"
              title="生成失败"
              :message="generationError"
              retryable
              @retry="generate"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <RecipeDetailModal
      v-model:visible="detailVisible"
      :recipe="selectedRecipe"
      :is-liked="isFavorite(selectedRecipe?.dbId)"
      @toggle-favorite="toggleFavorite"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRecipeGenerate } from '@/composables/useRecipeGenerate'
import { useFavorites } from '@/composables/useFavorites'
import { useCopyToClipboard } from '@/composables/useCopyToClipboard'
import RecipeForm from '@/components/recipe/RecipeForm.vue'
import RecipeCard from '@/components/common/RecipeCard.vue'
import RecipeDetailModal from '@/components/common/RecipeDetailModal.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import type { Recipe } from '@/types/recipe'
import { Loading } from '@element-plus/icons-vue'

const {
  formParams,
  generatedRecipes,
  generationState,
  generationError,
  generate,
  resetForm,
} = useRecipeGenerate()

const { toggleFavorite: toggleFav, isFavorite } = useFavorites()

const detailVisible = ref(false)
const selectedRecipe = ref<Recipe | null>(null)

function openDetail(recipe: Recipe) {
  selectedRecipe.value = recipe
  detailVisible.value = true
}

function toggleFavorite(recipe: Recipe) {
  toggleFav(recipe)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.generate-page {
  padding: 32px 0 64px;
}

.generate-layout {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 32px;
  align-items: start;

  @media (max-width: $breakpoint-md) {
    grid-template-columns: 1fr;
  }
}

.generate-form-col {
  position: sticky;
  top: calc($header-height + 24px);

  @media (max-width: $breakpoint-md) {
    position: static;
  }
}

.generate-result-col {
  min-height: 400px;
}

.result-placeholder {
  text-align: center;
  padding: 80px 24px;
  background: var(--app-card-bg, #fff);
  border-radius: $radius-xl;
  box-shadow: $shadow-sm;

  .placeholder-icon {
    font-size: 72px;
    margin-bottom: 16px;
  }

  h3 {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $color-text-primary;
    margin-bottom: 8px;
  }

  p {
    color: $color-text-secondary;
  }
}

.generating-state {
  background: var(--app-card-bg, #fff);
  padding: 24px;
  border-radius: $radius-xl;
  box-shadow: $shadow-sm;
}

.generating-hint {
  text-align: center;
  padding: 24px;
  color: $color-text-secondary;
  font-size: $font-size-md;
}

.result-success {
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    font-size: $font-size-md;
    font-weight: 600;
    color: $color-text-primary;
  }
}

.result-error {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-xl;
  box-shadow: $shadow-sm;
}
</style>
