<template>
  <footer class="app-footer">
    <div class="container footer-content">
      <div class="footer-brand">
        <div class="brand-row">
          <el-icon :size="24"><KnifeFork /></el-icon>
          <span>AI 智能食谱</span>
        </div>
        <p>用 AI 为每一餐增添灵感</p>
      </div>
      <div class="footer-links">
        <div class="link-group">
          <h4>功能</h4>
          <router-link to="/generate">AI 生成食谱</router-link>
          <router-link to="/recipes">食谱浏览</router-link>
          <router-link to="/community">美食社区</router-link>
        </div>
        <div class="link-group">
          <h4>关于</h4>
          <router-link to="/settings">设置</router-link>
          <a href="#" @click.prevent>帮助中心</a>
          <a href="#" @click.prevent>隐私政策</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; {{ year }} AI 智能食谱 · Powered by AI · All Rights Reserved</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.app-footer {
  background: #1d1e2c;
  color: rgba(255, 255, 255, 0.7);
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  padding: 48px 0 32px;
  gap: 48px;

  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
    gap: 32px;
  }
}

.footer-brand {
  .brand-row {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #fff;
    font-size: $font-size-lg;
    font-weight: 600;
    margin-bottom: 8px;
  }

  p {
    color: rgba(255, 255, 255, 0.5);
    font-size: $font-size-sm;
  }
}

.footer-links {
  display: flex;
  gap: 64px;

  @media (max-width: $breakpoint-sm) {
    gap: 40px;
  }
}

.link-group {
  h4 {
    color: #fff;
    font-size: $font-size-base;
    margin-bottom: 12px;
  }

  a {
    display: block;
    color: rgba(255, 255, 255, 0.5);
    font-size: $font-size-sm;
    padding: 4px 0;
    transition: color $transition-fast;

    &:hover {
      color: $color-primary-light;
    }
  }
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 16px 0;
  text-align: center;

  p {
    font-size: $font-size-xs;
    color: rgba(255, 255, 255, 0.35);
  }
}
</style>
