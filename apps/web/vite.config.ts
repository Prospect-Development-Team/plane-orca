import path from "node:path";
import * as dotenv from "dotenv";
import { reactRouter } from "@react-router/dev/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";
// Custom override: import local package.json as a fallback version source for local dev.
// In Docker builds, VITE_APP_VERSION env var (set inline in Dockerfile.web) takes precedence.
import localPackageJson from "./package.json";

dotenv.config({ path: path.resolve(__dirname, ".env") });

// Expose only vars starting with VITE_
const viteEnv = Object.keys(process.env)
  .filter((k) => k.startsWith("VITE_"))
  .reduce<Record<string, string>>((a, k) => {
    a[k] = process.env[k] ?? "";
    return a;
  }, {});

// Custom override: inject the root workspace version at build time.
// VITE_APP_VERSION is set inline in Dockerfile.web before the build command,
// reading from the root package.json before turbo prune reorganizes the file tree.
// Falls back to the local apps/web/package.json version in local dev.
viteEnv["VITE_APP_VERSION"] = process.env.VITE_APP_VERSION || localPackageJson.version;

export default defineConfig(() => ({
  define: {
    "process.env": JSON.stringify(viteEnv),
  },
  build: {
    assetsInlineLimit: 0,
  },
  plugins: [reactRouter(), tsconfigPaths({ projects: [path.resolve(__dirname, "tsconfig.json")] })],
  resolve: {
    alias: {
      // Custom override: redirect package.json imports to root workspace package.json
      // This ensures version-number.tsx displays the fork version in local dev.
      // In Docker builds, VITE_APP_VERSION env var takes precedence (set in Dockerfile.web).
      "package.json": path.resolve(__dirname, "../../package.json"),
      // Next.js compatibility shims used within web
      "next/link": path.resolve(__dirname, "app/compat/next/link.tsx"),
      "next/navigation": path.resolve(__dirname, "app/compat/next/navigation.ts"),
      "next/script": path.resolve(__dirname, "app/compat/next/script.tsx"),
    },
    dedupe: ["react", "react-dom", "@headlessui/react"],
  },
  server: {
    host: "127.0.0.1",
  },
  // No SSR-specific overrides needed; alias resolves to ESM build
}));
