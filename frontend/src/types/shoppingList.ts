export interface ShoppingItem {
  id: number
  shoppingListId?: number
  name: string
  amount: string
  category: string
  checked: boolean
  sortOrder?: number
}

export interface ShoppingList {
  id: number
  name: string
  sourceType: 'manual' | 'meal_plan' | 'recipes'
  sourceId?: number | null
  items: ShoppingItem[]
  itemCount?: number
  checkedCount?: number
  createdAt?: string
}

export const CATEGORY_CONFIG: Record<string, { icon: string; color: string }> = {
  '肉类': { icon: '🥩', color: '#F56C6C' },
  '蔬菜': { icon: '🥬', color: '#67C23A' },
  '调料': { icon: '🧂', color: '#E6A23C' },
  '主食': { icon: '🍚', color: '#FF6B35' },
  '乳制品': { icon: '🥛', color: '#409EFF' },
  '蛋类': { icon: '🥚', color: '#E6A23C' },
  '豆制品': { icon: '🫘', color: '#67C23A' },
  '其他': { icon: '🛒', color: '#909399' },
  '调料(家中常备)': { icon: '🧂', color: '#E6A23C' },
}
