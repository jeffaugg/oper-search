// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Altere para a URL do seu servidor de API
        changeOrigin: true,
        secure: false
      }
    }
  }
})
