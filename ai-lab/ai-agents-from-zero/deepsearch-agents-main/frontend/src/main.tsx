// 前端入口文件：
// 1. 先加载全局样式和 Ant Design 的重置样式
// 2. 再配置统一主题
// 3. 最后把 App 挂载到 index.html 里的 #root 节点
import "antd/dist/reset.css";
import { App as AntApp, ConfigProvider, theme } from "antd";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {/* ConfigProvider 是 Ant Design 的全局主题入口。
        初学者可以把它理解成“整个站点的 UI 配色和控件默认值配置中心”。 */}
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: "#20d6ff",
          colorSuccess: "#5dff9f",
          colorWarning: "#ffc857",
          colorError: "#ff5c7a",
          colorInfo: "#7c8cff",
          colorBgBase: "#05070b",
          colorBgContainer: "rgba(12, 18, 28, 0.86)",
          colorBorder: "rgba(113, 247, 255, 0.18)",
          borderRadius: 8,
          fontFamily:
            "'IBM Plex Sans', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
          fontFamilyCode:
            "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
        },
        components: {
          Button: {
            controlHeightLG: 46,
            primaryShadow: "0 0 24px rgba(32, 214, 255, 0.26)"
          },
          Input: {
            activeBorderColor: "#20d6ff",
            hoverBorderColor: "#5dff9f"
          }
        }
      }}
    >
      {/* AntApp 提供 message、modal 这类全局反馈能力。 */}
      <AntApp>
        <App />
      </AntApp>
    </ConfigProvider>
  </React.StrictMode>
);
