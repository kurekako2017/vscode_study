import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App";
import "./styles.css";

// 入口文件只负责把根组件挂载到 HTML；业务状态留在 App，API 调用留在 api.ts。
createRoot(document.getElementById("root")!).render(
  // StrictMode 会在开发阶段帮助发现不安全的副作用和缺失的资源清理。
  <StrictMode>
    <App />
  </StrictMode>,
);
