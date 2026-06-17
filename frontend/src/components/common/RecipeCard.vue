<template>
  <div class="recipe-card card-hover" @click="$emit('click', recipe)">
    <!-- Image placeholder -->
    <div class="card-image-wrapper">
      <img v-if="recipe.imageUrl" :src="recipe.imageUrl" :alt="recipe.title" class="card-image" />
      <div v-else class="gradient-placeholder" :class="dietClass">
        <span>{{ dietEmoji }}</span>
      </div>
      <!-- Favorite button -->
      <div class="card-fav" @click.stop="$emit('toggle-favorite', recipe)">
        <el-icon :size="20" :class="{ 'is-favorite': isLiked }">
          <StarFilled v-if="isLiked" />
          <Star v-else />
        </el-icon>
      </div>
    </div>

    <!-- Card body -->
    <div class="card-body">
      <!-- Tags -->
      <div class="card-tags">
        <el-tag size="small" :color="dietColor" effect="dark">
          {{ recipe.dietType }}
        </el-tag>
        <el-tag size="small" type="info" effect="plain">
          {{ recipe.difficulty }}
        </el-tag>
      </div>

      <!-- Title -->
      <h3 class="card-title">{{ recipe.title }}</h3>
      <p v-if="recipe.description" class="card-desc">{{ recipe.description }}</p>

      <!-- Meta -->
      <div class="card-meta">
        <span><el-icon><Clock /></el-icon> {{ recipe.cookingTime }}</span>
        <span><el-icon><User /></el-icon> {{ recipe.servings }}人份</span>
        <StarRating
          v-if="recipe.avgRating"
          :model-value="recipe.avgRating"
          :rating-count="recipe.ratingCount"
          readonly
          size="small"
          :show-label="false"
        />
      </div>

      <!-- Extra tags -->
      <div v-if="recipe.tags?.length" class="card-tags-bottom">
        <el-tag v-for="tag in recipe.tags.slice(0, 3)" :key="tag" size="small" type="warning" effect="light">
          {{ tag }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Recipe } from '@/types/recipe'
import { Clock, User, Star, StarFilled } from '@element-plus/icons-vue'
import StarRating from '@/components/common/StarRating.vue'

const props = defineProps<{
  recipe: Recipe
  isLiked?: boolean
}>()

defineEmits<{
  click: [recipe: Recipe]
  'toggle-favorite': [recipe: Recipe]
}>()

const dietClass = computed(() => {
  const map: Record<string, string> = {
    '减脂': 'diet-jianzhi', '家常': 'diet-home', '儿童餐': 'diet-kids',
    '素食': 'diet-veggie', '不限': 'diet-default',
  }
  return map[props.recipe.dietType] || 'diet-default'
})

const dietEmoji = computed(() => {
  const map: Record<string, string> = {
    '减脂': '🥗', '家常': '🍳', '儿童餐': '🍱', '素食': '🥬', '不限': '🍽️',
  }
  return map[props.recipe.dietType] || '🍽️'
})

const dietColor = computed(() => {
  const map: Record<string, string> = { '减脂': '#67C23A', '家常': '#FF6B35', '儿童餐': '#E6A23C', '素食': '#409EFF', '不限': '#909399' }
  return map[props.recipe.dietType] || '#909399'
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.recipe-card {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: $shadow-md;
}

.card-image-wrapper {
  position: relative;
  overflow: hidden;

  .card-image {
    width: 100%;
    aspect-ratio: 16 / 10;
    object-fit: cover;
  }
}

.card-fav {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  cursor: pointer;
  transition: all $transition-fast;
  color: $color-text-secondary;

  &:hover { transform: scale(1.1); }

  .is-favorite {
    color: $color-warning;
  }
}

.card-body {
  padding: 16px;
}

.card-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
}

.card-title {
  font-size: $font-size-md;
  font-weight: 600;
  color: $color-text-primary;
  margin-bottom: 6px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-desc {
  font-size: $font-size-sm;
  color: $color-text-secondary;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 16px;
  font-size: $font-size-sm;
  color: $color-text-secondary;

  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.card-tags-bottom {
  display: flex;
  gap: 4px;
  margin-top: 10px;
  flex-wrap: wrap;
}
</style>
