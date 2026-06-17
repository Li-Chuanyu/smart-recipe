<template>
  <router-view v-slot="{ Component }">
    <transition name="page" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useSettings } from '@/composables/useSettings'
import { useDarkMode } from '@/composables/useDarkMode'

const { loadSettings } = useSettings()
const { initTheme } = useDarkMode()

onMounted(() => {
  loadSettings()
  initTheme()
})
</script>
