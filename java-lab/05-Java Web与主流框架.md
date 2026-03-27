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

## 7. 结合 jtproject 理解四个开发框架

`java-projects/JtProject` 不是单一框架项目，而是多个框架一起协作的典型 Java Web 项目。

可以把它理解成:

- `Spring Boot`: 负责启动、自动配置、整合容器
- `Spring MVC`: 负责接收请求、路由分发、调用业务层
- `Hibernate / JPA`: 负责对象和数据库表之间的映射与持久化
- `JSP`: 负责页面展示

### 7.1 jtproject 的整体架构

```text
浏览器
  -> Spring Boot 内嵌 Tomcat
  -> Spring MVC Controller
  -> Service
  -> DAO
  -> Hibernate / JPA
  -> MySQL / H2
  -> 返回 JSP 页面
```

对应到项目里大致是:

- `controller`: 接收 URL 请求
- `services`: 写业务逻辑
- `dao`: 写数据库访问
- `models`: 实体类
- `webapp/views`: JSP 页面

### 7.2 框架1: Spring Boot

#### 概念

Spring Boot 不是用来写页面的，也不是专门操作数据库的。
它更像是整个项目的“启动器”和“整合器”。

#### 在 jtproject 中负责什么

- 启动应用
- 创建 Spring 容器
- 扫描 `@Controller`、`@Service`、`@Repository`
- 启动内嵌 Tomcat
- 读取 `application.properties`
- 整合 Spring MVC、数据源、事务等功能

#### 你可以这样理解

- 没有 Spring Boot，你需要自己配很多 XML 或 Java 配置
- 有了 Spring Boot，项目能更快启动，依赖整合也更方便

#### 在项目中的典型体现

- 启动类 `JtSpringProjectApplication`
- 配置文件 `application.properties`
- `pom.xml` 里的 `spring-boot-starter-web`

### 7.3 框架2: Spring MVC

#### 概念

Spring MVC 是 Web 层框架，核心职责是“接请求，再把请求交给正确的方法处理”。

#### 在 jtproject 中负责什么

- 定义 URL 和方法的对应关系
- 接收表单参数
- 调用 Service 层
- 把结果放到 `Model` 或 `ModelAndView`
- 决定返回哪个 JSP 页面

#### 典型调用方式

```text
用户访问 /user/products
  -> UserController
  -> ProductService
  -> ProductDao
  -> 查询数据库
  -> 返回 uproduct.jsp
```

#### 相关核心概念

- `@Controller`
- `@GetMapping`
- `@PostMapping`
- `@RequestParam`
- `Model`
- `ModelAndView`
- 视图解析器

#### 在项目中的典型体现

- `UserController`
- `AdminController`
- `WebMvcConfig`

### 7.4 框架3: Hibernate / JPA

#### 概念

Hibernate 是 ORM 框架，JPA 是一套持久化规范。
很多时候学习时会把它们放在一起理解。

简单说:

- JPA 定义“应该怎么做”
- Hibernate 负责“具体怎么实现”

#### 在 jtproject 中负责什么

- 把 Java 对象映射成数据库表
- 把查询结果映射成实体对象
- 执行增删改查
- 配合事务完成数据持久化

#### 在项目中的数据流

```text
Controller
  -> Service
  -> DaoImpl
  -> SessionFactory / EntityManager
  -> Hibernate
  -> MySQL
```

#### 相关核心概念

- `@Entity`
- `@Table`
- `@Id`
- `SessionFactory`
- `EntityManager`
- HQL
- `@Transactional`

#### 在 jtproject 中的特点

- 既有 JPA 风格注解实体
- 也有直接使用 Hibernate `SessionFactory` 的 DAO
- 属于“Spring 管理事务 + Hibernate 负责 ORM”的组合

### 7.5 框架4: JSP

#### 概念

JSP 是服务端页面模板技术。
它会在服务器端把数据和页面拼好，再返回给浏览器。

#### 在 jtproject 中负责什么

- 展示登录页、商品页、购物车页、后台页面
- 接收 Controller 放进来的数据
- 用标签和表达式渲染页面内容

#### 你可以这样理解

- JSP 主要负责“显示”
- 它不应该承担复杂业务逻辑
- 真正的业务应放在 Controller / Service / DAO 中

#### 在项目中的典型体现

- `userLogin.jsp`
- `index.jsp`
- `uproduct.jsp`
- `cart.jsp`
- `adminHome.jsp`

## 8. 这四个框架的区别

### 8.1 按职责区分

| 框架 | 主要职责 | 所在层 |
|---|---|---|
| Spring Boot | 启动项目、整合配置、管理容器 | 整体基础设施层 |
| Spring MVC | 处理请求和页面跳转 | Web/Controller层 |
| Hibernate / JPA | 操作数据库、对象映射 | DAO/持久层 |
| JSP | 渲染页面 | View层 |

### 8.2 按“你写代码时在做什么”区分

- 如果你在写启动类、配置端口、整合依赖，基本是在用 Spring Boot
- 如果你在写 `@GetMapping("/login")`，基本是在用 Spring MVC
- 如果你在写实体类、HQL、数据库保存查询，基本是在用 Hibernate / JPA
- 如果你在写 `.jsp` 页面展示商品列表，基本是在用 JSP

### 8.3 它们不是互相替代，而是互相配合

很多初学者容易误以为:

- Spring Boot 可以替代 Spring MVC
- Spring MVC 可以替代 Hibernate
- JSP 和 Spring Boot 是同一层的东西

其实不是。

正确理解是:

- Spring Boot 管“项目怎么跑起来”
- Spring MVC 管“请求怎么进来、怎么出去”
- Hibernate / JPA 管“数据怎么落库、怎么查询”
- JSP 管“页面怎么显示”

## 9. 学 jtproject 时建议重点观察什么

- 看启动类，理解 Spring Boot 如何启动整个应用
- 看 `Controller -> Service -> DAO -> Model -> JSP` 这条链路
- 看 `@Controller`、`@Service`、`@Repository` 的分层含义
- 看实体类和数据库表怎么对应
- 看一个请求最终是怎么跳到某个 JSP 页面的
- 看事务和数据库操作为什么通常写在 DAO 或 Service 中

## 10. 一句话总结

在 `jtproject` 里，最适合初学者掌握的四个框架关系是:

- Spring Boot 负责“搭台子”
- Spring MVC 负责“接请求”
- Hibernate / JPA 负责“管数据”
- JSP 负责“出页面”

## 11. jtproject 的另外三个框架版本

除了原始 `JtProject` 之外，这个工作区里还有三个很重要的学习版本:

- `JtProject-Thymeleaf`
- `JtProject-React`
- `JtProject-Vue`

它们的核心意义不是“业务逻辑完全重写”，而是让你对照学习:

- 同一个电商项目
- 后端仍然大体是 Spring Boot
- 只是视图层或前端架构发生变化

### 11.1 JtProject-Thymeleaf

#### 它是什么

这是把原始 JSP 页面改成 Thymeleaf 模板的版本。

#### 架构特点

```text
浏览器
  -> Spring Boot
  -> Spring MVC Controller
  -> Service
  -> DAO
  -> Hibernate / JPA
  -> 数据库
  -> Thymeleaf 模板 HTML
```

#### 重点概念

Thymeleaf 和 JSP 一样，都是服务端模板技术。

也就是说:

- 页面仍然由后端返回
- Controller 仍然直接返回视图名
- 后端把数据放进 `Model`
- 模板负责把数据渲染成 HTML

#### 在这个项目里主要学什么

- `th:text`
- `th:if`
- `th:each`
- `th:href`
- `th:action`
- `th:value`
- `th:replace`

#### 和 JSP 的主要区别

- JSP 习惯用 EL、JSTL、JSP 标签
- Thymeleaf 习惯在 HTML 标签上写 `th:*` 属性
- JSP 更像“页面脚本模板”
- Thymeleaf 更像“增强版 HTML 模板”

#### 适合理解成什么

如果说 JSP 是老式服务端页面方案，那么 Thymeleaf 就是更现代、更接近 HTML 语义的服务端模板方案。

### 11.2 JtProject-React

#### 它是什么

这是把前端改成 `React + TypeScript + Vite` 的版本。

#### 架构特点

```text
浏览器
  -> React 页面
  -> 调用 Spring Boot /api 接口
  -> Controller
  -> Service
  -> DAO
  -> Hibernate / JPA
  -> 数据库
  -> 返回 JSON
```

#### 重点概念

React 不是服务端模板，而是前端组件框架。

也就是说:

- 页面主要在浏览器里渲染
- 后端不再主要返回 JSP 页面
- 后端更多是提供 JSON 接口
- 前端自己控制路由、状态和组件渲染

#### 在这个项目里主要学什么

- Component
- JSX
- `useState`
- `useEffect`
- `props`
- `react-router-dom`
- 前后端分离

#### 和 JSP / Thymeleaf 的主要区别

- JSP / Thymeleaf 是服务端渲染页面
- React 是浏览器端渲染页面
- JSP / Thymeleaf 通常由 Controller 直接返回视图
- React 通常由后端提供 `/api/...`，前端自己拿数据再渲染

#### 适合理解成什么

React 更适合复杂交互页面、组件化开发和前后端分离项目。

### 11.3 JtProject-Vue

#### 它是什么

这是把前端改成 `Vue 3 + TypeScript + Vite` 的版本。

#### 架构特点

```text
浏览器
  -> Vue 页面
  -> 调用 Spring Boot /api 接口
  -> Controller
  -> Service
  -> DAO
  -> Hibernate / JPA
  -> 数据库
  -> 返回 JSON
```

#### 重点概念

Vue 也是前端框架，但它的模板表达通常比 React 更直观。

在这个项目里，核心理解是:

- Vue 在前端负责页面和交互
- Spring Boot 在后端负责接口和业务
- 页面渲染主要发生在浏览器端

#### 在这个项目里主要学什么

- `ref`
- `reactive`
- `v-if`
- `v-for`
- `v-model`
- `@click`
- `onMounted`
- `vue-router`

#### 和 React 的主要区别

- React 更偏 JSX 和函数式组件思维
- Vue 更偏模板语法和响应式绑定思维
- React 常见关键词是 `state`、`props`、hooks
- Vue 常见关键词是 `ref`、`reactive`、指令、Composition API

#### 适合理解成什么

Vue 对初学者通常更容易先看懂模板层，适合把“页面结构和数据绑定”先建立直觉。

## 12. 原始版和三个变体版怎么区分

### 12.1 从“页面是谁渲染的”来区分

| 项目 | 页面主要由谁渲染 | 典型技术 |
|---|---|---|
| JtProject | 服务端 | JSP |
| JtProject-Thymeleaf | 服务端 | Thymeleaf |
| JtProject-React | 浏览器前端 | React |
| JtProject-Vue | 浏览器前端 | Vue |

### 12.2 从“后端返回什么”来区分

| 项目 | 后端更常返回什么 |
|---|---|
| JtProject | JSP 视图 |
| JtProject-Thymeleaf | Thymeleaf 模板视图 |
| JtProject-React | JSON 接口数据 |
| JtProject-Vue | JSON 接口数据 |

### 12.3 从学习目标来区分

- 学 `JtProject`：重点看传统 MVC + JSP
- 学 `JtProject-Thymeleaf`：重点看服务端模板从 JSP 升级到 Thymeleaf
- 学 `JtProject-React`：重点看前后端分离、组件化、状态管理
- 学 `JtProject-Vue`：重点看响应式模板、指令、Vue 组件化

## 13. 这几个框架版本的关系

不要把这几个版本理解成互相冲突。

更准确地说:

- `JtProject` 是基础版
- `JtProject-Thymeleaf` 是服务端模板升级版
- `JtProject-React` 是前后端分离的 React 版
- `JtProject-Vue` 是前后端分离的 Vue 版

它们最适合拿来做“同一个业务，不同技术架构”的对照学习。

## 14. 最后再压缩记忆一次

如果你要把 `jtproject` 相关框架一次记住，可以这样背:

- `JtProject`：Spring Boot + Spring MVC + Hibernate/JPA + JSP
- `JtProject-Thymeleaf`：Spring Boot + Spring MVC + Hibernate/JPA + Thymeleaf
- `JtProject-React`：Spring Boot 后端 + React 前端
- `JtProject-Vue`：Spring Boot 后端 + Vue 前端

## 15. 如果你的重点是比较学习这四个框架

你现在最适合重点比较的是这四个:

- `JSP`
- `Thymeleaf`
- `React`
- `Vue`

这里要先建立一个很重要的认知:

- `JSP` 和 `Thymeleaf` 属于服务端页面模板技术
- `React` 和 `Vue` 属于前端框架

也就是说，它们虽然都和“页面显示”有关，但分属两种不同思路。

### 15.1 四个框架的本质区别

| 框架 | 类型 | 页面主要在哪里渲染 | 后端通常返回什么 |
|---|---|---|---|
| JSP | 服务端模板 | 服务器端 | HTML/JSP视图 |
| Thymeleaf | 服务端模板 | 服务器端 | HTML/模板视图 |
| React | 前端框架 | 浏览器端 | JSON接口 |
| Vue | 前端框架 | 浏览器端 | JSON接口 |

### 15.2 用最直白的话理解

- `JSP`：后端把页面拼好再发给浏览器
- `Thymeleaf`：后端把页面拼好再发给浏览器，但写法比 JSP 更现代
- `React`：后端只给数据，页面主要由前端自己拼出来
- `Vue`：后端只给数据，页面主要由前端自己拼出来，但模板语法通常更直观

### 15.3 在 jtproject 里怎么对照学习

| 项目 | 你主要在学什么 |
|---|---|
| `JtProject` | JSP 页面结构、传统 MVC 页面返回方式 |
| `JtProject-Thymeleaf` | 从 JSP 迁移到 Thymeleaf 的模板思路 |
| `JtProject-React` | React 组件、状态、前后端分离 |
| `JtProject-Vue` | Vue 模板、响应式、前后端分离 |

### 15.4 四个框架分别该抓什么概念

#### JSP

重点学:

- JSP 页面怎么接收后端数据
- EL 表达式
- JSTL 标签
- 页面跳转和表单提交

一句话理解:

`JSP = 传统 Java Web 页面技术`

#### Thymeleaf

重点学:

- `th:text`
- `th:if`
- `th:each`
- `th:href`
- `th:action`
- 模板继承和片段复用

一句话理解:

`Thymeleaf = 更现代、更像 HTML 的服务端模板`

#### React

重点学:

- 组件
- JSX
- `props`
- `state`
- `useState`
- `useEffect`
- 路由
- 调接口

一句话理解:

`React = 组件驱动的前端框架`

#### Vue

重点学:

- 模板语法
- `ref`
- `reactive`
- `v-if`
- `v-for`
- `v-model`
- `@click`
- 组件通信

一句话理解:

`Vue = 响应式模板驱动的前端框架`

### 15.5 四个框架之间怎么记区别

#### JSP vs Thymeleaf

- 都是服务端渲染
- 都是 Controller 把数据给页面
- 差别主要在模板写法
- JSP 更老，Thymeleaf 更现代

#### React vs Vue

- 都是前端框架
- 都常用于前后端分离
- React 更偏 JSX 和函数式思维
- Vue 更偏模板和响应式思维

#### JSP/Thymeleaf vs React/Vue

- 前两者是后端主导页面输出
- 后两者是前端主导页面输出
- 前两者一般返回视图
- 后两者一般请求接口拿 JSON

### 15.6 你的学习顺序建议

如果你是“比较学习”这四个框架，最顺的顺序通常是:

1. 先看 `JSP`
2. 再看 `Thymeleaf`
3. 再看 `React`
4. 最后看 `Vue`

原因很简单:

- 先理解服务端渲染页面
- 再理解更现代的服务端模板
- 然后再进入前后端分离
- 最后对比两种主流前端框架

### 15.7 最适合你的压缩版记忆

- `JSP`：老式服务端页面模板
- `Thymeleaf`：现代服务端页面模板
- `React`：组件化前端框架
- `Vue`：响应式前端框架
