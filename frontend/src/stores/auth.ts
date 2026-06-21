import { ref, computed } from 'vue'

// Reactive global auth state — no Pinia dependency, works everywhere
const _token = ref<string | null>(localStorage.getItem('access_token'))
const _userInfo = ref<any>(null)

try {
  const stored = localStorage.getItem('user_info')
  if (stored) _userInfo.value = JSON.parse(stored)
} catch { /* ignore */ }

export const isAuthenticated = computed(() => !!_token.value)
export const isAdmin = computed(() => _userInfo.value?.role === 'admin')
export const userInfo = computed(() => _userInfo.value)

export function setTokens(access: string, refresh: string) {
  _token.value = access
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}

export function setUserInfo(info: any) {
  _userInfo.value = info
  localStorage.setItem('user_info', JSON.stringify(info))
}

export function logout() {
  _token.value = null
  _userInfo.value = null
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_info')
}
