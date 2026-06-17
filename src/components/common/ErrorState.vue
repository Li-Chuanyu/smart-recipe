<template>
  <div class="error-state">
    <el-result :icon="icon" :title="title" :sub-title="message">
      <template #extra>
        <el-button v-if="retryable" type="primary" @click="$emit('retry')">重试</el-button>
        <slot name="action" />
      </template>
    </el-result>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon?: 'error' | 'warning' | 'info' | 'success'
  title?: string
  message?: string
  retryable?: boolean
}>()

defineEmits<{ retry: [] }>()
</script>

<style lang="scss" scoped>
.error-state {
  padding: 48px 24px;
}
</style>
