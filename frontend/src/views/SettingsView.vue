<template>
  <div class="settings-page">
    <div class="container" style="max-width: 640px;">
      <div class="page-header">
        <h1>⚙️ 设置</h1>
        <p>配置 API 和应用偏好</p>
      </div>
      <div class="settings-card">
        <el-form label-position="top">
          <el-form-item label="API 基础 URL">
            <el-input v-model="settings.apiBaseUrl" placeholder="https://api.openai.com" />
          </el-form-item>
          <el-form-item label="模型选择">
            <el-select v-model="settings.selectedModel" class="full-width">
              <el-option label="GPT-4o Mini (推荐)" value="gpt-4o-mini" />
              <el-option label="GPT-4o" value="gpt-4o" />
              <el-option label="DeepSeek Chat" value="deepseek-chat" />
              <el-option label="通义千问 Plus" value="qwen-plus" />
              <el-option label="Claude 3 Haiku" value="claude-3-haiku" />
            </el-select>
          </el-form-item>
          <el-form-item label="流式响应">
            <el-switch v-model="settings.streamMode" active-text="开启" inactive-text="关闭" />
          </el-form-item>
          <div class="settings-actions">
            <el-button @click="loadSettings">重置</el-button>
            <el-button type="primary" @click="save">保存设置</el-button>
          </div>
        </el-form>

        <el-divider />

        <h3 class="section-title">🎨 主题设置</h3>
        <el-form label-position="top">
          <el-form-item label="外观主题">
            <el-radio-group v-model="theme" @change="onThemeChange">
              <el-radio-button value="light">☀️ 浅色</el-radio-button>
              <el-radio-button value="dark">🌙 深色</el-radio-button>
              <el-radio-button value="system">💻 跟随系统</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>

        <el-divider />

        <h3 class="section-title">🔑 修改密码</h3>
        <el-form label-position="top" :model="pwdForm">
          <el-form-item label="旧密码">
            <el-input v-model="pwdForm.old" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码">
            <el-input v-model="pwdForm.new" type="password" show-password />
          </el-form-item>
          <el-button type="warning" :loading="changingPwd" @click="changePassword">修改密码</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useSettings } from '@/composables/useSettings'
import { useDarkMode } from '@/composables/useDarkMode'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'

const settings = useSettings()
const { theme, setTheme } = useDarkMode()

function onThemeChange(value: string) {
  setTheme(value as 'light' | 'dark' | 'system')
}
const pwdForm = reactive({ old: '', new: '' })
const changingPwd = ref(false)

const { saveSettings, loadSettings } = settings

function save() {
  saveSettings({
    apiBaseUrl: settings.apiBaseUrl.value,
    selectedModel: settings.selectedModel.value,
    streamMode: settings.streamMode.value,
  })
  ElMessage.success('设置已保存')
}

async function changePassword() {
  if (!pwdForm.old || !pwdForm.new) { ElMessage.warning('请填写所有密码字段'); return }
  if (pwdForm.new.length < 6) { ElMessage.warning('新密码至少6位'); return }
  changingPwd.value = true
  try {
    await authApi.changePassword(pwdForm.old, pwdForm.new)
    ElMessage.success('密码修改成功')
    pwdForm.old = ''; pwdForm.new = ''
  } catch { /* handled */ } finally { changingPwd.value = false }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.settings-page { padding: 32px 0 64px; }

.settings-card {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-xl;
  padding: 32px;
  box-shadow: $shadow-sm;
}

.full-width { width: 100%; }

.settings-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.section-title {
  font-size: $font-size-md;
  font-weight: 600;
  margin-bottom: 16px;
}
</style>
