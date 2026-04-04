# JtProject-Thymeleaf 文档总索引

这个目录是 `JtProject-Thymeleaf` 的项目级文档入口，重点服务于：

- Thymeleaf 页面学习
- 页面到 Controller 的调用链理解
- JSP 到 Thymeleaf 的迁移对照
- 启动、排障、测试与设计资料查阅

相关入口：

- 项目根入口：[README.md](../README.md)
- Java 项目总导航：[Java项目总启动导航.md](../../Java项目总启动导航.md)
- Java 项目文档入口：[doc/README.md](../../doc/README.md)

## 建议先看

如果你是第一次看这个项目，推荐顺序：

1. [README.md](../README.md)
2. [Thymeleaf学习指南.md](./reference/Thymeleaf学习指南.md)
3. [userLogin.html跳转到UserController的完整流程.md](./reference/userLogin.html跳转到UserController的完整流程.md)
4. [数据访问层与调用链学习文档.md](./reference/数据访问层与调用链学习文档.md)
5. [JSP页面 vs Thymeleaf页面逐页对照.md](./reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)

## 目录分区

### `guides/`

适合启动、排障、测试、重构这类“怎么做”的文档。

推荐文档：

- [手动启动项目完整指南.md](./guides/手动启动项目完整指南.md)
- [手动启动项目完整指南-IDEA版.md](./guides/手动启动项目完整指南-IDEA版.md)
- [启动失败解决方案.md](./guides/启动失败解决方案.md)
- [TESTING_GUIDE.md](./guides/TESTING_GUIDE.md)
- [REFACTORING_GUIDE.md](./guides/REFACTORING_GUIDE.md)

### `reference/`

适合理解结构、页面、控制器、调用链和配置。

推荐文档：

- [Thymeleaf学习指南.md](./reference/Thymeleaf学习指南.md)
- [数据访问层与调用链学习文档.md](./reference/数据访问层与调用链学习文档.md)
- [JSP页面 vs Thymeleaf页面逐页对照.md](./reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)
- [JSP改写成Thymeleaf练习题.md](./reference/JSP改写成Thymeleaf练习题.md)
- [启动到登录页面的完整流程.md](./reference/启动到登录页面的完整流程.md)
- [userLogin.html跳转到UserController的完整流程.md](./reference/userLogin.html跳转到UserController的完整流程.md)
- [项目框架与调用流程完整总结.md](./reference/项目框架与调用流程完整总结.md)
- [项目框架与内容总结.md](./reference/项目框架与内容总结.md)
- [ENV_CONFIG.md](./reference/ENV_CONFIG.md)
- [CONTROLLER_注释说明.md](./reference/CONTROLLER_注释说明.md)

### `jp-docs/`

适合看日式项目文档、设计书、测试资料、数据库资料和运维资料。

推荐入口：

- [jp-docs/README.md](./jp-docs/README.md)
- [00_文档一覧.md](./jp-docs/00_文档一覧.md)
- [17_URL一覧.md](./jp-docs/03_database/17_URL一覧.md)
- [53_インターフェース一覧.md](./jp-docs/03_database/53_インターフェース一覧.md)
- [72_CRUD一覧.md](./jp-docs/03_database/72_CRUD一覧.md)
- [15a-01_UserController詳細設計書.md](./jp-docs/02_class-design/15a-01_UserController詳細設計書.md)

### `history/`

适合查历史启动记录、问题修复、旧笔记和归档资料。

推荐入口：

- [history/README.md](./history/README.md)
- [01_启动历史总结.md](./history/01_启动历史总结.md)
- [02_问题修复历史总结.md](./history/02_问题修复历史总结.md)
- [03_历史归档索引.md](./history/03_历史归档索引.md)

## 页面源码入口

如果你想边看文档边对照模板，常用入口如下：

- 登录页：[userLogin.html](../src/main/resources/templates/userLogin.html)
- 注册页：[register.html](../src/main/resources/templates/register.html)
- 首页：[index.html](../src/main/resources/templates/index.html)
- 商品列表：[uproduct.html](../src/main/resources/templates/uproduct.html)
- 购物车：[cart.html](../src/main/resources/templates/cart.html)
- 后台首页：[adminHome.html](../src/main/resources/templates/adminHome.html)
- 分类管理：[categories.html](../src/main/resources/templates/categories.html)
- 商品管理：[products.html](../src/main/resources/templates/products.html)

## 后端源码入口

如果你想顺着页面继续看后端，可以从这里开始：

- 用户控制器：[UserController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)
- 管理员控制器：[AdminController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)
- 商品服务：[ProductServiceImpl.java](../src/main/java/com/jtspringproject/JtSpringProject/services/impl/ProductServiceImpl.java)
- 用户服务：[UserServiceImpl.java](../src/main/java/com/jtspringproject/JtSpringProject/services/impl/UserServiceImpl.java)
- 商品 DAO：[ProductDaoImpl.java](../src/main/java/com/jtspringproject/JtSpringProject/dao/impl/ProductDaoImpl.java)
- 用户 DAO：[UserDaoImpl.java](../src/main/java/com/jtspringproject/JtSpringProject/dao/impl/UserDaoImpl.java)

## 使用建议

- 想快速跑起来：先看 [README.md](../README.md)
- 想学 Thymeleaf 基础语法：先看 [Thymeleaf学习指南.md](./reference/Thymeleaf学习指南.md)
- 想看页面如何进入 Controller：先看 [userLogin.html跳转到UserController的完整流程.md](./reference/userLogin.html跳转到UserController的完整流程.md)
- 想做 JSP 和 Thymeleaf 对照：先看 [JSP页面 vs Thymeleaf页面逐页对照.md](./reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)
