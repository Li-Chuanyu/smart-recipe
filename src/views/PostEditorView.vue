<template>
  <div class="post-editor-page">
    <div class="container" style="max-width: 800px;">
      <div class="page-header">
        <h1>{{ isEdit ? '编辑帖子' : '✍️ 发布帖子' }}</h1>
        <p>分享你的美食心得</p>
      </div>
      <div class="editor-card">
        <el-form label-position="top">
          <el-form-item label="标题">
            <el-input v-model="form.title" placeholder="给帖子起个标题..." maxlength="100" show-word-limit size="large" />
          </el-form-item>
          <el-form-item label="内容">
            <el-input v-model="form.content" type="textarea" :rows="8" placeholder="分享你的烹饪经历、美食发现..." maxlength="5000" show-word-limit />
          </el-form-item>
          <el-form-item label="图片（可选）">
            <el-upload
              :action="'/api/v1/upload/image'"
              :headers="uploadHeaders"
              list-type="picture-card"
              :on-success="onUploadSuccess"
              :before-upload="beforeUpload"
              :limit="6"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
          </el-form-item>
          <div class="editor-actions">
            <el-button @click="$router.back()">取消</el-button>
            <el-button type="primary" :disabled="!form.title.trim()" :loading="loading" @click="handleSubmit">
              发布帖子
            </el-button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { communityApi } from '@/api/community'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const router = useRouter()
const isEdit = false
const loading = ref(false)
const form = reactive({ title: '', content: '' })
const uploadedImages = ref<string[]>([])

const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('access_token')}`,
}))

function onUploadSuccess(response: any) {
  if (response.data?.url) {
    uploadedImages.value.push(response.data.url)
  }
}

function beforeUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isImage) { ElMessage.error('只能上传图片文件'); return false }
  if (!isLt5M) { ElMessage.error('图片大小不能超过 5MB'); return false }
  return true
}

async function handleSubmit() {
  loading.value = true
  try {
    await communityApi.createPost({
      title: form.title.trim(),
      content: form.content.trim(),
      images: uploadedImages.value,
    })
    ElMessage.success('帖子发布成功')
    router.push('/community')
  } catch { /* handled */ } finally { loading.value = false }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.post-editor-page { padding: 32px 0 64px; }

.editor-card {
  background: #fff;
  border-radius: $radius-xl;
  padding: 32px;
  box-shadow: $shadow-sm;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}
</style>
