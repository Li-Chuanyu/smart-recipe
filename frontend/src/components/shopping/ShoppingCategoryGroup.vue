<template>
  <div class="category-group">
    <div class="category-header">
      <span class="category-icon">{{ config?.icon || '🛒' }}</span>
      <span class="category-name">{{ category }}</span>
      <span class="category-count">{{ items.length }}项</span>
    </div>
    <div class="category-items">
      <div
        v-for="item in items"
        :key="item.id"
        class="shopping-item-row"
        :class="{ checked: item.checked }"
      >
        <el-checkbox
          :model-value="item.checked"
          @change="toggleItem(item)"
        />
        <span class="item-name">{{ item.name }}</span>
        <span class="item-amount">{{ item.amount }}</span>
        <el-button
          text
          size="small"
          type="danger"
          :icon="Delete"
          @click="removeItem(item)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ShoppingItem } from '@/types/shoppingList'
import { CATEGORY_CONFIG } from '@/types/shoppingList'
import { Delete } from '@element-plus/icons-vue'

const props = defineProps<{
  category: string
  items: ShoppingItem[]
}>()

const emit = defineEmits<{
  'toggle': [item: ShoppingItem]
  'remove': [item: ShoppingItem]
}>()

const config = CATEGORY_CONFIG[props.category]

function toggleItem(item: ShoppingItem) {
  emit('toggle', item)
}

function removeItem(item: ShoppingItem) {
  emit('remove', item)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.category-group {
  margin-bottom: 24px;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  margin-bottom: 8px;
  border-bottom: 2px solid var(--app-border-light, $color-border-light);
}

.category-icon {
  font-size: 20px;
}

.category-name {
  font-weight: 700;
  font-size: $font-size-md;
  color: var(--app-text-primary, $color-text-primary);
}

.category-count {
  font-size: $font-size-sm;
  color: var(--app-text-secondary, $color-text-secondary);
  margin-left: auto;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.shopping-item-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: $radius-md;
  transition: background $transition-fast;

  &:hover {
    background: var(--app-bg-warm, $color-bg-warm);
  }

  &.checked {
    .item-name {
      text-decoration: line-through;
      color: var(--app-text-secondary, $color-text-secondary);
    }
    .item-amount {
      text-decoration: line-through;
      color: var(--app-text-secondary, $color-text-secondary);
    }
  }
}

.item-name {
  flex: 1;
  font-size: $font-size-base;
  font-weight: 500;
  color: var(--app-text-primary, $color-text-primary);
}

.item-amount {
  font-size: $font-size-sm;
  color: $color-primary;
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}
</style>
