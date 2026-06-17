<template>
  <div class="admin-layout">
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '240px'" class="admin-sidebar">
        <div class="admin-logo" @click="$router.push('/')">
          <el-icon :size="24"><CookingPot /></el-icon>
          <span v-show="!isCollapse" class="logo-text">食谱管理后台</span>
        </div>
        <el-menu
          :default-active="route.path"
          :collapse="isCollapse"
          :collapse-transition="false"
          router
          background-color="#1d1e2c"
          text-color="#a6a7b3"
          active-text-color="#FF6B35"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/admin/recipes">
            <el-icon><Document /></el-icon>
            <span>食谱管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/categories">
            <el-icon><Collection /></el-icon>
            <span>分类管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/community">
            <el-icon><ChatLineSquare /></el-icon>
            <span>社区管理</span>
          </el-menu-item>
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>返回前台</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="admin-header">
          <div class="header-left">
            <el-button :icon="isCollapse ? Expand : Fold" text @click="isCollapse = !isCollapse" />
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">后台管理</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <span class="admin-tag">管理员</span>
            <el-button text @click="handleLogout">退出</el-button>
          </div>
        </el-header>
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Expand, Fold } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)

const currentTitle = computed(() => {
  const map: Record<string, string> = {
    '/admin/dashboard': '数据仪表盘',
    '/admin/recipes': '食谱管理',
    '/admin/categories': '分类管理',
    '/admin/users': '用户管理',
    '/admin/community': '社区管理',
  }
  return map[route.path] || '管理后台'
})

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_info')
  router.push('/login')
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.admin-layout {
  min-height: 100vh;
  background: #f0f2f5;
}

.admin-sidebar {
  background: #1d1e2c;
  min-height: 100vh;
  transition: width 0.3s;
  overflow: hidden;
}

.admin-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px;
  color: #fff;
  cursor: pointer;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);

  .logo-text {
    font-size: 16px;
    font-weight: 600;
    white-space: nowrap;
  }
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid $color-border-light;
  padding: 0 20px;
  height: 56px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .admin-tag {
    background: $color-primary;
    color: #fff;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
  }
}

.admin-main {
  padding: 24px;
  min-height: calc(100vh - 56px);
}
</style>
