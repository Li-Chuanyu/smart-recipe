<template>
  <div class="admin-dashboard" v-loading="loading">
    <h2>数据仪表盘</h2>
    <div class="stats-grid">
      <el-row :gutter="16">
        <el-col :span="6" :sm="12" :xs="24" v-for="s in statCards" :key="s.label" style="margin-bottom: 16px;">
          <div class="stat-card" :style="{ borderTopColor: s.color }">
            <div class="stat-icon">{{ s.icon }}</div>
            <div class="stat-num">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import type { AdminStats } from '@/types/api'

const stats = ref<AdminStats | null>(null)
const loading = ref(false)

const statCards = computed(() => {
  if (!stats.value) return []
  return [
    { label: '用户总数', value: stats.value.total_users, icon: '👥', color: '#409EFF' },
    { label: '食谱总数', value: stats.value.total_recipes, icon: '📖', color: '#FF6B35' },
    { label: '帖子总数', value: stats.value.total_posts, icon: '💬', color: '#67C23A' },
    { label: '评论总数', value: stats.value.total_comments, icon: '💭', color: '#E6A23C' },
    { label: '待审核食谱', value: stats.value.pending_recipes, icon: '⏳', color: '#F56C6C' },
    { label: '待处理帖子', value: stats.value.flagged_posts, icon: '🚩', color: '#909399' },
  ]
})

onMounted(async () => {
  loading.value = true
  try { const { data } = await adminApi.getStats(); stats.value = data }
  catch { /* handled */ }
  finally { loading.value = false }
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.admin-dashboard { h2 { margin-bottom: 24px; } }

.stat-card {
  background: #fff;
  border-radius: $radius-lg;
  padding: 24px;
  border-top: 3px solid;
  box-shadow: $shadow-sm;
}

.stat-icon { font-size: 32px; margin-bottom: 8px; }
.stat-num { font-size: $font-size-2xl; font-weight: 700; color: $color-text-primary; }
.stat-label { font-size: $font-size-sm; color: $color-text-secondary; margin-top: 4px; }
</style>
