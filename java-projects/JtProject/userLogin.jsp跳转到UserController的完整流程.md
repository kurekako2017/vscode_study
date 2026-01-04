# 📝 userLogin.jsp 如何跳转到 UserController 的详细解析

> **从JSP表单提交到Controller处理的完整流程**

---

## 🎯 核心答案（快速理解）

**userLogin.jsp** 通过 **HTML表单的action属性** 来指定提交到哪个Controller：

```html
<form action="userloginvalidate" method="post">
    <input name="username" />
    <input name="password" />
    <button type="submit">Login</button>
</form>
```

**当用户点击 "Login" 按钮时**：
1. 浏览器发送 `POST /userloginvalidate` 请求
2. Spring MVC 的 DispatcherServlet 接收请求
3. 查找匹配 `@RequestMapping("userloginvalidate")` 的方法
4. 找到 `UserController.userlogin()` 方法并执行

---

## 📋 完整流程图

```
┌─────────────────────────────────────────────────────────────┐
│ 步骤1：用户在登录页面输入信息                                │
│                                                             │
│ userLogin.jsp 页面:                                         │
│ ┌──────────────────────────────────┐                       │
│ │  User Login coke1                │                       │
│ │                                  │                       │
│ │  Username: [admin_________]      │                       │
│ │  Password: [●●●●●_________]      │                       │
│ │                                  │                       │
│ │  [      Login 按钮      ]        │  ← 用户点击这里        │
│ └──────────────────────────────────┘                       │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤2：HTML表单触发提交                                      │
│                                                             │
│ <form action="userloginvalidate" method="post">            │
│      ↑                            ↑                        │
│      |                            |                        │
│   表单标签                    提交方式                       │
│                                                             │
│ action="userloginvalidate" ← 关键！指定提交的URL路径        │
│ method="post"              ← 使用POST方法（而不是GET）       │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤3：浏览器发送HTTP请求                                    │
│                                                             │
│ POST http://localhost:8080/userloginvalidate HTTP/1.1      │
│ Content-Type: application/x-www-form-urlencoded            │
│ Cookie: JSESSIONID=...                                      │
│                                                             │
│ 请求体 (Body):                                              │
│ username=admin&password=123456                             │
│    ↑                    ↑                                   │
│    |                    |                                   │
│ 来自 <input name="username">                                │
│ 来自 <input name="password">                                │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤4：Tomcat服务器接收请求                                  │
│                                                             │
│ 请求信息:                                                    │
│ - URL路径: /userloginvalidate                               │
│ - HTTP方法: POST                                            │
│ - 参数: username=admin, password=123456                    │
│                                                             │
│ 将请求转发给 Spring MVC 的 DispatcherServlet               │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤5：DispatcherServlet 查找匹配的Controller               │
│                                                             │
│ DispatcherServlet (Spring MVC核心分发器)                   │
│                                                             │
│ ① 接收请求: POST /userloginvalidate                         │
│                                                             │
│ ② 查询 HandlerMapping (路由映射表)                          │
│    查找规则:                                                │
│    - 路径匹配: /userloginvalidate                           │
│    - 方法匹配: POST                                         │
│                                                             │
│ ③ 遍历所有Controller中的 @RequestMapping 注解:             │
│                                                             │
│    UserController:                                          │
│    @RequestMapping(                                         │
│        value = "userloginvalidate",  ← 路径匹配！          │
│        method = RequestMethod.POST    ← 方法匹配！         │
│    )                                                        │
│    public ModelAndView userlogin(...) {                    │
│        // 这个方法！                                        │
│    }                                                        │
│                                                             │
│ ④ 找到匹配的方法: UserController.userlogin()               │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤6：Spring MVC 准备方法参数                               │
│                                                             │
│ Controller方法签名:                                          │
│ public ModelAndView userlogin(                             │
│     @RequestParam("username") String username,  ← 参数1    │
│     @RequestParam("password") String pass,      ← 参数2    │
│     Model model,                                ← 参数3    │
│     HttpServletResponse res                     ← 参数4    │
│ )                                                           │
│                                                             │
│ Spring MVC 自动处理:                                        │
│ ① 从请求参数中提取 "username" → 赋值给 username 变量        │
│ ② 从请求参数中提取 "password" → 赋值给 pass 变量            │
│ ③ 创建 Model 对象                                           │
│ ④ 获取 HttpServletResponse 对象                            │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤7：执行 UserController.userlogin() 方法                 │
│                                                             │
│ @RequestMapping(value = "userloginvalidate",               │
│                 method = RequestMethod.POST)               │
│ public ModelAndView userlogin(                             │
│     @RequestParam("username") String username,             │
│     @RequestParam("password") String pass,                 │
│     Model model,                                            │
│     HttpServletResponse res                                 │
│ ) {                                                         │
│     // 1. 打印接收到的参数（调试用）                        │
│     System.out.println(username);  // 输出: admin          │
│     System.out.println(pass);      // 输出: 123456         │
│                                                             │
│     // 2. 调用Service层验证用户                            │
│     User u = userService.checkLogin(username, pass);       │
│                                                             │
│     // 3. 判断验证结果                                     │
│     if(username.equals(u.getUsername())) {                 │
│         // 登录成功                                        │
│         res.addCookie(new Cookie("username", username));   │
│         ModelAndView mView = new ModelAndView("index");    │
│         mView.addObject("user", u);                        │
│         // 查询商品列表                                    │
│         List<Product> products = productService            │
│                                 .getProducts();            │
│         mView.addObject("products", products);             │
│         return mView;  // 返回首页                         │
│     } else {                                                │
│         // 登录失败                                        │
│         ModelAndView mView = new ModelAndView("userLogin");│
│         mView.addObject("msg", "Please enter correct...");  │
│         return mView;  // 返回登录页，显示错误             │
│     }                                                       │
│ }                                                           │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 步骤8：返回视图                                              │
│                                                             │
│ 登录成功:                                                    │
│ → ModelAndView("index") → /views/index.jsp                 │
│ → 显示首页，包含商品列表                                     │
│                                                             │
│ 登录失败:                                                    │
│ → ModelAndView("userLogin") → /views/userLogin.jsp         │
│ → 重新显示登录页，显示错误信息 "${msg}"                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 关键代码详解

### 1. **userLogin.jsp 表单定义**

```jsp
<!-- 文件位置: src/main/webapp/views/userLogin.jsp -->

<form action="userloginvalidate" method="post">
    <!--
        action="userloginvalidate" 说明:
        - 相对路径，基于当前域名
        - 完整URL: http://localhost:8080/userloginvalidate
        - 当用户点击提交按钮时，浏览器会发送POST请求到这个路径
    -->
    
    <!-- 用户名输入框 -->
    <input type="text" 
           name="username"
           id="username"
           placeholder="Username*"
           required>
    <!--
        name="username" 很重要！
        这个name属性的值会作为参数名传递到后端
        后端通过 @RequestParam("username") 接收
    -->
    
    <!-- 密码输入框 -->
    <input type="password"
           name="password"
           id="password"
           placeholder="Password*"
           required>
    <!--
        name="password" 很重要！
        对应后端的 @RequestParam("password")
    -->
    
    <!-- 提交按钮 -->
    <input type="submit" value="Login" class="btn btn-primary btn-block">
    <!--
        type="submit" 触发表单提交
        点击后会将表单数据发送到 action 指定的URL
    -->
    
    <!-- 错误消息显示 -->
    <h3 style="color:red;">${msg}</h3>
    <!--
        ${msg} 是 EL 表达式
        显示后端通过 mView.addObject("msg", "...") 传递的错误信息
    -->
</form>
```

### 2. **UserController 方法映射**

```java
// 文件位置: src/main/java/.../controller/UserController.java

@Controller
public class UserController {

    @Autowired
    private UserService userService;
    
    @Autowired
    private ProductService productService;

    /**
     * 处理用户登录验证
     * 
     * 路由映射:
     * - URL: /userloginvalidate
     * - 方法: POST
     * 
     * 对应JSP表单: <form action="userloginvalidate" method="post">
     */
    @RequestMapping(
        value = "userloginvalidate",  // ← 匹配JSP中的action
        method = RequestMethod.POST    // ← 匹配JSP中的method
    )
    public ModelAndView userlogin(
        @RequestParam("username") String username,  // ← 接收表单的username
        @RequestParam("password") String pass,      // ← 接收表单的password
        Model model,
        HttpServletResponse res
    ) {
        // 1. 打印接收到的参数
        System.out.println("收到用户名: " + username);
        System.out.println("收到密码: " + pass);
        
        // 2. 调用Service层验证
        User u = this.userService.checkLogin(username, pass);
        
        // 3. 验证用户名是否匹配
        if(username.equals(u.getUsername())) {
            // ✅ 登录成功
            // 设置Cookie
            res.addCookie(new Cookie("username", u.getUsername()));
            
            // 创建ModelAndView，指定返回首页
            ModelAndView mView = new ModelAndView("index");
            mView.addObject("user", u);
            
            // 获取商品列表
            List<Product> products = this.productService.getProducts();
            
            if (products.isEmpty()) {
                mView.addObject("msg", "No products are available");
            } else {
                mView.addObject("products", products);
            }
            
            return mView;  // 返回首页 index.jsp
            
        } else {
            // ❌ 登录失败
            // 创建ModelAndView，重新返回登录页
            ModelAndView mView = new ModelAndView("userLogin");
            mView.addObject("msg", "Please enter correct email and password");
            
            return mView;  // 返回登录页 userLogin.jsp，并显示错误
        }
    }
}
```

---

## 🎓 参数传递原理

### **从JSP到Controller的参数映射**

```
JSP表单字段                      Controller方法参数
─────────────────────────────────────────────────────────
<input name="username">    →    @RequestParam("username") String username
<input name="password">    →    @RequestParam("password") String pass
```

**Spring MVC 自动完成的工作**：
1. 从HTTP请求中提取参数 `username=admin&password=123456`
2. 根据 `@RequestParam` 注解的值匹配参数名
3. 自动类型转换（这里都是String类型）
4. 注入到方法参数中

### **name属性必须匹配**

❌ **错误示例**（不匹配）：
```jsp
<input name="user">  <!-- JSP中是 "user" -->
```
```java
@RequestParam("username") String username  // Controller中是 "username"
```
**结果**：Spring MVC 找不到参数，会抛出异常！

✅ **正确示例**（匹配）：
```jsp
<input name="username">  <!-- JSP中是 "username" -->
```
```java
@RequestParam("username") String username  // Controller中也是 "username"
```

---

## 🔗 其他跳转方式

### 1. **注册链接跳转**

```jsp
<!-- userLogin.jsp 中的注册链接 -->
<a href="/register">Register here</a>
```

**对应的Controller方法**：
```java
@GetMapping("/register")
public String registerUser() {
    return "register";  // 跳转到 register.jsp
}
```

### 2. **直接访问URL**

用户在浏览器输入：`http://localhost:8080/`

**对应的Controller方法**：
```java
@GetMapping("/")
public String userlogin(Model model) {
    return "userLogin";  // 显示登录页
}
```

---

## 📊 完整路由映射表

| JSP页面 | 触发方式 | action/href | HTTP方法 | Controller方法 | 返回视图 |
|---------|---------|------------|----------|---------------|---------|
| userLogin.jsp | 点击Login按钮 | `userloginvalidate` | POST | `UserController.userlogin(...)` | `index.jsp` 或 `userLogin.jsp` |
| userLogin.jsp | 点击Register链接 | `/register` | GET | `UserController.registerUser()` | `register.jsp` |
| 浏览器地址栏 | 输入URL | `/` | GET | `UserController.userlogin(Model)` | `userLogin.jsp` |
| register.jsp | 提交注册表单 | `newuserregister` | POST | `UserController.newUseRegister()` | `userLogin.jsp` |

---

## ✅ 验证跳转流程的方法

### 方法1：查看浏览器开发者工具

1. 打开登录页面
2. 按 `F12` 打开开发者工具
3. 切换到 **Network** 标签
4. 输入用户名密码，点击 Login
5. 观察请求：

```
Name: userloginvalidate
Method: POST
Status: 302 (重定向) 或 200 (成功)
Form Data:
  username: admin
  password: 123456
```

### 方法2：在Controller中添加断点

```java
@RequestMapping(value = "userloginvalidate", method = RequestMethod.POST)
public ModelAndView userlogin(...) {
    System.out.println("✅ 进入了 userlogin 方法");  // ← 添加这行
    // 在这里设置断点 ←
    System.out.println("用户名: " + username);
    System.out.println("密码: " + pass);
    // ...
}
```

点击Login后，程序会暂停在断点处。

### 方法3：查看控制台日志

启动应用后，控制台会显示路由映射：

```log
Mapped "{[userloginvalidate],methods=[POST]}" onto 
public org.springframework.web.servlet.ModelAndView 
com.jtspringproject.JtSpringProject.controller.UserController.userlogin(
    java.lang.String, java.lang.String, 
    org.springframework.ui.Model, 
    javax.servlet.http.HttpServletResponse
)
```

---

## 🎯 总结

### **跳转的核心机制**：

1. **JSP表单** 通过 `action` 属性指定目标URL
2. **用户点击提交** 触发浏览器发送HTTP请求
3. **Spring MVC** 通过 `@RequestMapping` 注解匹配URL
4. **DispatcherServlet** 找到对应的Controller方法并执行
5. **Controller** 处理业务逻辑并返回视图名称
6. **ViewResolver** 解析视图并渲染JSP页面
7. **浏览器** 显示最终结果

### **关键要素**：

```
JSP:    <form action="userloginvalidate" method="post">
         <input name="username">
         
         ↓ 用户提交表单
         
HTTP:   POST /userloginvalidate
        Body: username=admin&password=123456
        
        ↓ Spring MVC 路由匹配
        
Java:   @RequestMapping(value="userloginvalidate", method=POST)
        public ModelAndView userlogin(
            @RequestParam("username") String username,
            ...
        )
```

**现在你完全理解了 userLogin.jsp 如何跳转到 UserController 了吗？** 🎉

