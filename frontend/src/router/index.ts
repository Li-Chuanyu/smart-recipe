import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      { path: '', name: 'Home', component: () => import('@/views/HomeView.vue') },
      { path: 'generate', name: 'Generate', component: () => import('@/views/GenerateView.vue') },
      { path: 'recipes', name: 'Recipes', component: () => import('@/views/RecipeListView.vue') },
      { path: 'recipe/:id', name: 'RecipeDetail', component: () => import('@/views/RecipeDetailView.vue'), props: true },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/FavoritesView.vue'), meta: { requiresAuth: true } },
      { path: 'community', name: 'Community', component: () => import('@/views/CommunityView.vue') },
      { path: 'community/post/:id', name: 'PostDetail', component: () => import('@/views/PostDetailView.vue'), props: true },
      { path: 'community/write', name: 'PostEditor', component: () => import('@/views/PostEditorView.vue'), meta: { requiresAuth: true } },
      { path: 'login', name: 'Login', component: () => import('@/views/LoginView.vue') },
      { path: 'register', name: 'Register', component: () => import('@/views/RegisterView.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/ProfileView.vue'), meta: { requiresAuth: true } },
      { path: 'settings', name: 'Settings', component: () => import('@/views/SettingsView.vue') },
      { path: 'test', name: 'Test', component: () => import('@/views/TestPage.vue') },
      { path: 'meal-plan', name: 'MealPlan', component: () => import('@/views/MealPlanView.vue') },
      { path: 'shopping-lists', name: 'ShoppingLists', component: () => import('@/views/ShoppingListView.vue') },
      { path: 'shopping-list/:id', name: 'ShoppingListDetail', component: () => import('@/views/ShoppingListDetailView.vue'), props: true },
    ],
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'AdminDashboard', component: () => import('@/views/AdminDashboardView.vue') },
      { path: 'recipes', name: 'AdminRecipes', component: () => import('@/views/AdminRecipesView.vue') },
      { path: 'categories', name: 'AdminCategories', component: () => import('@/views/AdminCategoriesView.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/AdminUsersView.vue') },
      { path: 'community', name: 'AdminCommunity', component: () => import('@/views/AdminCommunityView.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// Auth guard — uses localStorage directly (synchronous, always accurate)
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  let user: any = null
  try { user = JSON.parse(localStorage.getItem('user_info') || 'null') } catch { user = null }

  if (to.meta.requiresAuth && !token) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return next({ name: 'Home' })
  }

  next()
})

export default router
