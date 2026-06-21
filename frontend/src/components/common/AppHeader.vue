<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="container header-inner">
      <router-link to="/" class="brand">
        <el-icon :size="28"><KnifeFork /></el-icon>
        <span class="brand-text">AI 食谱</span>
      </router-link>

      <!-- Desktop nav -->
      <nav class="nav-desktop">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/generate" class="nav-link nav-cta">AI 生成食谱</router-link>
        <router-link to="/recipes" class="nav-link">食谱浏览</router-link>
        <router-link to="/community" class="nav-link">美食社区</router-link>
        <router-link to="/meal-plan" class="nav-link">食谱计划</router-link>
        <router-link to="/shopping-lists" class="nav-link">购物清单</router-link>
      </nav>

      <div class="header-actions">
        <!-- Theme toggle -->
        <el-button text class="theme-toggle" @click="toggleTheme">
          <el-icon :size="20">
            <Sunny v-if="isDark" />
            <Moon v-else />
          </el-icon>
        </el-button>

        <template v-if="isAuthenticated">
          <el-dropdown trigger="click">
            <span class="user-avatar">
              <el-avatar :size="32" :src="userInfo?.avatar_url">
                {{ userInfo?.username?.charAt(0) }}
              </el-avatar>
              <span class="username">{{ userInfo?.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')">
                  <el-icon><User /></el-icon> 个人中心
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/favorites')">
                  <el-icon><Star /></el-icon> 我的收藏
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/meal-plan')">
                  <el-icon><Calendar /></el-icon> 食谱计划
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/shopping-lists')">
                  <el-icon><ShoppingCart /></el-icon> 购物清单
                </el-dropdown-item>
                <el-dropdown-item v-if="userInfo?.role === 'admin'" @click="$router.push('/admin')">
                  <el-icon><Setting /></el-icon> 后台管理
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button text @click="$router.push('/login')">登录</el-button>
          <el-button type="primary" size="small" @click="$router.push('/register')">注册</el-button>
        </template>

        <!-- Mobile hamburger -->
        <el-button class="mobile-toggle" :icon="Menu" text @click="drawerVisible = true" />
      </div>
    </div>

    <!-- Mobile drawer -->
    <el-drawer v-model="drawerVisible" direction="rtl" size="260px" title="AI 智能食谱">
      <nav class="nav-mobile">
        <router-link to="/" class="mobile-link" @click="drawerVisible = false">首页</router-link>
        <router-link to="/generate" class="mobile-link highlight" @click="drawerVisible = false">AI 生成食谱</router-link>
        <router-link to="/recipes" class="mobile-link" @click="drawerVisible = false">食谱浏览</router-link>
        <router-link to="/community" class="mobile-link" @click="drawerVisible = false">美食社区</router-link>
        <el-divider />
        <router-link v-if="!isAuthenticated" to="/login" class="mobile-link" @click="drawerVisible = false">登录</router-link>
        <router-link v-if="!isAuthenticated" to="/register" class="mobile-link" @click="drawerVisible = false">注册</router-link>
        <router-link v-if="isAuthenticated" to="/favorites" class="mobile-link" @click="drawerVisible = false">我的收藏</router-link>
        <router-link to="/meal-plan" class="mobile-link" @click="drawerVisible = false">食谱计划</router-link>
        <router-link to="/shopping-lists" class="mobile-link" @click="drawerVisible = false">购物清单</router-link>
        <router-link v-if="isAuthenticated" to="/profile" class="mobile-link" @click="drawerVisible = false">个人中心</router-link>
        <a v-if="isAuthenticated" class="mobile-link" @click="handleLogout">退出登录</a>
      </nav>
    </el-drawer>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, userInfo, logout } from '@/stores/auth'
import { Menu, Sunny, Moon, Calendar, ShoppingCart } from '@element-plus/icons-vue'
import { useDarkMode } from '@/composables/useDarkMode'

const router = useRouter()
const isScrolled = ref(false)
const drawerVisible = ref(false)
const { isDark, toggleTheme, initTheme } = useDarkMode()

function handleLogout() {
  logout()
  drawerVisible.value = false
  router.push('/')
}

function onScroll() {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: $header-height;
  z-index: 1000;
  background: var(--app-header-bg, rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(12px);
  border-bottom: 1px solid transparent;
  transition: all $transition-normal;

  &.scrolled {
    border-bottom-color: $color-border-light;
    box-shadow: $shadow-sm;
  }
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  color: $color-primary;
  font-weight: 700;

  .brand-text {
    font-size: $font-size-lg;
    @media (max-width: $breakpoint-sm) {
      display: none;
    }
  }
}

.nav-desktop {
  display: flex;
  align-items: center;
  gap: 8px;

  @media (max-width: $breakpoint-md) {
    display: none;
  }
}

.nav-link {
  padding: 6px 16px;
  border-radius: $radius-md;
  color: $color-text-regular;
  font-size: $font-size-base;
  transition: all $transition-fast;

  &:hover, &.router-link-active {
    color: $color-primary;
    background: rgba($color-primary, 0.06);
  }

  &.nav-cta {
    background: $color-primary;
    color: #fff;
    font-weight: 600;

    &:hover {
      background: $color-primary-dark;
      color: #fff;
    }
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle {
  color: var(--app-text-secondary, $color-text-secondary);
  &:hover {
    color: var(--app-text-primary, $color-text-primary);
  }
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: $color-text-primary;

  .username {
    @media (max-width: $breakpoint-sm) {
      display: none;
    }
  }
}

.mobile-toggle {
  display: none;
  @media (max-width: $breakpoint-md) {
    display: inline-flex;
  }
}

.nav-mobile {
  display: flex;
  flex-direction: column;
}

.mobile-link {
  display: block;
  padding: 12px 16px;
  color: $color-text-primary;
  font-size: $font-size-md;
  border-radius: $radius-md;
  transition: background $transition-fast;

  &:hover, &.router-link-active {
    color: $color-primary;
    background: rgba($color-primary, 0.06);
  }

  &.highlight {
    background: $color-primary;
    color: #fff;
    text-align: center;
    font-weight: 600;
    margin: 8px 0;

    &:hover {
      background: $color-primary-dark;
      color: #fff;
    }
  }
}
</style>
