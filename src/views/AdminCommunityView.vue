<template>
  <div class="admin-community" v-loading="loading">
    <h2>社区内容管理</h2>
    <el-table :data="posts" stripe>
      <el-table-column prop="title" label="标题" min-width="150" />
      <el-table-column prop="username" label="作者" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : row.status === 'hidden' ? 'warning' : 'info'">
            {{ row.status === 'published' ? '已发布' : row.status === 'hidden' ? '已隐藏' : '待审核' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="comment_count" label="评论" width="80" />
      <el-table-column prop="created_at" label="发布时间" width="120">
        <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="row.status === 'published'" size="small" type="warning" @click="hidePost(row.id)">隐藏</el-button>
          <el-button v-if="row.status === 'hidden'" size="small" type="success" @click="showPost(row.id)">恢复</el-button>
          <el-popconfirm title="确定删除？" @confirm="deletePost(row.id)">
            <template #reference><el-button size="small" type="danger">删除</el-button></template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div class="text-center mt-lg">
      <el-pagination v-model:current-page="page" :page-size="10" :total="total" layout="prev, pager, next" @current-change="fetchPosts" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { communityApi } from '@/api/community'
import { ElMessage } from 'element-plus'
import type { CommunityPost } from '@/types/api'

const posts = ref<Omit<CommunityPost, 'status'>[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)

async function fetchPosts() {
  loading.value = true
  try {
    const { data } = await communityApi.getPosts({ page: page.value })
    posts.value = data?.items || []
    total.value = data?.total || 0
  } catch { } finally { loading.value = false }
}

async function hidePost(id: number) {
  try { await communityApi.updatePost(id, { status: 'hidden' } as any); ElMessage.success('已隐藏'); fetchPosts() } catch { }
}

async function showPost(id: number) {
  try { await communityApi.updatePost(id, { status: 'published' } as any); ElMessage.success('已恢复'); fetchPosts() } catch { }
}

async function deletePost(id: number) {
  try { await communityApi.deletePost(id); ElMessage.success('已删除'); fetchPosts() } catch { }
}

function formatDate(d: string) { return new Date(d).toLocaleDateString('zh-CN') }

onMounted(() => fetchPosts())
</script>
