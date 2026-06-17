<template>
  <div class="shopping-detail-page">
    <div class="container" style="max-width: 800px;">
      <!-- Header -->
      <div class="detail-header">
        <el-button text :icon="ArrowLeft" @click="$router.push('/shopping-lists')">返回</el-button>
        <h1 v-if="list">{{ list.name }}</h1>
      </div>

      <!-- Progress -->
      <div v-if="list" class="progress-section">
        <div class="progress-stats">
          <span>采购进度</span>
          <span class="progress-text">{{ checkedCount }} / {{ list.items.length }} 项</span>
        </div>
        <el-progress
          :percentage="progressPercent"
          :color="progressBarColor"
          :stroke-width="12"
        />
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-wrap">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      </div>

      <!-- Grouped items -->
      <div v-else-if="list && groupedItems.length" class="items-section">
        <ShoppingCategoryGroup
          v-for="group in groupedItems"
          :key="group.category"
          :category="group.category"
          :items="group.items"
          @toggle="handleToggle"
          @remove="handleRemove"
        />
      </div>

      <!-- Empty -->
      <EmptyState
        v-else-if="list && !list.items.length"
        icon="🛒"
        title="清单是空的"
        description="这个购物清单还没有任何食材"
      />

      <!-- Not found -->
      <ErrorState
        v-else-if="!list && !loading"
        icon="error"
        title="找不到购物清单"
        message="该清单可能已被删除"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { shoppingListApi } from '@/api/shoppingList'
import type { ShoppingList, ShoppingItem } from '@/types/shoppingList'
import ShoppingCategoryGroup from '@/components/shopping/ShoppingCategoryGroup.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Loading } from '@element-plus/icons-vue'

const route = useRoute()
const listId = computed(() => Number(route.params.id))

const list = ref<ShoppingList | null>(null)
const loading = ref(true)

onMounted(() => loadList())
watch(() => route.params.id, () => loadList())

async function loadList() {
  loading.value = true
  try {
    const res = await shoppingListApi.getList(listId.value)
    list.value = res.data
  } catch {
    list.value = null
  } finally {
    loading.value = false
  }
}

const checkedCount = computed(() =>
  list.value?.items.filter(i => i.checked).length ?? 0
)

const progressPercent = computed(() => {
  if (!list.value?.items.length) return 0
  return Math.round((checkedCount.value / list.value.items.length) * 100)
})

const progressBarColor = computed(() => {
  if (progressPercent.value >= 100) return '#67C23A'
  if (progressPercent.value >= 50) return '#E6A23C'
  return '#FF6B35'
})

// Group items by category
const groupedItems = computed(() => {
  if (!list.value) return []
  const groups = new Map<string, ShoppingItem[]>()
  for (const item of list.value.items) {
    const cat = item.category || '其他'
    if (!groups.has(cat)) groups.set(cat, [])
    groups.get(cat)!.push(item)
  }
  return Array.from(groups.entries()).map(([category, items]) => ({ category, items }))
})

async function handleToggle(item: ShoppingItem) {
  try {
    await shoppingListApi.toggleCheck(listId.value, item.id)
    item.checked = !item.checked
  } catch { /* handled */ }
}

async function handleRemove(item: ShoppingItem) {
  try {
    await shoppingListApi.removeItem(listId.value, item.id)
    if (list.value) {
      list.value.items = list.value.items.filter(i => i.id !== item.id)
    }
    ElMessage.success('已移除')
  } catch { /* handled */ }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.shopping-detail-page {
  padding: 32px 0 64px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;

  h1 {
    font-size: $font-size-xl;
    font-weight: 700;
    color: var(--app-text-primary, $color-text-primary);
  }
}

.progress-section {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-lg;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: $shadow-sm;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: $font-size-sm;
  color: var(--app-text-secondary, $color-text-secondary);
}

.progress-text {
  font-weight: 600;
  color: var(--app-text-primary, $color-text-primary);
}

.items-section {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-xl;
  padding: 24px;
  box-shadow: $shadow-sm;
}

.loading-wrap {
  text-align: center;
  padding: 80px;
}
</style>
