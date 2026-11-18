import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// The guest page is served by the FastAPI backend at GET /qr, so every
// asset URL must be prefixed with /qr/ (backend/app.py serves
// frontend/dist/index.html at /qr and mounts frontend/dist/assets at
// /qr/assets).
export default defineConfig({
  plugins: [react()],
  base: '/qr/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    // Local dev (npm run dev): proxy API calls to the FastAPI backend
    // started via `python main.py --server-only` (default port 8000).
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
