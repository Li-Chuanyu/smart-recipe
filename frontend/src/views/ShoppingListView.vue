<template>
  <div class="shopping-lists-page">
    <div class="container">
      <div class="page-header">
        <h1>🛒 购物清单</h1>
        <p>管理你的食材采购清单</p>
      </div>

      <div class="toolbar">
        <el-button type="primary" @click="$router.push('/meal-plan')">
          📅 从食谱计划生成
        </el-button>
      </div>

      <div v-if="loading" class="loading-wrap">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      </div>

      <div v-else-if="!lists.length" class="empty-wrap">
        <EmptyState
          icon="🛒"
          title="还没有购物清单"
          description="在食谱计划页面一键生成，或从食谱详情创建"
          action-text="去食谱计划"
          @action="$router.push('/meal-plan')"
        />
      </div>

      <div v-else class="lists-grid">
        <div
          v-for="list in lists"
          :key="list.id"
          class="list-card card-hover"
          @click="$router.push(`/shopping-list/${list.id}`)"
        >
          <div class="list-card-header">
            <h3>{{ list.name }}</h3>
            <el-button
              text
              size="small"
              type="danger"
              :icon="Delete"
              @click.stop="deleteList(list.id)"
            />
          </div>
          <div class="list-card-progress">
            <el-progress
              :percentage="listProgress(list)"
              :color="progressColor(list)"
              :stroke-width="8"
            />
          </div>
          <div class="list-card-meta">
            <span>✅ {{ list.checkedCount || 0 }}/{{ list.itemCount || 0 }} 已购</span>
            <span class="source-tag">
              <el-tag size="small" v-if="list.sourceType === 'meal_plan'" type="success" effect="plain">来自食谱计划</el-tag>
              <el-tag size="small" v-else-if="list.sourceType === 'recipes'" type="primary" effect="plain">自选食谱</el-tag>
              <el-tag size="small" v-else type="info" effect="plain">手动创建</el-tag>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { shoppingListApi } from '@/api/shoppingList'
import type { ShoppingList } from '@/types/shoppingList'
import EmptyState from '@/components/common/EmptyState.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Loading } from '@element-plus/icons-vue'

const lists = ref<ShoppingList[]>([])
const loading = ref(true)

onMounted(() => loadLists())

async function loadLists() {
  loading.value = true
  try {
    const res = await shoppingListApi.getLists()
    lists.value = res.data || []
  } catch { lists.value = [] }
  finally { loading.value = false }
}

function listProgress(list: ShoppingList): number {
  if (!list.itemCount) return 0
  return Math.round(((list.checkedCount || 0) / list.itemCount) * 100)
}

function progressColor(list: ShoppingList): string {
  const pct = listProgress(list)
  if (pct >= 100) return '#67C23A'
  if (pct >= 50) return '#E6A23C'
  return '#FF6B35'
}

async function deleteList(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这个购物清单吗？', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await shoppingListApi.deleteList(id)
    lists.value = lists.value.filter(l => l.id !== id)
    ElMessage.success('已删除')
  } catch { /* cancelled */ }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.shopping-lists-page {
  padding: 32px 0 64px;
}

.toolbar {
  margin-bottom: 24px;
}

.loading-wrap {
  text-align: center;
  padding: 80px;
}

.lists-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;

  @media (max-width: $breakpoint-md) {
    grid-template-columns: repeat(2, 1fr);
  }
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.list-card {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-lg;
  padding: 20px;
  box-shadow: $shadow-sm;

  &-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;

    h3 {
      font-size: $font-size-md;
      font-weight: 600;
      color: var(--app-text-primary, $color-text-primary);
    }
  }

  &-progress {
    margin-bottom: 12px;
  }

  &-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: $font-size-sm;
    color: var(--app-text-secondary, $color-text-secondary);
  }
}
</style>
