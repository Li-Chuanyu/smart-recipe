<template>
  <div class="empty-state">
    <div class="empty-icon">{{ icon }}</div>
    <h3>{{ title }}</h3>
    <p v-if="description">{{ description }}</p>
    <slot name="action">
      <el-button v-if="actionText" type="primary" @click="$emit('action')">
        {{ actionText }}
      </el-button>
    </slot>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  title: string
  description?: string
  actionText?: string
}>()

defineEmits<{ action: [] }>()
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.empty-state {
  text-align: center;
  padding: 64px 24px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

h3 {
  font-size: $font-size-lg;
  color: $color-text-primary;
  margin-bottom: 8px;
}

p {
  font-size: $font-size-base;
  color: $color-text-secondary;
  margin-bottom: 24px;
}
</style>
