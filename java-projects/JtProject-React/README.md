# JtProject-React 学习与启动入口

相关入口：

- 项目总导航：[Java项目总启动导航.md](../Java项目总启动导航.md)
- Java 项目根入口：[README.md](../README.md)
- 项目文档总入口：[docs/README.md](./docs/README.md)

## 项目说明

这个目录是从原始 `JtProject` 复制出来的独立项目，改造成了：

- 后端：Spring Boot
- 前端：React + TypeScript + Vite
- 后端端口：`8083`
- 前端端口：`5173`
- 数据库改为本地 H2 文件库，路径在项目 `data/` 目录下
- 原始 `JtProject` 保持不变，这里是独立副本

## 快速启动（Windows / PowerShell）

启动后端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React
.\mvnw.cmd spring-boot:run
```

后端接口基地址：

```text
http://localhost:8083/api
```

启动前端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-React\frontend
npm install
npm run dev
```

前端页面地址：

```text
http://localhost:5173
```

## 账号与验证

默认账号：

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

验证建议：

1. 先启动后端
2. 再启动 `frontend` 前端开发服务器
3. 打开首页后测试登录、商品列表、后台页面

## 学习重点

- React 组件拆分
- 页面状态管理
- Hooks 用法
- 前端 Service 调用后端 API

## 学习文档

- 学习入口：[docs/README.md](./docs/README.md)
- React 学习路线：[docs/react-learning-path.md](./docs/react-learning-path.md)
- React 框架速查：[docs/react-framework-notes.md](./docs/react-framework-notes.md)
- 项目源码导读：[docs/project-code-map.md](./docs/project-code-map.md)

## 使用建议

1. 先把后端和前端都跑起来
2. 再看 `frontend/src/` 下的页面、路由和组件
3. 然后对照后端 Controller 和接口
4. 最后回看文档理解 React 版的页面组织方式
