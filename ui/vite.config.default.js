import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const DEV_API_URL = 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': {
        target: DEV_API_URL,
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          // Configure the proxy instance
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // Access the proxyReq object, req, and res for custom logic
            //console.log('Proxy request:', req.method, req.url);
            // Example: Modify headers before sending the request
            proxyReq.setHeader('Origin', DEV_API_URL);
          });
        }
      }
    }
  }
})
