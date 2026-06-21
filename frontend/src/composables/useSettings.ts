import { reactive, toRefs } from 'vue'

interface Settings {
  apiBaseUrl: string
  selectedModel: string
  streamMode: boolean
  language: string
}

const state = reactive<Settings>({
  apiBaseUrl: 'https://api.openai.com',
  selectedModel: 'deepseek-v4-flash',
  streamMode: true,
  language: 'zh-CN',
})

export function useSettings() {
  function loadSettings() {
    try {
      const raw = localStorage.getItem('app-settings')
      if (raw) {
        const parsed = JSON.parse(raw)
        Object.assign(state, parsed)
      }
    } catch { /* use defaults */ }
  }

  function saveSettings(settings: Partial<Settings>) {
    Object.assign(state, settings)
    localStorage.setItem('app-settings', JSON.stringify(state))
  }

  function resetDefaults() {
    Object.assign(state, {
      apiBaseUrl: 'https://api.openai.com',
      selectedModel: 'deepseek-v4-flash',
      streamMode: true,
      language: 'zh-CN',
    })
    localStorage.removeItem('app-settings')
  }

  return {
    ...toRefs(state),
    loadSettings,
    saveSettings,
    resetDefaults,
  }
}
