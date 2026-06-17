import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export function useCopyToClipboard() {
  const justCopied = ref(false)

  async function copyText(text: string) {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(text)
      } else {
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.select()
        document.execCommand('copy')
        document.body.removeChild(textarea)
      }
      justCopied.value = true
      ElMessage.success('已复制到剪贴板')
      setTimeout(() => { justCopied.value = false }, 2000)
    } catch {
      ElMessage.error('复制失败，请手动复制')
    }
  }

  function formatRecipeText(recipe: {
    title: string
    cookingTime: string
    difficulty: string
    servings: number
    ingredients: Array<{ name: string; amount: string; notes?: string }>
    steps: Array<{ stepNumber: number; instruction: string }>
    nutrition?: { calories: string; protein: string; carbs: string; fat: string; fiber: string }
    tips?: string
  }): string {
    const lines: string[] = [
      `【食谱名称】${recipe.title}`,
      `【烹饪时间】${recipe.cookingTime} | 【难度】${recipe.difficulty} | 【份量】${recipe.servings}人份`,
      '',
      '📋 食材：',
    ]
    recipe.ingredients.forEach(i => {
      lines.push(`  - ${i.name} ${i.amount}${i.notes ? `（${i.notes}）` : ''}`)
    })
    lines.push('', '📝 步骤：')
    recipe.steps.forEach(s => {
      lines.push(`  ${s.stepNumber}. ${s.instruction}`)
    })
    if (recipe.nutrition) {
      const n = recipe.nutrition
      lines.push('', `📊 营养信息：热量 ${n.calories} | 蛋白质 ${n.protein} | 碳水 ${n.carbs} | 脂肪 ${n.fat} | 膳食纤维 ${n.fiber}`)
    }
    if (recipe.tips) {
      lines.push('', `💡 小贴士：${recipe.tips}`)
    }
    return lines.join('\n')
  }

  return { justCopied, copyText, formatRecipeText }
}
