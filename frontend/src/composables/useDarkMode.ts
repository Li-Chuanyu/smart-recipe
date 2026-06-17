import { ref, computed, watch } from 'vue'

type ThemeMode = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'theme-preference'

// Reactive state (singleton)
const theme = ref<ThemeMode>('system')
let initialized = false
let mediaQuery: MediaQueryList | null = null

export function useDarkMode() {
  const isDark = computed(() => {
    if (theme.value === 'system') {
      return mediaQuery?.matches ?? false
    }
    return theme.value === 'dark'
  })

  function applyTheme(dark: boolean) {
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  function persist(mode: ThemeMode) {
    localStorage.setItem(STORAGE_KEY, mode)
  }

  function setTheme(mode: ThemeMode) {
    theme.value = mode
    persist(mode)
    if (mode === 'system') {
      applyTheme(mediaQuery?.matches ?? false)
    } else {
      applyTheme(mode === 'dark')
    }
  }

  function toggleTheme() {
    const next = isDark.value ? 'light' : 'dark'
    setTheme(next)
  }

  function initTheme() {
    if (initialized) return
    initialized = true

    // Setup system media query listener
    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', (e) => {
      if (theme.value === 'system') {
        applyTheme(e.matches)
      }
    })

    // Read stored preference
    const stored = localStorage.getItem(STORAGE_KEY) as ThemeMode | null
    const mode: ThemeMode = stored && ['light', 'dark', 'system'].includes(stored)
      ? stored
      : 'system'
    theme.value = mode

    if (mode === 'system') {
      applyTheme(mediaQuery.matches)
    } else {
      applyTheme(mode === 'dark')
    }
  }

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme,
    initTheme,
  }
}
