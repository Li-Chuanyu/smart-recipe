<template>
  <div class="recipe-filter-bar">
    <el-input
      :model-value="keyword"
      placeholder="搜索食谱名称、食材..."
      clearable
      prefix-icon="Search"
      style="width: 240px"
      @input="$emit('update:keyword', ($event as any).target?.value ?? $event)"
    />
    <el-select :model-value="dietType" placeholder="饮食类型" clearable style="width: 130px" @change="$emit('update:dietType', $event)">
      <el-option v-for="d in DIET_TYPES" :key="d.value" :label="d.label" :value="d.value" />
    </el-select>
    <el-select :model-value="difficulty" placeholder="难度" clearable style="width: 110px" @change="$emit('update:difficulty', $event)">
      <el-option v-for="d in DIFFICULTY_OPTIONS" :key="d.value" :label="d.label" :value="d.value" />
    </el-select>
    <el-select :model-value="sortBy" style="width: 130px" @change="$emit('update:sortBy', $event)">
      <el-option label="最新收藏" value="newest" />
      <el-option label="最早收藏" value="oldest" />
      <el-option label="按名称" value="title" />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { DIET_TYPES, DIFFICULTY_OPTIONS } from '@/types/recipe'

defineProps<{
  keyword: string
  dietType: string
  difficulty: string
  sortBy: string
}>()

defineEmits<{
  'update:keyword': [string]
  'update:dietType': [string]
  'update:difficulty': [string]
  'update:sortBy': [string]
}>()
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.recipe-filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 16px 0;
}
</style>
