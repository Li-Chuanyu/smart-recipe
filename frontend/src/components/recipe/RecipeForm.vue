<template>
  <div class="recipe-form-wrapper">
    <h2 class="form-title">
      <el-icon><Edit /></el-icon>
      填写你的需求，AI 为你生成专属食谱
    </h2>

    <el-form ref="formRef" :model="formParams" label-position="top" label-width="auto" size="large">
      <!-- Ingredients -->
      <el-form-item label="🥬 可用食材" prop="ingredients">
        <el-select
          v-model="formParams.ingredients"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入食材名称，按回车添加（如：番茄、鸡蛋、鸡胸肉）"
          :reserve-keyword="false"
          class="full-width"
          :popper-options="{ strategy: 'fixed' }"
        >
          <el-option
            v-for="item in recentIngredients"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-form-item>

      <!-- Taste + Diet Type row -->
      <el-row :gutter="16">
        <el-col :span="12" :xs="24">
          <el-form-item label="🌶️ 口味偏好">
            <el-select v-model="formParams.tastePreference" placeholder="选择口味" clearable class="full-width">
              <el-option v-for="t in TASTE_OPTIONS" :key="t.value" :label="t.label" :value="t.value" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12" :xs="24">
          <el-form-item label="🍽️ 饮食类型">
            <el-radio-group v-model="formParams.dietType" class="diet-type-group">
              <el-radio-button v-for="d in DIET_TYPES" :key="d.value" :value="d.value">
                {{ d.label }}
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- Cooking Time + Servings row -->
      <el-row :gutter="16">
        <el-col :span="12" :xs="24">
          <el-form-item label="⏱️ 最长烹饪时间">
            <div class="slider-wrap">
              <el-slider v-model="formParams.cookingTime" :min="5" :max="180" :step="5" show-input :marks="timeMarks" />
            </div>
          </el-form-item>
        </el-col>
        <el-col :span="12" :xs="24">
          <el-form-item label="👥 用餐人数">
            <el-input-number v-model="formParams.servings" :min="1" :max="10" class="full-width" />
          </el-form-item>
        </el-col>
      </el-row>

      <!-- Recipe count -->
      <el-form-item label="📋 生成数量">
        <el-select v-model="formParams.recipeCount" class="full-width">
          <el-option :value="1" label="1 个食谱" />
          <el-option :value="2" label="2 个食谱" />
          <el-option :value="3" label="3 个食谱" />
        </el-select>
      </el-form-item>

      <!-- Additional notes -->
      <el-form-item label="📝 补充说明">
        <el-input
          v-model="formParams.additionalNotes"
          type="textarea"
          :rows="3"
          placeholder="如：不要放蒜、家里有烤箱、需要低盐等..."
          maxlength="200"
          show-word-limit
        />
      </el-form-item>

      <!-- Submit -->
      <el-button
        type="primary"
        size="large"
        class="submit-btn"
        :loading="isGenerating"
        :disabled="isGenerating"
        @click="$emit('submit')"
      >
        <template v-if="!isGenerating">
          <el-icon><MagicStick /></el-icon> AI 生成食谱
        </template>
        <template v-else>
          <el-icon class="is-loading"><Loading /></el-icon> AI 正在创作中...
        </template>
      </el-button>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { RecipeFormParams } from '@/types/recipe'
import { DIET_TYPES, TASTE_OPTIONS } from '@/types/recipe'
import { Edit, MagicStick, Loading } from '@element-plus/icons-vue'

defineProps<{
  formParams: RecipeFormParams
  isGenerating: boolean
}>()

defineEmits<{
  submit: []
}>()

const recentIngredients = ref<string[]>(
  (() => { try { return JSON.parse(localStorage.getItem('recent-ingredients') || '[]') } catch { return [] } })()
)

// Key time points shown as dots on the slider track (no text to avoid overlap)
// User can read exact value from the input box on the right
const timeMarks: Record<number, string> = {
  5: '', 30: '', 60: '', 120: '', 180: '',
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.recipe-form-wrapper {
  background: #fff;
  padding: 32px;
  border-radius: $radius-xl;
  box-shadow: $shadow-md;
}

.form-title {
  font-size: $font-size-xl;
  font-weight: 700;
  color: $color-text-primary;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.full-width {
  width: 100%;
}

.slider-wrap {
  padding-top: 8px;
}

.diet-type-group {
  :deep(.el-radio-button__inner) {
    padding: 8px 16px;
  }
}

.submit-btn {
  width: 100%;
  height: 52px;
  font-size: $font-size-lg;
  font-weight: 700;
  margin-top: 8px;
  background: linear-gradient(135deg, $color-primary, $color-secondary);
  border: none;
  transition: all $transition-normal;

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, $color-primary-dark, darken($color-secondary, 8%));
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba($color-primary, 0.4);
  }
}
</style>
