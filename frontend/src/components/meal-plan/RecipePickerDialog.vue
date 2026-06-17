<template>
  <el-dialog
    v-model="dialogVisible"
    title="选择食谱"
    width="600px"
    destroy-on-close
  >
    <div class="picker-search">
      <el-input
        v-model="keyword"
        placeholder="搜索食谱..."
        clearable
        prefix-icon="Search"
        @input="search"
      />
    </div>

    <div v-if="loading" class="picker-loading">
      <el-icon class="is-loading"><Loading /></el-icon> 搜索中...
    </div>

    <div v-else-if="!recipes.length" class="picker-empty">
      <p>没有找到食谱</p>
      <p class="hint">请先到 <router-link to="/generate">AI 生成</router-link> 或浏览食谱库</p>
    </div>

    <div v-else class="picker-grid">
      <div
        v-for="recipe in recipes"
        :key="recipe.dbId || recipe.id"
        class="picker-item"
        @click="selectRecipe(recipe)"
      >
        <div class="picker-item-title">{{ recipe.title }}</div>
        <div class="picker-item-meta">
          <span>{{ recipe.cookingTime }}</span>
          <span>{{ recipe.difficulty }}</span>
          <span class="rating" v-if="recipe.avgRating">⭐ {{ recipe.avgRating }}</span>
        </div>
      </div>
    </div>

    <div v-if="total > perPage" class="picker-pagination">
      <el-pagination
        v-model:current-page="page"
        :page-size="perPage"
        :total="total"
        layout="prev, pager, next"
        small
        @current-change="search"
      />
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { recipeApi } from '@/api/recipe'
import type { Recipe } from '@/types/recipe'
import { Loading } from '@element-plus/icons-vue'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits<{
  'update:visible': [boolean]
  'select': [Recipe]
}>()

const dialogVisible = ref(false)
const keyword = ref('')
const recipes = ref<Recipe[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = 8
const total = ref(0)

watch(() => props.visible, (v) => {
  dialogVisible.value = v
  if (v) {
    keyword.value = ''
    page.value = 1
    search()
  }
})
watch(dialogVisible, (v) => { if (!v) emit('update:visible', false) })

async function search() {
  loading.value = true
  try {
    const res = await recipeApi.getList({
      keyword: keyword.value || undefined,
      page: page.value,
      perPage,
    })
    recipes.value = res.data?.items || []
    total.value = res.data?.total || 0
  } catch { recipes.value = [] }
  finally { loading.value = false }
}

function selectRecipe(recipe: Recipe) {
  emit('select', recipe)
  dialogVisible.value = false
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.picker-search {
  margin-bottom: 16px;
}

.picker-loading, .picker-empty {
  text-align: center;
  padding: 40px;
  color: $color-text-secondary;
}

.hint {
  margin-top: 8px;
  font-size: $font-size-sm;
}

.picker-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 400px;
  overflow-y: auto;
}

.picker-item {
  padding: 12px 16px;
  border: 1px solid var(--app-border-light, $color-border-light);
  border-radius: $radius-md;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    border-color: $color-primary;
    background: rgba($color-primary, 0.04);
  }

  &-title {
    font-weight: 600;
    font-size: $font-size-base;
    color: var(--app-text-primary, $color-text-primary);
  }

  &-meta {
    display: flex;
    gap: 12px;
    margin-top: 4px;
    font-size: $font-size-sm;
    color: var(--app-text-secondary, $color-text-secondary);

    .rating { color: $color-warning; }
  }
}

.picker-pagination {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}
</style>
