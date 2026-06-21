import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        configure: (proxy: any) => {
          proxy.on('proxyRes', (proxyRes: any) => {
            // Rewrite 308 redirect Location to avoid cross-origin issues
            if (proxyRes.statusCode >= 300 && proxyRes.statusCode < 400) {
              const loc = proxyRes.headers['location']
              if (loc) {
                proxyRes.headers['location'] = loc.replace('http://localhost:5001', '')
              }
            }
          })
        },
      },
      '/uploads': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
        },
      },
    },
  },
})
