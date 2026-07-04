import { svelte } from "@sveltejs/vite-plugin-svelte";
import litestar from "litestar-vite-plugin";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    svelte(),
    litestar({
      input: ["resources/main.ts"],
      bundleDir: "public",
      resourceDir: "resources",
      staticDir: "resources/public",
      inertiaMode: true,
      types: false,
      executor: "pnpm",
    }),
  ],
});
