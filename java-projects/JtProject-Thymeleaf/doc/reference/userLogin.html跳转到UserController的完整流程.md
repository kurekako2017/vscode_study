# 📝 userLogin.html 跳转到 UserController 的完整流程说明

> **从 Thymeleaf 登录模板提交到 Controller 处理的完整流程**

---

## 🎯 核心答案

当前 `JtProject-Thymeleaf` 项目默认使用 **Thymeleaf** 作为视图模板引擎。

登录页面不是以“JSP 默认流程”为主，而是：

```html
<form th:action="@{/userloginvalidate}" method="post" class="stack">
    <input id="username" name="username" type="text" required>
    <input id="password" name="password" type="password" required>
    <button type="submit">登录</button>
</form>
```

当用户点击“登录”按钮时，完整链路是：

1. 浏览器先请求 `GET /`
2. `UserController.userloginPage()` 返回视图名 `userLogin`
3. Thymeleaf 解析为 `templates/userLogin.html`
4. 页面里的 `th:action="@{/userloginvalidate}"` 生成表单提交地址
5. 用户提交表单后，浏览器发送 `POST /userloginvalidate`
6. Spring MVC 命中 `UserController.userloginAlias()`
7. `userloginAlias()` 再委托给 `userlogin()` 执行登录逻辑
8. Controller 返回 `index` 或 `userLogin` 视图名
9. Thymeleaf 再渲染对应的 `.html` 模板

---

## 📌 当前项目中的关键位置

### 1. Thymeleaf 默认配置

配置文件：
[application.properties](../../src/main/resources/application.properties)

关键配置：

```properties
spring.thymeleaf.prefix=classpath:/templates/
spring.thymeleaf.suffix=.html
```

这表示当 Controller 返回：

```java
return "userLogin";
```

Spring Boot 默认会解析为：

```text
src/main/resources/templates/userLogin.html
```

而不是 JSP。

### 2. 登录模板

模板文件：
[userLogin.html](../../src/main/resources/templates/userLogin.html)

关键代码：

```html
<form th:action="@{/userloginvalidate}" method="post" class="stack">
  <div class="field">
    <label for="username">用户名</label>
    <input id="username" name="username" type="text" required>
  </div>
  <div class="field">
    <label for="password">密码</label>
    <input id="password" name="password" type="password" required>
  </div>
  <div class="actions">
    <button type="submit">登录</button>
    <a class="button secondary" th:href="@{/register}">去注册</a>
  </div>
</form>
```

这里最关键的是：

- `th:action="@{/userloginvalidate}"`：由 Thymeleaf 生成提交地址
- `name="username"`：提交给后端的参数名
- `name="password"`：提交给后端的参数名
- `th:href="@{/register}"`：注册链接也是由 Thymeleaf 动态生成

---

## 📋 完整流程图

```text
用户访问 http://localhost:8085/
        ↓
Spring MVC 接收 GET /
        ↓
UserController.userloginPage(request)
        ↓
返回 ModelAndView("userLogin")
        ↓
Thymeleaf 根据 application.properties 解析视图
        ↓
templates/userLogin.html 被渲染
        ↓
浏览器看到登录表单
        ↓
用户输入 username / password 并点击“登录”
        ↓
Thymeleaf 已将 th:action 生成成 /userloginvalidate
        ↓
浏览器发送 POST /userloginvalidate
        ↓
Spring MVC 命中 UserController.userloginAlias(...)
        ↓
userloginAlias(...) 委托给 userlogin(...)
        ↓
UserService.checkLogin(username, pass)
        ↓
登录成功：返回 ModelAndView("index")
登录失败：返回 ModelAndView("userLogin")
        ↓
Thymeleaf 渲染 index.html 或 userLogin.html
```

---

## 🔍 分步骤解析

### 步骤1：用户访问登录页

控制器代码：
[UserController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

```java
@GetMapping("/")
public ModelAndView userloginPage(HttpServletRequest request) {
    ModelAndView mView = new ModelAndView("userLogin");
    ...
    return mView;
}
```

含义：

- 浏览器访问 `GET /`
- Spring MVC 调用 `userloginPage()`
- 方法返回视图名 `"userLogin"`
- 因为项目默认使用 Thymeleaf，所以最终渲染的是 `userLogin.html`

### 步骤2：Thymeleaf 渲染模板

`userLogin.html` 不是普通静态 HTML，它会先经过 Thymeleaf 处理，例如：

```html
<head th:replace="fragments/layout :: head('用户登录')"></head>
<section th:replace="fragments/layout :: hero(...)"></section>
<div th:replace="fragments/layout :: message(${msg}, 'error')"></div>
```

这说明：

- 页面头部来自公共片段
- 顶部说明区域来自公共片段
- 如果模型中有 `msg`，错误消息区域会被渲染出来

这正是 Thymeleaf 和 JSP 说明文档最大的区别之一。

### 步骤3：表单地址由 `th:action` 生成

关键代码：

```html
<form th:action="@{/userloginvalidate}" method="post" class="stack">
```

Thymeleaf 在服务端渲染页面时，会把它处理成浏览器最终可提交的地址，例如：

```html
<form action="/userloginvalidate" method="post" class="stack">
```

也就是说：

- 模板里写的是 `th:action`
- 浏览器真正收到的是标准 HTML 的 `action`
- 用户点击提交后，浏览器照常发起 HTTP POST 请求

### 步骤4：浏览器提交登录请求

用户点击“登录”按钮后，请求类似：

```http
POST /userloginvalidate HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=lisa&password=765
```

参数来源：

- `username` 来自 `<input name="username">`
- `password` 来自 `<input name="password">`

### 步骤5：Spring MVC 命中登录入口

控制器代码：
[UserController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

```java
@RequestMapping(value = "userloginvalidate", method = RequestMethod.POST)
public ModelAndView userloginAlias(
        @RequestParam("username") String username,
        @RequestParam("password") String pass,
        Model model,
        HttpServletResponse res,
        HttpServletRequest request) {
    return userlogin(username, pass, model, res, request);
}
```

这里说明：

- `POST /userloginvalidate` 会先进入 `userloginAlias()`
- 这是当前模板表单真正命中的方法
- 它本身不做复杂业务，只负责转调真实登录逻辑

### 步骤6：委托到真实登录逻辑

控制器代码：
[UserController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

```java
@RequestMapping(value = "userloginvalidate1", method = RequestMethod.POST)
public ModelAndView userlogin(
        @RequestParam("username") String username,
        @RequestParam("password") String pass,
        Model model,
        HttpServletResponse res,
        HttpServletRequest request) {
    User u = this.userService.checkLogin(username, pass);
    ...
}
```

业务链路：

```text
UserController
    ↓
UserService.checkLogin(...)
    ↓
UserDao / 数据库查询
    ↓
返回 User 对象
```

### 步骤7：登录成功或失败

成功时：

```java
ModelAndView mView  = new ModelAndView("index");
mView.addObject("user", u);
mView.addObject("products", products);
return mView;
```

失败时：

```java
ModelAndView mView = new ModelAndView("userLogin");
mView.addObject("msg", "Please enter correct email and password");
return mView;
```

含义：

- 登录成功：返回 `index`，Thymeleaf 渲染 `index.html`
- 登录失败：返回 `userLogin`，Thymeleaf 重新渲染 `userLogin.html`
- 同时 `msg` 会回传到页面，用于显示错误提示

### 步骤8：Thymeleaf 渲染结果页面

因为项目默认是：

```properties
spring.thymeleaf.prefix=classpath:/templates/
spring.thymeleaf.suffix=.html
```

所以最终视图解析是：

| Controller 返回值 | 默认解析结果 |
|---|---|
| `"userLogin"` | `templates/userLogin.html` |
| `"index"` | `templates/index.html` |
| `"register"` | `templates/register.html` |

---

## 🎓 参数传递对应关系

```text
Thymeleaf 表单字段                  Controller 方法参数
---------------------------------------------------------------
name="username"              ->   @RequestParam("username") String username
name="password"              ->   @RequestParam("password") String pass
```

只要前端 `name` 和后端 `@RequestParam` 对应上，Spring MVC 就能自动绑定参数。

---

## ✅ 这个流程和旧 JSP 文档的区别

旧写法关注的是：

- `userLogin.jsp`
- JSP EL 表达式
- `/views/*.jsp`

当前默认流程更应该关注的是：

- `userLogin.html`
- `th:action`、`th:href`、`th:replace`
- `classpath:/templates/*.html`

也就是说：

**Controller、Service、DAO 的调用链本质没变，变化的是“视图层从 JSP 说明切换为 Thymeleaf 说明”。**

---

## 🧭 一句话总结

在当前 `JtProject-Thymeleaf` 默认配置下，登录流程应理解为：

```text
GET / -> UserController.userloginPage() -> userLogin.html
用户提交表单
-> POST /userloginvalidate
-> UserController.userloginAlias()
-> UserController.userlogin()
-> UserService / DAO
-> 返回 index.html 或 userLogin.html
```

如果以后切到某些保留的 JSP profile，视图解析方式可能会改回 `/views/*.jsp`；但就当前默认运行方式而言，这份文档应该以 **Thymeleaf 版本流程** 为准。
