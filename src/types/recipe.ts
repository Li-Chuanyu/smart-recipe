export interface Ingredient {
  name: string
  amount: string
  notes: string
}

export interface Step {
  stepNumber: number
  instruction: string
}

export interface Nutrition {
  calories: string
  protein: string
  carbs: string
  fat: string
  fiber: string
}

export interface Recipe {
  id: string
  title: string
  description: string
  cookingTime: string
  prepTime?: string
  difficulty: '简单' | '中等' | '困难'
  dietType: '减脂' | '家常' | '儿童餐' | '素食' | '不限'
  tags: string[]
  servings: number
  ingredients: Ingredient[]
  steps: Step[]
  nutrition: Nutrition
  tips: string
  imageSuggestion?: string
  imageUrl?: string
  // DB-backed fields
  dbId?: number
  userId?: number
  status?: string
  viewCount?: number
  favoriteCount?: number
  isAiGenerated?: boolean
  savedAt?: string
  createdAt?: string
  categoryId?: number
}

export interface RecipeFormParams {
  ingredients: string[]
  tastePreference: string
  cookingTime: number
  dietType: string
  servings: number
  recipeCount: number
  additionalNotes: string
}

export const DEFAULT_FORM_PARAMS: RecipeFormParams = {
  ingredients: [],
  tastePreference: '',
  cookingTime: 30,
  dietType: '家常',
  servings: 2,
  recipeCount: 2,
  additionalNotes: '',
}

export const DIET_TYPES = [
  { label: '减脂', value: '减脂', color: '#67C23A' },
  { label: '家常', value: '家常', color: '#FF6B35' },
  { label: '儿童餐', value: '儿童餐', color: '#E6A23C' },
  { label: '素食', value: '素食', color: '#409EFF' },
  { label: '不限', value: '不限', color: '#909399' },
]

export const TASTE_OPTIONS = [
  { label: '不辣', value: '不辣' },
  { label: '微辣', value: '微辣' },
  { label: '中辣', value: '中辣' },
  { label: '麻辣', value: '麻辣' },
  { label: '清淡', value: '清淡' },
  { label: '酸甜', value: '酸甜' },
  { label: '咸鲜', value: '咸鲜' },
]

export const DIFFICULTY_OPTIONS = [
  { label: '简单', value: '简单' },
  { label: '中等', value: '中等' },
  { label: '困难', value: '困难' },
]
