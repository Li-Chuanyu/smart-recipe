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
      <div v-else-if="plan" class="calendar-wrap">
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

      <!-- Error state -->
      <div v-else class="error-wrap">
        <ErrorState
          icon="warning"
          title="无法加载食谱计划"
          message="请确保已登录"
          retryable
          @retry="loadPlan"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { mealPlanApi } from '@/api/mealPlan'
import { shoppingListApi } from '@/api/shoppingList'
import type { MealPlan } from '@/types/mealPlan'
import MealPlanCalendar from '@/components/meal-plan/MealPlanCalendar.vue'
import ErrorState from '@/components/common/ErrorState.vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, ArrowRight, Loading } from '@element-plus/icons-vue'

const router = useRouter()

const plan = ref<MealPlan | null>(null)
const loading = ref(true)

// Calculate current week Monday
function getMonday(date: Date): string {
  const d = new Date(date)
  d.setDate(d.getDate() - d.getDay() + 1) // Monday
  return d.toISOString().slice(0, 10)
}

const currentMonday = ref(getMonday(new Date()))

const weekLabel = computed(() => {
  const monday = new Date(currentMonday.value + 'T00:00:00')
  const sunday = new Date(monday)
  sunday.setDate(sunday.getDate() + 6)
  const fmt = (d: Date) => `${d.getMonth() + 1}月${d.getDate()}日`
  return `${fmt(monday)} - ${fmt(sunday)}`
})

onMounted(() => loadPlan())

async function loadPlan() {
  loading.value = true
  try {
    const res = await mealPlanApi.getPlanByWeek(currentMonday.value)
    if (res.data) {
      plan.value = res.data
    } else {
      // Auto-create a plan for this week
      const createRes = await mealPlanApi.createPlan({ week_start: currentMonday.value })
      plan.value = createRes.data
    }
  } catch {
    plan.value = null
  } finally {
    loading.value = false
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
  if (!plan.value) return
  try {
    await mealPlanApi.addEntry(plan.value.id, entry)
    await loadPlan()
    ElMessage.success('已添加食谱')
  } catch { /* handled */ }
}

async function handleRemoveEntry(entryId: number) {
  if (!plan.value) return
  try {
    await mealPlanApi.removeEntry(plan.value.id, entryId)
    await loadPlan()
    ElMessage.success('已移除食谱')
  } catch { /* handled */ }
}

async function generateShoppingList() {
  if (!plan.value) return
  try {
    const res = await shoppingListApi.generateFromMealPlan(
      plan.value.id,
      `${currentMonday.value} 采购清单`
    )
    ElMessage.success('购物清单已生成')
    router.push(`/shopping-list/${res.data.id}`)
  } catch { /* handled */ }
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
