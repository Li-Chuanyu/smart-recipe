<template>
  <div class="meal-calendar">
    <!-- Header row: empty corner + day labels -->
    <div class="calendar-header">
      <div class="corner-cell"></div>
      <div v-for="day in 7" :key="day" class="day-header" :class="{ today: isToday(day - 1) }">
        <span class="day-name">{{ DAY_LABELS[day - 1] }}</span>
        <span class="day-date">{{ getDayDate(day - 1) }}</span>
      </div>
    </div>

    <!-- Meal rows -->
    <div v-for="mealType in mealTypes" :key="mealType" class="meal-row">
      <div class="meal-label">
        <span class="meal-icon">{{ MEAL_ICONS[mealType] }}</span>
        <span>{{ MEAL_LABELS[mealType] }}</span>
      </div>
      <div v-for="day in 7" :key="day" class="meal-slot" :class="{ filled: getEntry(day - 1, mealType) }">
        <template v-if="getEntry(day - 1, mealType)">
          <div class="slot-content">
            <span class="slot-title">{{ getEntry(day - 1, mealType)?.recipeData?.title }}</span>
            <el-button
              text
              size="small"
              type="danger"
              class="slot-remove"
              @click.stop="removeEntry(day - 1, mealType)"
            >
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </template>
        <template v-else>
          <div class="slot-empty" @click="openPicker(day - 1, mealType)">
            <el-icon><Plus /></el-icon>
          </div>
        </template>
      </div>
    </div>

    <!-- Recipe picker dialog -->
    <RecipePickerDialog
      v-model:visible="pickerVisible"
      @select="onRecipeSelected"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { MealType, MealPlanEntry } from '@/types/mealPlan'
import { DAY_LABELS, MEAL_LABELS, MEAL_ICONS } from '@/types/mealPlan'
import type { Recipe } from '@/types/recipe'
import RecipePickerDialog from './RecipePickerDialog.vue'
import { Plus, Close } from '@element-plus/icons-vue'

const props = defineProps<{
  entries: MealPlanEntry[]
  weekStart: string
}>()

const emit = defineEmits<{
  'add-entry': [entry: { recipe_id: number; day_of_week: number; meal_type: string }]
  'remove-entry': [recipeId: number]
}>()

const mealTypes: MealType[] = ['breakfast', 'lunch', 'dinner']
const pickerVisible = ref(false)
const pendingDay = ref(0)
const pendingMealType = ref<MealType>('lunch')

const weekStartDate = computed(() => new Date(props.weekStart + 'T00:00:00'))

function getDayDate(dayIndex: number): string {
  const d = new Date(weekStartDate.value)
  d.setDate(d.getDate() + dayIndex)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function isToday(dayIndex: number): boolean {
  const d = new Date(weekStartDate.value)
  d.setDate(d.getDate() + dayIndex)
  const today = new Date()
  return d.toDateString() === today.toDateString()
}

function getEntry(day: number, mealType: MealType): MealPlanEntry | undefined {
  return props.entries.find(e => e.dayOfWeek === day && e.mealType === mealType)
}

function openPicker(day: number, mealType: MealType) {
  pendingDay.value = day
  pendingMealType.value = mealType
  pickerVisible.value = true
}

function onRecipeSelected(recipe: Recipe) {
  emit('add-entry', {
    recipe_id: recipe.dbId!,
    day_of_week: pendingDay.value,
    meal_type: pendingMealType.value,
  })
}

function removeEntry(day: number, mealType: MealType) {
  const entry = getEntry(day, mealType)
  if (entry?.recipeId) {
    emit('remove-entry', entry.recipeId)
  }
}
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as *;

.meal-calendar {
  background: var(--app-card-bg, #fff);
  border-radius: $radius-xl;
  box-shadow: $shadow-sm;
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: 80px repeat(7, 1fr);
  background: $color-primary;
  color: #fff;
}

.corner-cell {
  padding: 12px;
  border-right: 1px solid rgba(255,255,255,0.2);
}

.day-header {
  text-align: center;
  padding: 12px 4px;
  border-right: 1px solid rgba(255,255,255,0.15);

  &:last-child { border-right: none; }

  &.today {
    background: rgba(255,255,255,0.15);
    font-weight: 700;
  }

  .day-name {
    display: block;
    font-size: $font-size-sm;
    font-weight: 600;
  }

  .day-date {
    display: block;
    font-size: $font-size-xs;
    opacity: 0.8;
    margin-top: 2px;
  }
}

.meal-row {
  display: grid;
  grid-template-columns: 80px repeat(7, 1fr);
  border-bottom: 1px solid var(--app-border-light, $color-border-light);

  &:last-child { border-bottom: none; }
}

.meal-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 8px;
  background: var(--app-bg-warm, $color-bg-warm);
  border-right: 1px solid var(--app-border-light, $color-border-light);
  font-size: $font-size-sm;
  font-weight: 600;
  color: var(--app-text-primary, $color-text-primary);

  .meal-icon {
    font-size: 18px;
    margin-bottom: 2px;
  }
}

.meal-slot {
  min-height: 60px;
  padding: 6px;
  border-right: 1px solid var(--app-border-light, $color-border-light);
  display: flex;
  align-items: center;
  justify-content: center;

  &:last-child { border-right: none; }

  &.filled {
    background: rgba($color-primary, 0.04);
  }
}

.slot-empty {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--app-border, $color-border);
  border-radius: $radius-round;
  cursor: pointer;
  color: var(--app-text-secondary, $color-text-secondary);
  transition: all $transition-fast;

  &:hover {
    border-color: $color-primary;
    color: $color-primary;
    background: rgba($color-primary, 0.06);
  }
}

.slot-content {
  position: relative;
  width: 100%;
  text-align: center;
  padding: 6px 24px;
}

.slot-title {
  font-size: $font-size-xs;
  font-weight: 600;
  color: $color-primary;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.slot-remove {
  position: absolute;
  top: 0;
  right: 0;
  padding: 2px;
  min-height: auto;
}

@media (max-width: $breakpoint-md) {
  .calendar-header {
    grid-template-columns: 56px repeat(7, 1fr);
  }
  .meal-row {
    grid-template-columns: 56px repeat(7, 1fr);
  }
  .day-header {
    padding: 8px 2px;
    .day-name { font-size: $font-size-xs; }
    .day-date { font-size: 10px; }
  }
  .meal-label {
    padding: 8px 4px;
    font-size: $font-size-xs;
  }
}
</style>
