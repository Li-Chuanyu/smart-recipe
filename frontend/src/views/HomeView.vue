<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero">
      <div class="container hero-content">
        <div class="hero-text">
          <h1>用 AI 为每一餐<br /><span class="highlight">增添灵感</span></h1>
          <p>输入你的食材、口味偏好和饮食需求，AI 大厨即刻为你生成专属食谱。<br />再也不用为"今天吃什么"发愁。</p>
          <div class="hero-actions">
            <el-button type="primary" size="large" round @click="$router.push('/generate')">
              <el-icon><MagicStick /></el-icon> 立即生成食谱
            </el-button>
            <el-button size="large" round @click="$router.push('/recipes')">
              浏览食谱库
            </el-button>
          </div>
        </div>

        <!-- 右侧视觉区：轮播图 + 缩小卡片 -->
        <div class="hero-visual">
          <!-- 轮播图，间隔 2 秒 -->
          <el-carousel 
            height="180px" 
            indicator-position="outside" 
            class="hero-carousel"
            :interval="2000"
            :autoplay="true"
            :loop="true"
          >
            <el-carousel-item v-for="(img, idx) in carouselImages" :key="idx">
              <img :src="img.url" :alt="img.alt" class="carousel-image" />
            </el-carousel-item>
          </el-carousel>

          <!-- 缩小后的悬浮卡片 -->
          <div class="floating-cards">
            <div
              v-for="(card, idx) in floatingCards"
              :key="idx"
              class="float-card"
              :style="{ animationDelay: idx * 0.2 + 's' }"
            >
              {{ card.emoji }} {{ card.label }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works（三步搞定一顿饭） -->
    <section class="page-section how-it-works">
      <div class="container">
        <div class="page-header">
          <h1>三步搞定一顿饭</h1>
          <p>比点外卖还简单</p>
        </div>
        <div class="steps-row">
          <div v-for="(step, i) in steps" :key="i" class="step-card">
            <div class="step-card-icon">{{ step.icon }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features（为什么选择 AI 食谱？） -->
    <section class="page-section features">
      <div class="container">
        <div class="page-header">
          <h1>为什么选择 AI 食谱？</h1>
          <p>智能、便捷、个性化的烹饪体验</p>
        </div>
        <div class="features-grid">
          <div v-for="(f, i) in features" :key="i" class="feature-card card-hover">
            <div class="feature-icon">{{ f.icon }}</div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="page-section cta-section">
      <div class="container text-center">
        <h1>准备好探索美味了吗？</h1>
        <p>免费开始，无需下载任何 App</p>
        <el-button type="primary" size="large" round @click="$router.push('/generate')" style="margin-top:24px">
          <el-icon><MagicStick /></el-icon> 免费生成你的第一份食谱
        </el-button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { MagicStick } from '@element-plus/icons-vue'

const steps = [
  { icon: '📝', title: '填写需求', desc: '输入现有食材、口味偏好和饮食类型，只需 10 秒' },
  { icon: '🤖', title: 'AI 创作', desc: '大模型理解你的需求，生成 1-3 份标准化食谱' },
  { icon: '🍳', title: '开始烹饪', desc: '按照详细的步骤和食材清单，轻松做出美味' },
]

const features = [
  { icon: '🧠', title: '智能匹配', desc: '根据食材种类、口味偏好智能搭配，不浪费任何食材' },
  { icon: '⚡', title: '秒级生成', desc: '大模型 API 极速响应，几秒内完成食谱创作' },
  { icon: '📋', title: '标准化格式', desc: '每份食谱包含食材清单、步骤、营养数据、烹饪贴士' },
  { icon: '⭐', title: '收藏管理', desc: '登录后可收藏喜欢的食谱，随时查看和筛选' },
  { icon: '🔍', title: '多维度搜索', desc: '按关键词、饮食类型、烹饪时长快速筛选食谱' },
  { icon: '🌐', title: '美食社区', desc: '分享你的烹饪成果，和其他食客交流心得' },
]

const floatingCards = [
  { emoji: '🥗', label: '减脂餐' },
  { emoji: '🍳', label: '家常菜' },
  { emoji: '🍱', label: '儿童餐' },
  { emoji: '🥬', label: '素食' },
  { emoji: '🍜', label: '面食' },
  { emoji: '🍰', label: '甜点' },
  { emoji: '🍣', label: '日料' },
  { emoji: '🍗', label: '油炸食品' },
]

// 轮播图图片
// 图片放在 public/img/ 目录下，访问路径为 /img/xxx.jpg
const carouselImages = [
  { url: '/img/轮播图1.jpg', alt: '美食示例1' },
  { url: '/img/轮播图2.jpg', alt: '美食示例2' },
  { url: '/img/轮播图3.jpg', alt: '美食示例3' },
]
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.hero {
  padding: 80px 0 64px;
  background: linear-gradient(135deg, $color-bg-warm 0%, #FFF3E6 50%, #FFE8D6 100%);
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 64px;

  @media (max-width: $breakpoint-md) {
    flex-direction: column;
    text-align: center;
    gap: 40px;
  }
}

.hero-text {
  flex: 1;

  h1 {
    font-size: $font-size-hero;
    font-weight: 800;
    line-height: 1.3;
    color: $color-text-primary;
    margin-bottom: 16px;

    @media (max-width: $breakpoint-sm) {
      font-size: $font-size-3xl;
    }
  }

  .highlight {
    background: linear-gradient(135deg, $color-primary, $color-secondary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  p {
    font-size: $font-size-md;
    color: $color-text-secondary;
    line-height: 1.8;
    margin-bottom: 32px;
  }
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 40px;

  @media (max-width: $breakpoint-md) {
    justify-content: center;
  }
}

// 右侧视觉区域
.hero-visual {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;

  @media (max-width: $breakpoint-md) {
    display: none;
  }
}

//轮播图样式
.hero-carousel {
  width: 100%;
  max-width: 450px;
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: $shadow-md;

  :deep(.el-carousel__container) {
    height: 180px;
  }
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

//悬浮卡片
.floating-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 12px 16px;
  max-width: 450px;
  padding: 8px 12px;
}

.float-card {
  padding: 6px 14px;
  background: #fff;
  border-radius: $radius-md;
  box-shadow: $shadow-sm;
  font-weight: 600;
  font-size: $font-size-sm;
  white-space: nowrap;
  animation: float 3.5s ease-in-out infinite;
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.05);
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

//步骤区块
.how-it-works {
  position: relative;
  background-image: url('/img/背景1.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 80px 0;          // 统一内边距
  margin-bottom: 40px;      // 与下一区块拉开距离
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08); // 底部阴影

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.2); // 统一遮罩透明度
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
  }

  // 标题颜色
  .page-header h1,
  .page-header p {
    color: #333;
  }

  .step-card {
    background: rgba(255, 255, 255, 0.9);
  }
}

//功能区块
.features {
  position: relative;
  background-image: url('/img/背景2.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 80px 0;
  margin-top: -10px;        // 轻微重叠，消除双倍间距，营造连贯感
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.06); // 顶部阴影

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-color: rgba(255, 255, 255, 0.2); // 与上方遮罩一致
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
  }

  .page-header h1,
  .page-header p {
    color: #333;
  }

  .feature-card {
    background: rgba(255, 248, 240, 0.85);
  }
}

.steps-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;

  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.step-card {
  text-align: center;
  padding: 32px 24px;
  background: #fff;
  border-radius: $radius-xl;
  box-shadow: $shadow-sm;
  transition: all $transition-normal;

  &:hover {
    box-shadow: $shadow-lg;
    transform: translateY(-4px);
  }

  &-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  h3 {
    font-size: $font-size-lg;
    font-weight: 600;
    margin-bottom: 8px;
  }

  p {
    color: $color-text-secondary;
    font-size: $font-size-sm;
  }
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;

  @media (max-width: $breakpoint-md) {
    grid-template-columns: repeat(2, 1fr);
  }
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  padding: 24px;
  background: $color-bg-warm;
  border-radius: $radius-lg;
  transition: all $transition-normal;

  .feature-icon {
    font-size: 36px;
    margin-bottom: 12px;
  }

  h3 {
    font-size: $font-size-md;
    font-weight: 600;
    margin-bottom: 6px;
  }

  p {
    font-size: $font-size-sm;
    color: $color-text-secondary;
    line-height: 1.6;
  }
}

.cta-section {
  background: linear-gradient(135deg, $color-primary, $color-secondary);
  color: #fff;

  h1 { color: #fff; }
  p { color: rgba(255, 255, 255, 0.85); }
}
</style>
