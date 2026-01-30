import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Permet l'accès depuis n'importe quel domaine
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
    hmr: {
      clientPort: 443, // Port HTTPS pour Cloudflare
    },
  },
  preview: {
    host: '0.0.0.0', // Permet l'accès depuis n'importe quelle IP
    port: 4173,
    strictPort: false,
    allowedHosts: [
      'salescoach-frontend.onrender.com',
      '.onrender.com', // Autorise tous les sous-domaines onrender.com
    ],
  },
})
