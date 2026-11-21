import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Financeiro Familiar',
        short_name: 'Financeiro',
        lang: 'pt-BR',
        display: 'standalone',
        start_url: '/',
        theme_color: '#0f766e',
        background_color: '#ffffff',
      },
    }),
  ],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
})
