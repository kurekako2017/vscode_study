/**
 * React 应用入口
 * 挂载根组件并加载全局样式
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

// React 18 的标准入口：先找到根节点，再把整个应用树挂上去。
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
