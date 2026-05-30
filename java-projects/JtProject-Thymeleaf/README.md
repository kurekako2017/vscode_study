# JtProject-Thymeleaf 学习与启动入口

相关入口：

- 项目总导航：[Java项目总启动导航.md](../Java项目总启动导航.md)
- Java 项目根入口：[README.md](../README.md)
- 项目文档总入口：[doc/README.md](./doc/README.md)

## 项目说明

这个目录是从原始 `JtProject` 复制出来的独立学习项目，改造成了：

- 后端：Spring Boot
- 页面模板：Thymeleaf
- 数据库：本地 H2 文件库
- 端口：`8085`

这个项目的目标不是一次性把原 JSP 全部 1:1 改完，而是提供一套最小可学习版本，让你能用同一份业务逻辑对照学习：

- JSP 怎么写
- Thymeleaf 怎么写
- React / Vue 又怎么写

## 快速启动（Windows / PowerShell）

启动后端：

```powershell
cd d:\dev\source_code\vscode_study\java-projects\JtProject-Thymeleaf
.\mvnw.cmd spring-boot:run
```

启动后访问：

```text
http://localhost:8085/
```

H2 控制台：

```text
http://localhost:8085/h2-console
```

## 账号与验证

默认账号：

- 普通用户：`lisa / 765`
- 管理员：`admin / 123`

验证建议：

1. 先访问 `/`
2. 测试用户登录和管理员登录
3. 再进入商品、分类、购物车等页面观察模板渲染

## 页面入口

- 用户登录：`/`
- 用户注册：`/register`
- 首页：`/index`
- 商品列表：`/user/products`
- 购物车：`/user/cart`
- 管理员登录：`/admin/login`
- 后台首页：`/admin/Dashboard`
- 分类管理：`/admin/categories`
- 商品管理：`/admin/products`
- 客户列表：`/admin/customers`
- 资料维护：`/admin/profileDisplay`

## 学习重点

- `th:text`
- `th:if`
- `th:each`
- `th:href`
- `th:action`
- `th:value`
- `th:selected`
- `th:replace`

## 学习文档

- 文档总入口：[doc/README.md](./doc/README.md)
- Thymeleaf 框架系统学习指南：[doc/reference/thymeleaf-framework-guide.md](./doc/reference/thymeleaf-framework-guide.md)
- Thymeleaf 学习指南：[doc/reference/Thymeleaf学习指南.md](./doc/reference/Thymeleaf学习指南.md)
- 数据访问层与调用链：[doc/reference/数据访问层与调用链学习文档.md](./doc/reference/数据访问层与调用链学习文档.md)
- JSP/Thymeleaf 对照文档：[doc/reference/JSP页面 vs Thymeleaf页面逐页对照.md](./doc/reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)
- 改写练习题：[doc/reference/JSP改写成Thymeleaf练习题.md](./doc/reference/JSP改写成Thymeleaf练习题.md)

## 使用建议

1. 先运行页面，看模板效果
2. 再看 `src/main/resources/templates/` 下的 HTML
3. 再对照 `controller/` 看页面数据从哪来
4. 最后回看 `service/` 和 `dao/`，理解 Thymeleaf 只是视图层变化，业务链路基本不变
