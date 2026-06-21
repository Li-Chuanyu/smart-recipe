<template>
  <div class="container" style="padding:64px;text-align:center">
    <h1>测试页面</h1>
    <p>如果你能看到这个，路由正常工作</p>
    <p>Token: {{ hasToken ? '✅ 已登录' : '❌ 未登录' }}</p>
    <el-button type="primary" @click="goMealPlan">去食谱计划</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const hasToken = ref(!!localStorage.getItem('access_token'))
function goMealPlan() { router.push('/meal-plan') }
</script>
