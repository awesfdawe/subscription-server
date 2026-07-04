# subscription-server

Simple Litestar + Svelte Inertia boilerplate with `pnpm`, `vite`, `svelte`, `typescript`, `tailwindcss`, `daisyui`, `eslint`, and `prettier`.

## Structure

```text
backend/
  app.py
  config.py
  controllers/
  middleware/
  schemas/
  services/

frontend/
  package.json
  vite.config.ts
  tsconfig.json
  svelte.config.js
  eslint.config.js
  prettier.config.cjs
  postcss.config.js
  index.html
  resources/
```

## Backend dev

```bash
litestar --app backend.app:app run
```

Set `VITE_DEV_MODE=false` to use built frontend assets.

## Frontend setup

```bash
cd frontend
pnpm install
```

The normal development flow is to run Litestar and let `litestar-vite` handle Vite integration.
