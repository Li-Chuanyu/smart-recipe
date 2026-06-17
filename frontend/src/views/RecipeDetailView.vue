<template>
  <div class="recipe-detail-page">
    <div class="container" v-loading="loading">
      <div v-if="recipe" class="detail-content">
        <!-- Back button -->
        <el-button text @click="$router.back()" class="back-btn">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>

        <!-- Header -->
        <div class="detail-header">
          <div class="detail-image">
            <img v-if="recipe.imageUrl" :src="recipe.imageUrl" :alt="recipe.title" />
            <div v-else class="gradient-placeholder" :class="dietClass">
              <span>{{ dietEmoji }}</span>
            </div>
          </div>
          <div class="detail-info">
            <div class="detail-tags">
              <el-tag :color="dietColor" effect="dark">{{ recipe.dietType }}</el-tag>
              <el-tag type="info" effect="plain">{{ recipe.difficulty }}</el-tag>
            </div>
            <h1>{{ recipe.title }}</h1>
            <p class="detail-desc">{{ recipe.description }}</p>
            <div class="detail-meta-row">
              <span><el-icon><Clock /></el-icon> {{ recipe.cookingTime }}</span>
              <span><el-icon><User /></el-icon> {{ recipe.servings }}人份</span>
            </div>
            <!-- Rating -->
            <div v-if="recipe.avgRating || isAuthenticated" class="detail-rating-row">
              <StarRating
                :model-value="recipe.avgRating ?? 0"
                :rating-count="recipe.ratingCount"
                readonly
                size="default"
              />
              <span v-if="isAuthenticated" class="my-rating-section">
                我的评分：
                <StarRating
                  :model-value="userScore"
                  :readonly="false"
                  size="default"
                  :show-label="false"
                  @update:model-value="submitRating"
                />
                <el-button v-if="userScore > 0" text size="small" type="danger" @click="clearMyRating">清除</el-button>
              </span>
            </div>
            <div class="detail-actions">
              <el-button type="primary" @click="toggleFav(recipe)">
                <el-icon><StarFilled v-if="isLiked" /><Star v-else /></el-icon>
                {{ isLiked ? '取消收藏' : '收藏食谱' }}
              </el-button>
              <el-button @click="copyRecipe">
                <el-icon><DocumentCopy /></el-icon> 复制食谱
              </el-button>
            </div>
          </div>
        </div>

        <el-divider />

        <!-- Body -->
        <div class="detail-body">
          <section>
            <h2>📋 食材清单</h2>
            <div class="ingredient-grid">
              <div v-for="(ing, idx) in recipe.ingredients" :key="idx" class="ingredient-item">
                <span class="ing-name">{{ ing.name }}</span>
                <span class="ing-amount">{{ ing.amount }}</span>
                <span v-if="ing.notes" class="ing-notes">{{ ing.notes }}</span>
              </div>
            </div>
          </section>

          <section>
            <h2>📝 烹饪步骤</h2>
            <div class="steps-list">
              <div v-for="step in recipe.steps" :key="step.stepNumber" class="step-card">
                <span class="step-number">{{ step.stepNumber }}</span>
                <p>{{ step.instruction }}</p>
              </div>
            </div>
          </section>

          <section>
            <h2>📊 营养信息</h2>
            <div class="nutrition-grid">
              <div v-for="item in nutritionItems" :key="item.label" class="nutrition-card">
                <span class="nutri-val">{{ item.value || '--' }}</span>
                <span class="nutri-label">{{ item.label }}</span>
              </div>
            </div>
          </section>

          <el-alert
            v-if="recipe.tips"
            :title="recipe.tips"
            type="success"
            :closable="false"
            show-icon
          />
        </div>
      </div>

      <!-- Not found -->
      <EmptyState
        v-else-if="!loading"
        icon="🔍"
        title="食谱未找到"
        description="该食谱可能已被删除或不存在"
        action-text="浏览食谱库"
        @action="$router.push('/recipes')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { recipeApi } from '@/api/recipe'
import { useFavorites } from '@/composables/useFavorites'
import { useCopyToClipboard } from '@/composables/useCopyToClipboard'
import EmptyState from '@/components/common/EmptyState.vue'
import StarRating from '@/components/common/StarRating.vue'
import type { Recipe } from '@/types/recipe'
import { ArrowLeft, Clock, User, Star, StarFilled, DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const { toggleFavorite: toggleFav, isFavorite } = useFavorites()
const { copyText, formatRecipeText } = useCopyToClipboard()

const recipe = ref<Recipe | null>(null)
const loading = ref(true)
const userScore = ref(0)

const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))
const isLiked = computed(() => isFavorite(recipe.value?.dbId))

const dietClass = computed(() => {
  const m: Record<string, string> = { '减脂': 'diet-jianzhi', '家常': 'diet-home', '儿童餐': 'diet-kids', '素食': 'diet-veggie', '不限': 'diet-default' }
  return m[recipe.value?.dietType || ''] || 'diet-default'
})
const dietEmoji = computed(() => {
  const m: Record<string, string> = { '减脂': '🥗', '家常': '🍳', '儿童餐': '🍱', '素食': '🥬', '不限': '🍽️' }
  return m[recipe.value?.dietType || ''] || '🍽️'
})
const dietColor = computed(() => {
  const m: Record<string, string> = { '减脂': '#67C23A', '家常': '#FF6B35', '儿童餐': '#E6A23C', '素食': '#409EFF' }
  return m[recipe.value?.dietType || ''] || '#909399'
})
const nutritionItems = computed(() => {
  const n = recipe.value?.nutrition
  if (!n) return []
  return [
    { label: '热量', value: n.calories },
    { label: '蛋白质', value: n.protein },
    { label: '碳水', value: n.carbs },
    { label: '脂肪', value: n.fat },
    { label: '膳食纤维', value: n.fiber },
  ]
})

function copyRecipe() {
  if (recipe.value) copyText(formatRecipeText(recipe.value))
}

async function fetchMyRating() {
  if (!recipe.value?.dbId || !isAuthenticated.value) return
  try {
    const res = await recipeApi.getMyRating(recipe.value.dbId)
    userScore.value = res.data?.score ?? 0
  } catch { userScore.value = 0 }
}

async function submitRating(score: number) {
  if (!recipe.value?.dbId) return
  try {
    const res = await recipeApi.rate(recipe.value.dbId, score)
    userScore.value = res.data?.userScore ?? score
    if (recipe.value) {
      recipe.value.avgRating = res.data?.avgRating
      recipe.value.ratingCount = res.data?.ratingCount
    }
    ElMessage.success('评分成功')
  } catch { /* handled */ }
}

async function clearMyRating() {
  if (!recipe.value?.dbId) return
  try {
    const res = await recipeApi.deleteRating(recipe.value.dbId)
    userScore.value = 0
    if (recipe.value && res.data) {
      recipe.value.avgRating = res.data.avgRating
      recipe.value.ratingCount = res.data.ratingCount
    }
    ElMessage.success('已取消评分')
  } catch { /* handled */ }
}

onMounted(async () => {
  try {
    const id = route.params.id
    const { data } = await recipeApi.getDetail(id as string)
    recipe.value = data
    await fetchMyRating()
  } catch {
    recipe.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.recipe-detail-page {
  padding: 32px 0 64px;
}

.detail-content {
  max-width: 900px;
  margin: 0 auto;
}

.back-btn {
  margin-bottom: 20px;
}

.detail-header {
  display: flex;
  gap: 32px;
  margin-bottom: 24px;

  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
  }
}

.detail-image {
  width: 400px;
  flex-shrink: 0;
  border-radius: $radius-xl;
  overflow: hidden;

  img {
    width: 100%;
    aspect-ratio: 4/3;
    object-fit: cover;
  }

  @media (max-width: $breakpoint-sm) {
    width: 100%;
  }
}

.detail-info {
  flex: 1;

  h1 {
    font-size: $font-size-3xl;
    font-weight: 700;
    margin: 12px 0 8px;
  }
}

.detail-tags {
  display: flex;
  gap: 8px;
}

.detail-desc {
  color: $color-text-secondary;
  font-size: $font-size-md;
  margin-bottom: 12px;
}

.detail-meta-row {
  display: flex;
  gap: 20px;
  color: $color-text-secondary;
  margin-bottom: 20px;

  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.detail-actions {
  display: flex;
  gap: 12px;
}

.detail-rating-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding: 8px 0;

  .my-rating-section {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: $font-size-sm;
    color: var(--app-text-secondary, $color-text-secondary);
  }
}

.detail-body {
  section {
    margin-bottom: 32px;

    h2 {
      font-size: $font-size-xl;
      font-weight: 600;
      margin-bottom: 16px;
    }
  }
}

.ingredient-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;

  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.ingredient-item {
  display: flex;
  gap: 8px;
  padding: 8px 16px;
  background: var(--app-bg-gray, $color-bg-gray);
  border-radius: $radius-sm;
  font-size: $font-size-base;

  .ing-name { font-weight: 600; }
  .ing-amount { color: $color-primary; }
  .ing-notes { color: $color-text-secondary; font-size: $font-size-sm; }
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-card {
  display: flex;
  gap: 16px;
  padding: 16px 20px;
  background: var(--app-bg-warm, $color-bg-warm);
  border-radius: $radius-md;
  border-left: 4px solid $color-primary;

  .step-number {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $color-primary;
    color: #fff;
    border-radius: 50%;
    font-weight: 700;
  }

  p {
    font-size: $font-size-base;
    line-height: 1.8;
  }
}

.nutrition-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;

  @media (max-width: $breakpoint-sm) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.nutrition-card {
  text-align: center;
  padding: 16px;
  background: var(--app-bg-warm, $color-bg-warm);
  border-radius: $radius-md;

  .nutri-val {
    display: block;
    font-size: $font-size-lg;
    font-weight: 700;
    color: $color-primary;
  }

  .nutri-label {
    display: block;
    font-size: $font-size-sm;
    color: $color-text-secondary;
    margin-top: 4px;
  }
}
</style>
