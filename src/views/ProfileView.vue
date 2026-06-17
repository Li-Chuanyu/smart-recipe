<template>
  <div class="profile-page">
    <div class="container" style="max-width: 640px;">
      <div class="page-header">
        <h1>👤 个人中心</h1>
      </div>

      <!-- Loading -->
      <div v-if="!user && loading" class="profile-card text-center" style="padding: 80px;">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      </div>

      <!-- Not logged in -->
      <div v-else-if="!user && !loading" class="profile-card text-center" style="padding: 60px;">
        <p style="margin-bottom: 16px; color: #909399;">请先登录</p>
        <el-button type="primary" @click="$router.push('/login')">去登录</el-button>
      </div>

      <!-- Profile content -->
      <div v-else-if="user" class="profile-card">
        <!-- Avatar section -->
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerUpload">
            <el-avatar :size="88" :src="user.avatar_url || undefined">
              {{ user.username?.charAt(0) }}
            </el-avatar>
            <div class="avatar-overlay">
              <el-icon :size="24"><Camera /></el-icon>
            </div>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            style="display: none"
            @change="handleAvatarChange"
          />
        </div>

        <!-- Info display / edit mode -->
        <div v-if="!editing" class="info-display">
          <h2>{{ user.username }}</h2>
          <p class="user-email">{{ user.email }}</p>
          <el-tag :type="user.role === 'admin' ? 'danger' : 'info'" size="small">
            {{ user.role === 'admin' ? '管理员' : '普通用户' }}
          </el-tag>
          <p class="join-date">注册于 {{ formatDate(user.created_at) }}</p>
          <div class="info-actions">
            <el-button type="primary" @click="startEdit">编辑资料</el-button>
          </div>
        </div>

        <!-- Edit mode -->
        <div v-else class="edit-form">
          <el-form label-position="top">
            <el-form-item label="头像">
              <div class="avatar-wrapper edit-avatar" @click="triggerUpload">
                <el-avatar :size="72" :src="user.avatar_url || undefined">
                  {{ user.username?.charAt(0) }}
                </el-avatar>
                <div class="avatar-overlay">
                  <el-icon :size="20"><Camera /></el-icon>
                </div>
              </div>
              <p class="upload-hint" v-if="uploading">正在上传...</p>
            </el-form-item>

            <el-form-item label="用户名">
              <el-input v-model="editForm.username" placeholder="用户名" maxlength="20" show-word-limit />
            </el-form-item>
          </el-form>

          <div class="edit-actions">
            <el-button @click="cancelEdit">取消</el-button>
            <el-button type="primary" :loading="saving" @click="saveProfile">保存</el-button>
          </div>
        </div>

        <el-divider />

        <!-- Links -->
        <div class="profile-links">
          <el-button text @click="$router.push('/favorites')">
            <el-icon><Star /></el-icon> 我的收藏
          </el-button>
          <el-button text @click="$router.push('/settings')">
            <el-icon><Setting /></el-icon> 修改密码
          </el-button>
          <el-button v-if="user?.role === 'admin'" text type="danger" @click="$router.push('/admin')">
            <el-icon><Monitor /></el-icon> 后台管理
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { authApi } from '@/api/auth'
import { uploadImage } from '@/api/upload'
import { ElMessage } from 'element-plus'
import type { UserInfo } from '@/types/api'
import { Camera, Loading, Star, Setting, Monitor } from '@element-plus/icons-vue'

const user = ref<UserInfo | null>(null)
const loading = ref(true)
const editing = ref(false)
const saving = ref(false)
const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const editForm = reactive({
  username: '',
})

function triggerUpload() {
  fileInput.value?.click()
}

async function handleAvatarChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  // Validate
  if (!file.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件')
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }

  uploading.value = true
  try {
    const { data } = await uploadImage(file)
    const avatarUrl = data!.url
    await authApi.updateMe({ avatar_url: avatarUrl } as any)
    if (user.value) user.value.avatar_url = avatarUrl
    localStorage.setItem('user_info', JSON.stringify(user.value))
    ElMessage.success('头像已更新')
  } catch { /* handled */ }
  finally {
    uploading.value = false
    target.value = ''
  }
}

function startEdit() {
  editForm.username = user.value?.username || ''
  editing.value = true
}

function cancelEdit() {
  editing.value = false
}

async function saveProfile() {
  if (!editForm.username.trim()) {
    ElMessage.warning('用户名不能为空')
    return
  }
  saving.value = true
  try {
    await authApi.updateMe({ username: editForm.username.trim() } as any)
    if (user.value) user.value.username = editForm.username.trim()
    localStorage.setItem('user_info', JSON.stringify(user.value))
    ElMessage.success('资料已保存')
    editing.value = false
  } catch { /* handled */ }
  finally { saving.value = false }
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await authApi.getMe()
    user.value = data
    localStorage.setItem('user_info', JSON.stringify(data))
  } catch { user.value = null }
  finally { loading.value = false }
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.profile-page { padding: 32px 0 64px; }

.profile-card {
  background: #fff;
  border-radius: $radius-xl;
  padding: 40px 32px;
  box-shadow: $shadow-sm;
}

// Avatar
.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
  border-radius: 50%;

  &:hover .avatar-overlay {
    opacity: 1;
  }
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity $transition-fast;
}

// Info display
.info-display {
  text-align: center;

  h2 {
    font-size: $font-size-xl;
    font-weight: 700;
    margin-bottom: 4px;
  }
}

.user-email {
  color: $color-text-secondary;
  font-size: $font-size-sm;
  margin: 4px 0 10px;
}

.join-date {
  color: $color-text-placeholder;
  font-size: $font-size-xs;
  margin: 8px 0 16px;
}

.info-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

// Edit form
.edit-form {
  max-width: 400px;
  margin: 0 auto;
}

.edit-avatar {
  display: inline-flex;
}

.upload-hint {
  color: $color-primary;
  font-size: $font-size-sm;
  margin-top: 4px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// Links
.profile-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style>
