// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // forward /chat requests to your FastAPI backend
      "/chat": "http://localhost:8000",
    },
  },
});
