<template>
  <el-dialog
    v-model="dialogVisible"
    :title="recipe?.title || '食谱详情'"
    width="700px"
    :close-on-click-modal="false"
    destroy-on-close
    class="recipe-dialog"
  >
    <template v-if="recipe">
      <!-- Meta bar -->
      <div class="detail-meta">
        <el-tag :color="dietColor" effect="dark">{{ recipe.dietType }}</el-tag>
        <el-tag type="info" effect="plain">{{ recipe.difficulty }}</el-tag>
        <span class="meta-item"><el-icon><Clock /></el-icon> {{ recipe.cookingTime }}</span>
        <span class="meta-item"><el-icon><User /></el-icon> {{ recipe.servings }}人份</span>
      </div>

      <p v-if="recipe.description" class="detail-desc">{{ recipe.description }}</p>

      <!-- Rating bar -->
      <div v-if="isAuthenticated || recipe.avgRating" class="detail-rating-bar">
        <StarRating
          :model-value="recipe.avgRating ?? 0"
          :rating-count="recipe.ratingCount"
          readonly
          size="default"
        />
        <span v-if="isAuthenticated" class="my-rating-hint">
          你的评分：
          <StarRating
            :model-value="userScore"
            :readonly="false"
            size="default"
            :show-label="false"
            @update:model-value="submitRating"
          />
          <el-button v-if="userScore > 0" text size="small" type="danger" @click="clearRating">清除</el-button>
        </span>
      </div>

      <el-divider />

      <!-- Ingredients -->
      <h3 class="section-title">📋 食材清单</h3>
      <div class="ingredient-grid">
        <div v-for="(ing, idx) in recipe.ingredients" :key="idx" class="ingredient-item">
          <span class="ing-name">{{ ing.name }}</span>
          <span class="ing-amount">{{ ing.amount }}</span>
          <span v-if="ing.notes" class="ing-notes">{{ ing.notes }}</span>
        </div>
      </div>

      <el-divider />

      <!-- Steps -->
      <h3 class="section-title">📝 烹饪步骤</h3>
      <div class="steps-list">
        <div v-for="step in recipe.steps" :key="step.stepNumber" class="step-card">
          <span class="step-number">{{ step.stepNumber }}</span>
          <p class="step-text">{{ step.instruction }}</p>
        </div>
      </div>

      <el-divider />

      <!-- Nutrition -->
      <h3 class="section-title">📊 营养信息</h3>
      <div class="nutrition-bars">
        <div v-for="(val, key) in nutritionItems" :key="key" class="nutrition-item">
          <span class="nutrition-label">{{ val.label }}</span>
          <div class="nutrition-bar-bg">
            <div class="nutrition-bar" :style="{ width: val.percent + '%', background: val.color }" />
          </div>
          <span class="nutrition-value">{{ val.value || '--' }}</span>
        </div>
      </div>

      <!-- Tips -->
      <el-alert v-if="recipe.tips" :title="recipe.tips" type="success" :closable="false" show-icon class="mt-lg">
        <template #title>
          <span class="tips-text">💡 {{ recipe.tips }}</span>
        </template>
      </el-alert>
    </template>

    <template #footer>
      <el-button @click="copyRecipe">
        <el-icon><DocumentCopy /></el-icon> 复制食谱
      </el-button>
      <el-button :type="isLiked ? 'warning' : 'default'" @click="toggleFav">
        <el-icon><StarFilled v-if="isLiked" /><Star v-else /></el-icon>
        {{ isLiked ? '取消收藏' : '收藏' }}
      </el-button>
      <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Recipe } from '@/types/recipe'
import { useCopyToClipboard } from '@/composables/useCopyToClipboard'
import { recipeApi } from '@/api/recipe'
import { ElMessage } from 'element-plus'
import { Clock, User, DocumentCopy, Star, StarFilled } from '@element-plus/icons-vue'
import StarRating from '@/components/common/StarRating.vue'

const props = defineProps<{
  visible: boolean
  recipe: Recipe | null
  isLiked?: boolean
}>()

const emit = defineEmits<{
  'update:visible': [boolean]
  'toggle-favorite': [Recipe]
}>()

const dialogVisible = ref(false)
const { copyText, formatRecipeText } = useCopyToClipboard()
const userScore = ref(0)

const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

watch(() => props.visible, async (v) => {
  dialogVisible.value = v
  if (v && props.recipe?.dbId && isAuthenticated.value) {
    try {
      const res = await recipeApi.getMyRating(props.recipe.dbId)
      userScore.value = res.data?.score ?? 0
    } catch { userScore.value = 0 }
  } else {
    userScore.value = 0
  }
})
watch(dialogVisible, v => { if (!v) emit('update:visible', false) })

const dietColor = computed(() => {
  const m: Record<string, string> = { '减脂': '#67C23A', '家常': '#FF6B35', '儿童餐': '#E6A23C', '素食': '#409EFF' }
  return m[props.recipe?.dietType || ''] || '#909399'
})

const nutritionItems = computed(() => {
  const n = props.recipe?.nutrition
  if (!n) return []
  const parseVal = (s: string) => parseFloat(s) || 0
  const max = Math.max(100, parseVal(n.calories) / 3)
  return [
    { label: '热量', value: n.calories, percent: Math.min(100, (parseVal(n.calories) / max) * 100), color: '#FF6B35' },
    { label: '蛋白质', value: n.protein, percent: Math.min(100, (parseVal(n.protein) / max) * 100 * 5), color: '#409EFF' },
    { label: '碳水', value: n.carbs, percent: Math.min(100, (parseVal(n.carbs) / max) * 100), color: '#E6A23C' },
    { label: '脂肪', value: n.fat, percent: Math.min(100, (parseVal(n.fat) / max) * 100 * 2), color: '#F56C6C' },
    { label: '膳食纤维', value: n.fiber, percent: Math.min(100, (parseVal(n.fiber) / max) * 100 * 5), color: '#67C23A' },
  ]
})

function copyRecipe() {
  if (props.recipe) copyText(formatRecipeText(props.recipe))
}

function toggleFav() {
  if (props.recipe) emit('toggle-favorite', props.recipe)
}

async function submitRating(score: number) {
  if (!props.recipe?.dbId) return
  try {
    const res = await recipeApi.rate(props.recipe.dbId, score)
    userScore.value = res.data?.userScore ?? score
    if (props.recipe) {
      props.recipe.avgRating = res.data?.avgRating
      props.recipe.ratingCount = res.data?.ratingCount
    }
    ElMessage.success('评分成功')
  } catch { /* handled */ }
}

async function clearRating() {
  if (!props.recipe?.dbId) return
  try {
    const res = await recipeApi.deleteRating(props.recipe.dbId)
    userScore.value = 0
    if (props.recipe && res.data) {
      props.recipe.avgRating = res.data.avgRating
      props.recipe.ratingCount = res.data.ratingCount
    }
    ElMessage.success('已取消评分')
  } catch { /* handled */ }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.detail-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: $font-size-sm;
  color: $color-text-secondary;
}

.detail-desc {
  margin-top: 12px;
  color: $color-text-regular;
  font-size: $font-size-base;
}

.detail-rating-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  padding: 12px 16px;
  background: var(--app-bg-warm, $color-bg-warm);
  border-radius: $radius-md;

  .my-rating-hint {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: $font-size-sm;
    color: var(--app-text-secondary, $color-text-secondary);
  }
}

.section-title {
  font-size: $font-size-md;
  font-weight: 600;
  margin-bottom: 12px;
}

.ingredient-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.ingredient-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--app-bg-gray, $color-bg-gray);
  border-radius: $radius-sm;
  font-size: $font-size-sm;

  .ing-name { font-weight: 600; color: $color-text-primary; }
  .ing-amount { color: $color-primary; }
  .ing-notes { color: $color-text-secondary; font-size: $font-size-xs; }
}

.steps-list { display: flex; flex-direction: column; gap: 10px; }

.step-card {
  display: flex;
  gap: 14px;
  padding: 12px 14px;
  background: var(--app-bg-warm, $color-bg-warm);
  border-radius: $radius-md;
  border-left: 3px solid $color-primary;

  .step-number {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $color-primary;
    color: #fff;
    border-radius: 50%;
    font-size: $font-size-sm;
    font-weight: 700;
  }

  .step-text { flex: 1; font-size: $font-size-base; color: $color-text-regular; line-height: 1.7; }
}

.nutrition-bars { display: flex; flex-direction: column; gap: 8px; }

.nutrition-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nutrition-label {
  width: 60px;
  font-size: $font-size-sm;
  color: $color-text-secondary;
  flex-shrink: 0;
}

.nutrition-bar-bg {
  flex: 1;
  height: 8px;
  background: var(--app-bg-gray, $color-bg-gray);
  border-radius: 4px;
  overflow: hidden;
}

.nutrition-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.nutrition-value {
  width: 80px;
  font-size: $font-size-sm;
  color: $color-text-regular;
  flex-shrink: 0;
}

.tips-text { font-size: $font-size-base; }

.mt-lg { margin-top: 16px; }
</style>
