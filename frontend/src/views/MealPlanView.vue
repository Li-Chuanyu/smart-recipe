<template>
  <div class="meal-plan-page">
    <div class="container">
      <div class="page-header">
        <h1>📅 每周食谱计划</h1>
        <p>规划一周的饮食，告别"今天吃什么"的烦恼</p>
      </div>

      <!-- Week navigation -->
      <div class="week-nav">
        <el-button :icon="ArrowLeft" circle @click="prevWeek" />
        <span class="week-label">{{ weekLabel }}</span>
        <el-button :icon="ArrowRight" circle @click="nextWeek" />
        <el-button type="primary" @click="$router.push('/shopping-lists')" style="margin-left: auto;">
          🛒 购物清单
        </el-button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-wrap">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        <p>加载中...</p>
      </div>

      <!-- Calendar -->
      <div v-else class="calendar-wrap">
        <MealPlanCalendar
          :entries="plan.entries"
          :week-start="plan.weekStart"
          @add-entry="handleAddEntry"
          @remove-entry="handleRemoveEntry"
        />

        <div class="plan-actions">
          <el-button type="success" size="large" @click="generateShoppingList">
            🛒 从本周计划生成购物清单
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { recipeApi } from '@/api/recipe'
import MealPlanCalendar from '@/components/meal-plan/MealPlanCalendar.vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ArrowRight, Loading } from '@element-plus/icons-vue'

const router = useRouter()

const loading = ref(true)

// --- LocalStorage-based meal plan (no login required) ---
interface LocalEntry {
  recipeId: number
  recipeData?: any
  dayOfWeek: number
  mealType: string
}
interface LocalPlan {
  weekStart: string
  entries: LocalEntry[]
}

const STORAGE_PREFIX = 'meal_plan_'

function getMonday(date: Date): string {
  const d = new Date(date)
  d.setDate(d.getDate() - d.getDay() + 1)
  return d.toISOString().slice(0, 10)
}

const currentMonday = ref(getMonday(new Date()))
const localEntries = ref<LocalEntry[]>([])

const weekLabel = computed(() => {
  const monday = new Date(currentMonday.value + 'T00:00:00')
  const sunday = new Date(monday)
  sunday.setDate(sunday.getDate() + 6)
  const fmt = (d: Date) => `${d.getMonth() + 1}月${d.getDate()}日`
  return `${fmt(monday)} - ${fmt(sunday)}`
})

const plan = computed<LocalPlan>(() => ({
  weekStart: currentMonday.value,
  entries: localEntries.value
}))

function loadPlan() {
  loading.value = true
  try {
    const raw = localStorage.getItem(STORAGE_PREFIX + currentMonday.value)
    localEntries.value = raw ? JSON.parse(raw) : []
  } catch { localEntries.value = [] }
  finally { loading.value = false }
}

onMounted(() => loadPlan())

function savePlan() {
  if (localEntries.value.length > 0) {
    localStorage.setItem(STORAGE_PREFIX + currentMonday.value, JSON.stringify(localEntries.value))
  } else {
    localStorage.removeItem(STORAGE_PREFIX + currentMonday.value)
  }
}

function prevWeek() {
  const d = new Date(currentMonday.value + 'T00:00:00')
  d.setDate(d.getDate() - 7)
  currentMonday.value = getMonday(d)
  loadPlan()
}

function nextWeek() {
  const d = new Date(currentMonday.value + 'T00:00:00')
  d.setDate(d.getDate() + 7)
  currentMonday.value = getMonday(d)
  loadPlan()
}

async function handleAddEntry(entry: { recipe_id: number; day_of_week: number; meal_type: string }) {
  // Remove existing entry for this slot
  localEntries.value = localEntries.value.filter(
    e => !(e.dayOfWeek === entry.day_of_week && e.mealType === entry.meal_type)
  )
  // Fetch recipe data to store locally
  let recipeData: any = null
  try {
    const res = await recipeApi.getDetail(entry.recipe_id)
    recipeData = res.data
  } catch { /* recipe fetch failed, store without details */ }
  localEntries.value.push({
    recipeId: entry.recipe_id,
    recipeData,
    dayOfWeek: entry.day_of_week,
    mealType: entry.meal_type,
  })
  savePlan()
  ElMessage.success('已添加食谱')
}

function handleRemoveEntry(entryId: number) {
  localEntries.value = localEntries.value.filter(e => e.recipeId !== entryId)
  savePlan()
  ElMessage.success('已移除食谱')
}

function generateShoppingList() {
  // Extract number and unit from amount string (e.g. "2个" → [2, "个"], "500克" → [500, "克"])
  function parseAmount(a: string): [number, string] {
    const match = a.match(/^([\d.]+)\s*(\S*)/)
    if (match) return [parseFloat(match[1]), match[2] || '']
    return [0, a] // "适量", "少许" etc → 0 quantity
  }

  // Combine two amounts intelligently
  function combineAmounts(a: string, b: string): string {
    const [numA, unitA] = parseAmount(a)
    const [numB, unitB] = parseAmount(b)
    // Both have numbers with same unit → sum
    if (numA > 0 && numB > 0 && unitA === unitB) {
      const total = numA + numB
      return total % 1 === 0 ? `${total}${unitA}` : `${total.toFixed(1)}${unitA}`
    }
    // One has number, other doesn't
    if (numA > 0 && numB === 0) return a
    if (numB > 0 && numA === 0) return b
    // Both non-numeric — just keep one
    if (a === b) return a
    return a  // keep first when can't merge
  }

  // Seasonings that most people already have — exclude from shopping list
  const HAS_AT_HOME = /^(盐|白糖|糖|酱油|生抽|老抽|料酒|醋|陈醋|白醋|蚝油|味精|鸡精|鸡粉|胡椒粉|花椒粉|花椒|五香粉|淀粉|生粉|食用油|色拉油|香油|麻油|辣椒油|豆瓣酱|番茄酱|番茄沙司)$/

  const allIngredients: Array<{name: string, amount: string}> = []

  for (const entry of localEntries.value) {
    if (entry.recipeData?.ingredients) {
      for (const ing of entry.recipeData.ingredients) {
        const name = ing.name.trim()
        if (!name) continue
        // Skip common seasonings — not needed on shopping list
        if (HAS_AT_HOME.test(name)) continue
        // Regular ingredient
        const existing = allIngredients.find(i => i.name === name)
        if (existing) {
          existing.amount = combineAmounts(existing.amount, ing.amount || '适量')
        } else {
          allIngredients.push({ name, amount: ing.amount || '适量' })
        }
      }
    }
  }

  if (!allIngredients.length && !seasonings.length) {
    ElMessage.warning('当前计划中没有食谱')
    return
  }

  const listsRaw = localStorage.getItem('shopping_lists') || '[]'
  const lists = JSON.parse(listsRaw)

  // Categorize regular ingredients
  const categories: Record<string, Array<{name: string, amount: string, checked: boolean}>> = {}
  const rules: Array<[string, RegExp]> = [
    ['肉类', /肉|鸡|鸭|鱼|虾|蟹|贝|牛|猪|羊|排骨|培根|香肠|火腿/i],
    ['蔬菜', /菜|白菜|青菜|菠菜|生菜|番茄|西红柿|土豆|萝卜|黄瓜|茄子|豆角|青椒|辣椒|洋葱|西兰花|花菜|芹菜|玉米|南瓜|冬瓜|苦瓜|蘑菇|香菇|木耳|藕|笋|韭|蒜|姜|葱|香菜/i],
    ['蛋类', /蛋|鸡蛋|鸭蛋|鹌鹑蛋/i],
    ['豆制品', /豆腐|豆皮|豆浆|豆干|腐竹|千张|毛豆/i],
    ['乳制品', /奶|牛奶|酸奶|黄油|芝士|奶油|奶酪/i],
    ['主食', /米|面$|面粉|面包|馒头|饼|面条|饺子|馄饨|年糕|粉丝|意面/i],
  ]

  for (const ing of allIngredients) {
    let cat = '其他'
    for (const [c, re] of rules) {
      if (re.test(ing.name)) { cat = c; break }
    }
    if (!categories[cat]) categories[cat] = []
    categories[cat].push({ name: ing.name, amount: ing.amount, checked: false })
  }

  // Seasonings are skipped entirely — everyone has them at home

  const items = Object.entries(categories).map(([cat, catItems]) =>
    catItems.map(i => ({ ...i, category: cat }))
  ).flat()

  const newList = {
    id: Date.now(),
    name: `${currentMonday.value} 采购清单`,
    items,
    createdAt: new Date().toISOString(),
  }
  lists.unshift(newList)
  localStorage.setItem('shopping_lists', JSON.stringify(lists))
  ElMessage.success('购物清单已生成')
  router.push(`/shopping-list/${newList.id}`)
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.meal-plan-page {
  padding: 32px 0 64px;
}

.week-nav {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.week-label {
  font-size: $font-size-lg;
  font-weight: 700;
  color: var(--app-text-primary, $color-text-primary);
  min-width: 200px;
  text-align: center;
}

.loading-wrap {
  text-align: center;
  padding: 80px;
  color: var(--app-text-secondary, $color-text-secondary);
}

.calendar-wrap {
  margin-bottom: 32px;
}

.plan-actions {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.error-wrap {
  margin-top: 48px;
}
</style>
