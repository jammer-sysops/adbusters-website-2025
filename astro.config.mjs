// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import react from "@astrojs/react";
import node from "@astrojs/node";

// https://astro.build/config
export default defineConfig({
  adapter: node({ mode: 'standalone' }),
  integrations: [react()],
  output: 'server',
  vite: {
    plugins: /** @type {any} */ (tailwindcss()),
  },
});
