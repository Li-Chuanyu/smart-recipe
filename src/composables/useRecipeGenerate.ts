import { ref, reactive } from 'vue'
import { recipeApi } from '@/api/recipe'
import type { Recipe, RecipeFormParams } from '@/types/recipe'
import { DEFAULT_FORM_PARAMS } from '@/types/recipe'
import { ElMessage } from 'element-plus'

type GenerationState = 'idle' | 'generating' | 'success' | 'error'

const formParams = reactive<RecipeFormParams>({ ...DEFAULT_FORM_PARAMS })
const generatedRecipes = ref<Recipe[]>([])
const generationState = ref<GenerationState>('idle')
const generationError = ref('')
const streamedPreview = ref('')

export function useRecipeGenerate() {
  async function generate() {
    if (!formParams.ingredients.length && !formParams.tastePreference) {
      ElMessage.warning('请至少填写食材或口味偏好')
      return
    }

    generationState.value = 'generating'
    generationError.value = ''
    streamedPreview.value = ''

    try {
      const response = await recipeApi.generate({ ...formParams })
      generatedRecipes.value = response.data || []
      generationState.value = 'success'
      ElMessage.success(`成功生成 ${generatedRecipes.value.length} 个食谱`)
    } catch (err: any) {
      generationState.value = 'error'
      generationError.value = err.response?.data?.message || err.message || '食谱生成失败，请重试'
      ElMessage.error(generationError.value)
    }
  }

  function clearResults() {
    generatedRecipes.value = []
    generationState.value = 'idle'
    generationError.value = ''
    streamedPreview.value = ''
  }

  function resetForm() {
    Object.assign(formParams, { ...DEFAULT_FORM_PARAMS })
    clearResults()
  }

  return {
    formParams,
    generatedRecipes,
    generationState,
    generationError,
    streamedPreview,
    generate,
    clearResults,
    resetForm,
  }
}
