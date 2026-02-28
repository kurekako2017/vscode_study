<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%-- 使用 EL 表达式 (${msg}) 显示来自 Controller 的错误消息， 不需要 <jsp:useBean> 声明 --%>

<%--
    用户登录页面
    功能：提供用户登录表单，验证用户名和密码
    提交到：/userloginvalidate 接口
--%>
<!doctype html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <!-- 响应式视口设置 -->
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <!-- 引入 Bootstrap 4.4.1 CSS框架 -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
          integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

    <!-- 引入 FontAwesome 图标库 -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css"
          integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">

    <title>用户登录 - JT电商系统</title>
</head>
<body>


<!-- 主容器：包含登录表单 -->
<div class="container my-3">
    
            <div class="col-sm-6">
                <!-- 登录标题 -->
                <h2>User Login</h2>

                <!--
                    用户登录表单

                    📝 表单提交流程：
                    1. 用户填写用户名和密码
                    2. 点击 Login 按钮（type="submit"）
                    3. 浏览器发送 POST 请求到 action 指定的 URL
                    4. 请求路径: POST /userloginvalidate
                    5. 请求参数: username=xxx&password=xxx
                    6. Spring MVC 的 DispatcherServlet 接收请求
                    7. 根据 @RequestMapping 路由到 UserController.userlogin() 方法
                    8. 执行登录验证逻辑
                    9. 返回结果页面（成功→index.jsp，失败→userLogin.jsp）

                    - action: userloginvalidate - 表单提交的后端接口（必须与Controller中的路由匹配）
                    - method: post - 使用POST方法提交（安全性考虑，密码不会显示在URL中）
                -->
                <form action="/userloginvalidate" method="post">

                    <!--
                        用户名输入框

                        📝 重要属性说明：
                        - name="username" : 最关键的属性！提交表单时的参数名
                          → 后端通过 @RequestParam("username") 接收此参数
                          → 参数名必须与Controller中的注解值完全一致

                        - id="username" : 用于JavaScript操作和label的for属性关联

                        - required : HTML5验证，确保用户必须填写此字段

                        - placeholder : 输入框的提示文字

                        - class="form-control..." : Bootstrap样式类
                    -->
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text"
                               name="username"
                               id="username"
                               placeholder="Username*"
                               required
                               class="form-control form-control-lg">
                    </div>

                    <!--
                        密码输入框

                        📝 重要属性说明：
                        - type="password" : 密码类型，输入内容会显示为 ●●● （安全性）

                        - name="password" : 提交表单时的参数名
                          → 后端通过 @RequestParam("password") 接收此参数
                          → 与Controller的参数名对应

                        - required : 必填字段验证
                    -->
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password"
                               class="form-control form-control-lg"
                               placeholder="Password*"
                               required
                               name="password"
                               id="password">
                    </div>

                    <!--
                        注册链接提示

                        📝 跳转流程：
                        1. 用户点击 "Register here" 链接
                        2. 浏览器发送 GET /register 请求
                        3. 路由到 UserController.registerUser() 方法
                        4. 返回 register.jsp 注册页面
                    -->
                    <span>Don't have an account <a class="linkControl" href="/register">Register here</a></span> <br><br>

                    <!--
                        登录提交按钮

                        📝 提交流程：
                        - type="submit" : 提交按钮，点击后触发表单提交
                        - 浏览器收集表单数据：username=xxx&password=xxx
                        - 发送POST请求到 action 指定的URL（userloginvalidate）
                        - 等待服务器响应
                    -->
                    <input type="submit" value="Login" class="btn btn-primary btn-block">

                    <!--
                        错误消息显示区域

                        📝 EL表达式说明：
                        - ${msg} : Expression Language（表达式语言）
                        - 从后端 ModelAndView 中获取 "msg" 属性的值
                        - 如果登录失败，Controller会设置：
                          mView.addObject("msg", "Please enter correct email and password");
                        - 该消息会在这里显示为红色文字
                    -->
                    <br><h3 style="color:red;">${msg}</h3>
                    <br>
                </form>
            </div>

</div>

<!-- JavaScript 库引用 -->
<!-- jQuery 3.4.1 - JavaScript库，用于DOM操作 -->
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>

<!-- Popper.js - Bootstrap的工具提示和弹出框依赖 -->
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>

<!-- Bootstrap 4.4.1 JavaScript - 提供交互组件功能 -->
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>
</html>