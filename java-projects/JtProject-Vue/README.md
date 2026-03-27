# JtProject Vue

这个目录是从原始 `JtProject` 复制出来的独立项目，改造成了：

- 后端：Spring Boot
- 前端：Vue 3 + TypeScript + Vite
- 后端端口：`8084`
- 前端端口：`5174`

## 启动后端

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue
.\mvnw.cmd spring-boot:run
```

后端接口基地址：

```text
http://localhost:8084/api
```

## 启动前端

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Vue\frontend
npm install
npm run dev
```

前端页面地址：

```text
http://localhost:5174
```

## 默认账号

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

## 说明

- 数据库改为本地 H2 文件库，路径在项目 `data/` 目录下。
- 原始 `JtProject` 保持不变，这里是独立副本。

## 学习文档

- 学习入口：[docs/README.md](/d:/dev/source_code/vscode_study/java-projects/JtProject-Vue/docs/README.md)
- Vue 学习路线：[docs/vue-learning-path.md](/d:/dev/source_code/vscode_study/java-projects/JtProject-Vue/docs/vue-learning-path.md)
- Vue 框架速查：[docs/vue-framework-notes.md](/d:/dev/source_code/vscode_study/java-projects/JtProject-Vue/docs/vue-framework-notes.md)
- 项目源码导读：[docs/project-code-map.md](/d:/dev/source_code/vscode_study/java-projects/JtProject-Vue/docs/project-code-map.md)
