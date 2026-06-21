<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <el-icon :size="40" color="#FF6B35"><KnifeFork /></el-icon>
        <h2>登录 AI 食谱</h2>
        <p>欢迎回来，继续你的美食之旅</p>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" prefix-icon="Message" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" size="large" class="submit-btn" :loading="loading" @click="handleLogin">
          登录
        </el-button>
      </el-form>
      <div class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { setTokens, setUserInfo } from '@/stores/auth'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { KnifeFork, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const form = reactive({ email: '', password: '' })
const rules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
}

async function handleLogin() {
  loading.value = true
  try {
    const { data } = await authApi.login({ email: form.email, password: form.password })
    setTokens(data!.access_token, data!.refresh_token)
    // Fetch user info
    const { data: userData } = await authApi.getMe()
    setUserInfo(userData)
    ElMessage.success('登录成功')
    const redirect = route.query.redirect as string
    router.push(redirect || '/')
  } catch (err: any) {
    const msg = err?.response?.data?.message || err?.message || '登录失败'
    ElMessage.error(msg)
  }
  finally { loading.value = false }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 32px 16px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: $radius-xl;
  box-shadow: $shadow-lg;
  padding: 40px 36px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;

  h2 { font-size: $font-size-2xl; font-weight: 700; margin: 12px 0 6px; }
  p { color: $color-text-secondary; font-size: $font-size-sm; }
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-size: $font-size-md;
  font-weight: 600;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: $font-size-sm;
  color: $color-text-secondary;
}
</style>
