<template>
  <div class="admin-recipes" v-loading="loading">
    <h2>食谱管理</h2>
    <el-table :data="recipes" stripe style="width: 100%">
      <el-table-column prop="title" label="食谱名称" min-width="150" />
      <el-table-column prop="dietType" label="饮食类型" width="100" />
      <el-table-column prop="difficulty" label="难度" width="80" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : row.status === 'hidden' ? 'warning' : 'info'">
            {{ row.status === 'published' ? '已发布' : row.status === 'hidden' ? '已下架' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="row.status === 'published'" type="warning" size="small" @click="updateStatus(row.id, 'hidden')">下架</el-button>
          <el-button v-if="row.status === 'hidden'" type="success" size="small" @click="updateStatus(row.id, 'published')">恢复</el-button>
          <el-popconfirm title="确定删除此食谱？" @confirm="deleteRecipe(row.id)">
            <template #reference>
              <el-button type="danger" size="small">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top: 16px; text-align: center;">
      <el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev, pager, next" @current-change="fetchRecipes" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { ElMessage } from 'element-plus'
import type { Recipe } from '@/types/recipe'

const recipes = ref<Recipe[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchRecipes() {
  loading.value = true
  try {
    const { data } = await adminApi.getPendingRecipes(page.value)
    recipes.value = data?.items || []
    total.value = data?.total || 0
  } catch { } finally { loading.value = false }
}

async function updateStatus(id: number, status: string) {
  try {
    await adminApi.updateRecipeStatus(id, status)
    ElMessage.success('状态已更新')
    fetchRecipes()
  } catch { }
}

async function deleteRecipe(id: number) {
  try {
    await adminApi.updateRecipeStatus(id, 'deleted')
    ElMessage.success('食谱已删除')
    fetchRecipes()
  } catch { }
}

onMounted(() => fetchRecipes())
</script>
