import { defineConfig } from '@tanstack/start/config'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
  tsr: {
    appDirectory: 'app',
    routesDirectory: 'app/routes',
  },
})
