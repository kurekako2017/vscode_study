/**
 * React 浏览器入口。
 * Vite 加载本文件后，将 App 挂载到 index.html 的 #root，并加载全局样式。
 * StrictMode 帮助本地开发发现副作用问题；业务 API 与状态逻辑均位于 App/api。
 * 企业级可在此组合 Router、ErrorBoundary 和观测 Provider，但不放业务审批规则。
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App";
import "./styles.css";

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
