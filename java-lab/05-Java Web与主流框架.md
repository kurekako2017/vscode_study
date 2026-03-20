# Java Web 与主流框架

## 1. 先理解 Java Web 的本质

浏览器发送 HTTP 请求，服务端接收请求并返回 HTML、JSON 或其他数据。

Java Web 开发核心就是处理:

- 请求
- 参数
- 业务逻辑
- 数据库访问
- 响应页面或接口结果

## 2. 传统 Java Web 技术

### Servlet

- 接收请求
- 处理参数
- 调用业务逻辑
- 返回响应

### JSP

- 用于服务端渲染页面
- 老项目中仍很常见

### Filter

- 用于登录校验、编码设置、日志记录

### Listener

- 用于监听应用生命周期、Session 变化等

## 3. MVC 模式

典型分层:

- Controller: 接收请求
- Service: 业务逻辑
- DAO/Repository: 数据访问
- Entity/Model: 数据对象
- View: JSP、Thymeleaf、HTML

典型调用链:

```text
userlogin.jsp
  -> UserController
  -> UserService
  -> UserDao
  -> Database
```

## 4. 传统框架

### Struts

对日维护项目中常见。

需要了解:

- Action
- Form
- 配置文件
- 页面跳转

### Spring

核心点:

- IoC
- DI
- AOP
- 事务

### Hibernate

核心点:

- 实体映射
- Session
- HQL
- 延迟加载

## 5. 现代主流: Spring Boot

Spring Boot 是当前学习重点，但不能替代你对传统项目的理解。

### 常见目录结构

```text
src/
`-- main/
    |-- java/
    |   `-- com/example/demo/
    |       |-- DemoApplication.java
    |       |-- controller/
    |       |-- service/
    |       |-- repository/
    |       `-- entity/
    `-- resources/
        |-- application.properties
        |-- static/
        `-- templates/
```

### 关键文件说明

- `DemoApplication.java`: 启动类
- `controller`: 控制层
- `service`: 业务层
- `repository` 或 `dao`: 数据访问层
- `entity` 或 `model`: 实体类
- `application.properties`: 配置文件
- `templates`: 模板页面
- `static`: 静态资源

## 6. 对日项目里的学习建议

- 先学会 Servlet/JSP 和 MVC，再学 Spring Boot
- 看到 `userlogin.jsp`、`Action`、`DAO`、`struts-config.xml` 不要陌生
- 学现代框架时，也要知道老项目是如何组织代码的
- 会写 CRUD 只是开始，真正重点是按设计书实现和维护既有逻辑
