<template>
  <div class="post-detail-page">
    <div class="container" v-loading="loading">
      <el-button text @click="$router.back()" class="back-btn">
        <el-icon><ArrowLeft /></el-icon> 返回社区
      </el-button>

      <template v-if="post">
        <div class="post-card-detail">
          <div class="post-user">
            <el-avatar :size="44">{{ post.username?.charAt(0) }}</el-avatar>
            <div>
              <div class="username">{{ post.username }}</div>
              <div class="time">{{ formatDate(post.created_at) }}</div>
            </div>
          </div>
          <h1>{{ post.title }}</h1>
          <div class="post-content" v-html="post.content?.replace(/\n/g, '<br>')" />
          <div v-if="post.images?.length" class="post-images">
            <img v-for="(img, i) in post.images" :key="i" :src="img" />
          </div>
          <div class="post-actions">
            <el-button :type="post.is_liked ? 'primary' : 'default'" text @click="handleLike">
              <el-icon><StarFilled v-if="post.is_liked" /><Star v-else /></el-icon>
              {{ post.like_count }}
            </el-button>
            <span><el-icon><View /></el-icon> {{ post.view_count }} 浏览</span>
          </div>
        </div>

        <!-- Comments -->
        <div class="comments-section">
          <h3>评论 ({{ comments.length }})</h3>
          <div class="comment-input">
            <el-input v-model="commentText" type="textarea" :rows="2" placeholder="发表你的评论..." />
            <el-button type="primary" style="margin-top: 8px;" @click="submitComment">发表评论</el-button>
          </div>
          <div v-if="comments.length" class="comment-list">
            <div v-for="c in comments" :key="c.id" class="comment-item">
              <el-avatar :size="32">{{ c.username?.charAt(0) }}</el-avatar>
              <div class="comment-body">
                <div class="comment-header">
                  <span class="comment-username">{{ c.username }}</span>
                  <span class="comment-time">{{ formatDate(c.created_at) }}</span>
                </div>
                <p>{{ c.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { communityApi } from '@/api/community'
import type { CommunityPost, Comment } from '@/types/api'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Star, StarFilled, View } from '@element-plus/icons-vue'

const route = useRoute()
const post = ref<CommunityPost | null>(null)
const comments = ref<Comment[]>([])
const commentText = ref('')
const loading = ref(true)

async function fetchPost() {
  loading.value = true
  try {
    const id = Number(route.params.id)
    const [postRes, commentRes] = await Promise.all([
      communityApi.getPost(id),
      communityApi.getComments(id),
    ])
    post.value = postRes.data
    comments.value = commentRes.data || []
  } catch { post.value = null } finally { loading.value = false }
}

async function handleLike() {
  if (!post.value) return
  try {
    const { data } = await communityApi.like(post.value.id)
    post.value.is_liked = data!.liked
    post.value.like_count += data!.liked ? 1 : -1
  } catch { /* handled */ }
}

async function submitComment() {
  if (!commentText.value.trim() || !post.value) return
  try {
    const { data } = await communityApi.createComment(post.value.id, commentText.value.trim())
    if (data) comments.value.push(data)
    commentText.value = ''
    ElMessage.success('评论发布成功')
  } catch { /* handled */ }
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => fetchPost())
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.post-detail-page {
  padding: 32px 0 64px;

  .container {
    max-width: 800px;
  }
}

.back-btn { margin-bottom: 20px; }

.post-card-detail {
  background: #fff;
  border-radius: $radius-xl;
  padding: 32px;
  box-shadow: $shadow-sm;
  margin-bottom: 32px;
}

.post-user {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;

  .username { font-weight: 600; }
  .time { font-size: $font-size-sm; color: $color-text-secondary; }
}

h1 { font-size: $font-size-2xl; margin-bottom: 16px; }

.post-content {
  font-size: $font-size-base;
  line-height: 1.8;
  color: $color-text-regular;
  margin-bottom: 16px;
}

.post-images {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;

  img {
    width: 200px;
    height: 150px;
    object-fit: cover;
    border-radius: $radius-md;
  }
}

.post-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 16px;
  border-top: 1px solid $color-border-light;
  color: $color-text-secondary;
}

.comments-section {
  background: #fff;
  border-radius: $radius-xl;
  padding: 32px;
  box-shadow: $shadow-sm;

  h3 { margin-bottom: 16px; }
}

.comment-input {
  margin-bottom: 24px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid $color-border-light;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  gap: 12px;
  margin-bottom: 4px;

  .comment-username { font-weight: 600; font-size: $font-size-sm; }
  .comment-time { font-size: $font-size-xs; color: $color-text-secondary; }
}
</style>
