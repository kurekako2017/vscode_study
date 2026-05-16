# Sample Projects Index

This folder contains runnable example projects used for local VS Code demonstrations.

Projects

- `react-node-template` — Minimal React (Vite) + Node (Express) example.
  - Start server:
    ```bash
    cd web-projects/sample/react-node-template/server
    npm install
    npm run dev
    ```
  - Start client:
    ```bash
    cd web-projects/sample/react-node-template/client
    npm install
    npm run dev
    ```

- `company-website` — Next.js + Supabase example (frontend + backend schema).
  - Quick start (frontend):
    ```bash
    cd web-projects/sample/company-website/frontend
    pnpm install
    pnpm dev
    ```
  - See `web-projects/sample/company-website/README.md` for full setup and Supabase migration steps.

Tips

- Use VS Code `Run and Debug` → `Run Fullstack` (if configured) to start front+back together for `react-node-template`.
- For `company-website` you may need to create `.env.local` from `.env.example` and fill Supabase keys before running.
