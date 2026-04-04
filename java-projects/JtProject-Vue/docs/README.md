# JtProject-Vue 文档总索引

这个目录是 `JtProject-Vue` 的项目级文档入口，重点服务于：

- Vue 页面学习
- 前后端分离结构理解
- 组件、页面、Composables 和 Service 拆分学习
- 页面与后端 API 联动关系梳理

相关入口：

- 项目根入口：[README.md](../README.md)
- Java 项目总导航：[Java项目总启动导航.md](../../Java项目总启动导航.md)
- Java 项目文档入口：[doc/README.md](../../doc/README.md)

## 建议先看

如果你是第一次看这个项目，推荐顺序：

1. [README.md](../README.md)
2. [vue-learning-path.md](./vue-learning-path.md)
3. [vue-framework-notes.md](./vue-framework-notes.md)
4. [project-code-map.md](./project-code-map.md)
5. [composables-learning-guide.md](./composables-learning-guide.md)

## 文档分区

### 学习路线

- [vue-learning-path.md](./vue-learning-path.md)

适合按顺序学习 Vue 页面、状态和项目演进路线。

### 框架与概念

- [vue-framework-notes.md](./vue-framework-notes.md)
- [composables-learning-guide.md](./composables-learning-guide.md)

适合理解 Vue 关键概念、响应式状态和组合式函数用法。

### 项目结构与页面组织

- [project-code-map.md](./project-code-map.md)
- [page-structure-guide.md](./page-structure-guide.md)

适合理解目录结构、页面拆分、组件边界和服务层组织。

## 前端源码入口

如果你想边读文档边看 Vue 代码，可以从这里开始：

- 前端入口：[main.ts](../frontend/src/main.ts)
- 前端主页面：[App.vue](../frontend/src/App.vue)
- 全局样式：[style.css](../frontend/src/style.css)
- 状态组合：[useAppStore.ts](../frontend/src/composables/useAppStore.ts)
- 业务 Service：[appService.ts](../frontend/src/services/appService.ts)

## 后端源码入口

虽然这是 Vue 学习版，但后端仍然是 Spring Boot，可以从这里往下看：

- API 控制器：[ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
- 用户控制器：[UserController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)
- 管理员控制器：[AdminController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)

## 使用建议

- 想先把项目跑起来：先看 [README.md](../README.md)
- 想按路线学习 Vue：先看 [vue-learning-path.md](./vue-learning-path.md)
- 想先理解项目结构：先看 [project-code-map.md](./project-code-map.md)
- 想重点学 Composables：先看 [composables-learning-guide.md](./composables-learning-guide.md)
