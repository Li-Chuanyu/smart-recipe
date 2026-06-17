<template>
  <div class="admin-users" v-loading="loading">
    <h2>用户管理</h2>
    <el-table :data="users" stripe>
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : 'info'">{{ row.role === 'admin' ? '管理员' : '用户' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'warning'">{{ row.is_active ? '正常' : '已禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="120">
        <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button v-if="row.is_active" size="small" type="warning" @click="toggleUser(row.id, false)">禁用</el-button>
          <el-button v-else size="small" type="success" @click="toggleUser(row.id, true)">启用</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="text-center mt-lg">
      <el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev, pager, next" @current-change="fetchUsers" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { ElMessage } from 'element-plus'
import type { UserInfo } from '@/types/api'

const users = ref<UserInfo[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await adminApi.getUsers(page.value)
    users.value = data?.items || []
    total.value = data?.total || 0
  } catch { } finally { loading.value = false }
}

async function toggleUser(id: number, active: boolean) {
  try {
    await adminApi.updateUserStatus(id, active)
    ElMessage.success(`用户已${active ? '启用' : '禁用'}`)
    fetchUsers()
  } catch { }
}

function formatDate(d: string) { return new Date(d).toLocaleDateString('zh-CN') }

onMounted(() => fetchUsers())
</script>
