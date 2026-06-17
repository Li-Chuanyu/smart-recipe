<template>
  <div class="star-rating" :class="[`size-${size}`, { readonly: readonly }]">
    <span
      v-for="star in 5"
      :key="star"
      class="star"
      :class="{
        filled: star <= displayValue,
        half: !readonly && star === Math.ceil(displayValue) && displayValue % 1 !== 0,
      }"
      @click="!readonly && setRating(star)"
      @mouseenter="!readonly && (hoverValue = star)"
      @mouseleave="!readonly && (hoverValue = 0)"
    >
      <el-icon :size="iconSize">
        <StarFilled v-if="star <= (hoverValue || displayValue)" />
        <Star v-else />
      </el-icon>
    </span>
    <span v-if="showLabel" class="rating-label">
      <template v-if="readonly && ratingCount !== undefined">
        {{ displayValue.toFixed(1) }}
        <span class="rating-count">({{ ratingCount }})</span>
      </template>
      <template v-else-if="!readonly && modelValue > 0">
        已评分 {{ modelValue }} 星
      </template>
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Star, StarFilled } from '@element-plus/icons-vue'

const props = withDefaults(defineProps<{
  modelValue?: number
  readonly?: boolean
  size?: 'small' | 'default' | 'large'
  ratingCount?: number
  showLabel?: boolean
}>(), {
  modelValue: 0,
  readonly: true,
  size: 'default',
  ratingCount: undefined,
  showLabel: true,
})

const emit = defineEmits<{
  'update:modelValue': [value: number]
}>()

const hoverValue = ref(0)

const displayValue = computed(() => {
  return hoverValue.value || props.modelValue || 0
})

const iconSize = computed(() => {
  return props.size === 'small' ? 14 : props.size === 'large' ? 22 : 18
})

function setRating(score: number) {
  emit('update:modelValue', score)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.star-rating {
  display: inline-flex;
  align-items: center;
  gap: 2px;

  &.size-small .star { line-height: 1; }
  &.size-large .star { line-height: 1; }
}

.star {
  color: #c0c4cc;
  cursor: default;
  transition: color 0.15s, transform 0.15s;

  &.filled {
    color: #f7ba2a;
  }

  .star-rating:not(.readonly) & {
    cursor: pointer;
    &:hover {
      transform: scale(1.15);
      color: #f7ba2a;
    }
  }
}

.rating-label {
  margin-left: 6px;
  font-size: $font-size-sm;
  color: $color-warning;
  font-weight: 600;

  .rating-count {
    color: var(--app-text-secondary, $color-text-secondary);
    font-weight: 400;
    font-size: $font-size-xs;
  }
}
</style>
