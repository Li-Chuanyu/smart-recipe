<template>
  <div class="community-page">
    <div class="container">
      <div class="page-header">
        <h1>💬 美食社区</h1>
        <p>分享你的烹饪成果，和其他食客交流心得</p>
      </div>

      <div class="community-actions">
        <el-input v-model="keyword" placeholder="搜索帖子..." clearable prefix-icon="Search" style="width: 260px" @input="fetchPosts" />
        <el-button type="primary" @click="$router.push('/community/write')">
          <el-icon><Edit /></el-icon> 发布帖子
        </el-button>
      </div>

      <div v-loading="loading">
        <div v-if="posts.length" class="post-list">
          <div v-for="post in posts" :key="post.id" class="post-card card-hover" @click="$router.push(`/community/post/${post.id}`)">
            <div class="post-avatar">
              <el-avatar :size="40">{{ post.username?.charAt(0) }}</el-avatar>
            </div>
            <div class="post-main">
              <div class="post-header">
                <h3>{{ post.title }}</h3>
                <el-tag v-if="post.is_pinned" size="small" type="danger">置顶</el-tag>
              </div>
              <p class="post-preview">{{ post.content?.substring(0, 150) }}{{ post.content?.length > 150 ? '...' : '' }}</p>
              <div class="post-meta">
                <span>{{ post.username }}</span>
                <span>{{ formatDate(post.created_at) }}</span>
                <span><el-icon><View /></el-icon> {{ post.view_count }}</span>
                <span><el-icon><ChatDotRound /></el-icon> {{ post.comment_count }}</span>
                <span><el-icon><Star /></el-icon> {{ post.like_count }}</span>
              </div>
            </div>
          </div>
        </div>

        <EmptyState v-if="!posts.length && !loading" icon="💬" title="还没有帖子" description="快来发布第一条帖子吧！" action-text="发布帖子" @action="$router.push('/community/write')" />
      </div>

      <div v-if="total > perPage" class="text-center mt-xl">
        <el-pagination v-model:current-page="page" :page-size="perPage" :total="total" layout="prev, pager, next" @current-change="fetchPosts" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { communityApi } from '@/api/community'
import type { CommunityPost } from '@/types/api'
import EmptyState from '@/components/common/EmptyState.vue'
import { Edit, View, ChatDotRound, Star } from '@element-plus/icons-vue'

const posts = ref<CommunityPost[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = 10
const total = ref(0)
const keyword = ref('')

async function fetchPosts() {
  loading.value = true
  try {
    const { data } = await communityApi.getPosts({ page: page.value, keyword: keyword.value || undefined })
    posts.value = data?.items || []
    total.value = data?.total || 0
  } catch { posts.value = [] } finally { loading.value = false }
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('zh-CN')
}

onMounted(() => fetchPosts())
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.community-page {
  padding: 32px 0 64px;
}

.community-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  display: flex;
  gap: 16px;
  padding: 20px 24px;
  background: #fff;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
}

.post-main {
  flex: 1;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;

  h3 {
    font-size: $font-size-md;
    font-weight: 600;
  }
}

.post-preview {
  font-size: $font-size-base;
  color: $color-text-secondary;
  margin-bottom: 12px;
  line-height: 1.6;
}

.post-meta {
  display: flex;
  gap: 16px;
  font-size: $font-size-sm;
  color: $color-text-secondary;
  flex-wrap: wrap;

  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}
</style>
