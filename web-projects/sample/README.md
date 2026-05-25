# 示例项目索引

此目录包含用于在本地 VS Code 中演示的可运行示例项目。

项目列表

- `react-node-template` — 最小的 React (Vite) + Node (Express) 示例。
  - 启动后端：
    ```bash
    cd web-projects/sample/react-node-template/server
    npm install
    npm run dev
    ```
  - 启动前端：
    ```bash
    cd web-projects/sample/react-node-template/client
    npm install
    npm run dev
    ```

- `company-website` — 基于 Next.js + Supabase 的示例（含前端与后端 schema）。
  - 快速启动（仅前端）：
    ```bash
    cd web-projects/sample/company-website/frontend
    pnpm install
    pnpm dev
    ```
  - 完整配置与 Supabase 迁移请参见：`web-projects/sample/company-website/README.md`

提示

- 可在 VS Code 中使用“运行和调试（Run and Debug）”→ 选择 `Run Fullstack`（如果已配置）一次性启动 `react-node-template` 的前后端。
- 运行 `company-website` 前，请根据 `frontend/.env.example` 复制并填写 `.env.local`（需要 Supabase 的 URL 与 Key）。

