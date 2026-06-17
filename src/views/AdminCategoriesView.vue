<template>
  <div class="admin-categories" v-loading="loading">
    <div class="flex-between" style="margin-bottom: 16px;">
      <h2>分类管理</h2>
      <el-button type="primary" @click="openDialog()">添加分类</el-button>
    </div>
    <el-table :data="categories" stripe>
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除？" @confirm="handleDelete(row.id)">
            <template #reference><el-button size="small" type="danger">删除</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑分类' : '添加分类'" width="500px">
      <el-form label-position="top">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="分类名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" placeholder="分类描述" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { ElMessage } from 'element-plus'
import type { Category } from '@/types/api'

const categories = ref<Category[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Category | null>(null)
const form = reactive({ name: '', description: '', sort_order: 0 })

async function fetch() {
  loading.value = true
  try { const { data } = await adminApi.getCategories(); categories.value = data || [] }
  catch { } finally { loading.value = false }
}

function openDialog(cat?: Category) {
  if (cat) {
    editing.value = cat
    form.name = cat.name; form.description = cat.description; form.sort_order = cat.sort_order
  } else {
    editing.value = null
    form.name = ''; form.description = ''; form.sort_order = 0
  }
  dialogVisible.value = true
}

async function handleSave() {
  try {
    if (editing.value) {
      await adminApi.updateCategory(editing.value.id, { ...form })
      ElMessage.success('分类已更新')
    } else {
      await adminApi.createCategory({ ...form })
      ElMessage.success('分类已创建')
    }
    dialogVisible.value = false
    fetch()
  } catch { }
}

async function handleDelete(id: number) {
  try {
    await adminApi.deleteCategory(id)
    ElMessage.success('分类已删除')
    fetch()
  } catch { }
}

onMounted(() => fetch())
</script>
