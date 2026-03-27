# JtProject-Thymeleaf 学习指南

这份文档的目标很明确：

- 让你知道 Thymeleaf 在这个项目里应该先学什么
- 让你能把页面模板和后端 `Controller -> Service -> DAO` 对上
- 让你能把 `JSP` 和 `Thymeleaf` 的写法差异看清楚

---

## 1. 这个项目里的 Thymeleaf 学习路线

建议按下面顺序学：

1. 先看 [userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html)  
   学 `th:action`、`th:href`、`th:if`
2. 再看 [uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html)  
   学 `th:each`、`th:text`
3. 再看 [cart.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/cart.html)  
   学列表渲染和条件渲染
4. 再看 [fragments/layout.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/fragments/layout.html)  
   学 `th:replace`
5. 最后看后台页面  
   [categories.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/categories.html)  
   [products.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/products.html)  
   [productsUpdate.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/productsUpdate.html)

---

## 2. 先建立一个核心概念

Thymeleaf 不是前后端分离框架。

它和 JSP 一样，都是：

- 服务端模板引擎
- 页面在服务器端渲染
- Controller 把数据放进 `Model` 或 `ModelAndView`
- 模板把这些数据拼成 HTML 返回给浏览器

所以对你来说，最重要的认知是：

`学 Thymeleaf，不是重学业务逻辑，而是学习“后端数据怎样在 HTML 模板里表达”。`

---

## 3. 和 JSP 的对照关系

| 学习点 | JSP 常见写法 | Thymeleaf 写法 |
|---|---|---|
| 输出文本 | `${user.username}` / `<%= ... %>` | `th:text="${user.username}"` |
| 链接 | `<a href="/user/products">` | `<a th:href="@{/user/products}">` |
| 表单 action | `<form action="/login">` | `<form th:action="@{/login}">` |
| 循环列表 | `c:forEach` | `th:each` |
| 条件判断 | `c:if` | `th:if` |
| 输入框回填 | `${product.name}` | `th:value="${product.name}"` |
| 公共片段 | JSP include | `th:replace` |

一句话记忆：

`JSP 更像“标签 + EL 表达式”，Thymeleaf 更像“给 HTML 标签加 th:* 属性”。`

---

## 4. 这个项目里最值得先学的 8 个 Thymeleaf 属性

## 4.1 `th:text`

作用：把后端变量输出到页面中。

示例位置：

- [index.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/index.html)
- [uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html)

例子：

```html
<h3 th:text="${product.name}">商品名称</h3>
```

意思是：

- 页面最终显示 `product.name`
- 标签里的默认文字“商品名称”只是模板占位

---

## 4.2 `th:if`

作用：条件成立时才渲染标签。

示例位置：

- [userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html)
- [cart.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/cart.html)

例子：

```html
<p th:if="${products == null or #lists.isEmpty(products)}">当前购物车为空。</p>
```

---

## 4.3 `th:each`

作用：遍历集合。

示例位置：

- [uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html)
- [categories.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/categories.html)
- [displayCustomers.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/displayCustomers.html)

例子：

```html
<tr th:each="customer : ${customers}">
```

意思是：

- 从后端传来的 `customers` 集合里
- 每次取一个元素叫 `customer`
- 用来生成一行表格

---

## 4.4 `th:href`

作用：生成链接地址。

示例位置：

- [fragments/layout.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/fragments/layout.html)

例子：

```html
<a th:href="@{/user/products}">商品列表</a>
```

---

## 4.5 `th:action`

作用：生成表单提交地址。

示例位置：

- [userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html)
- [register.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/register.html)

例子：

```html
<form th:action="@{/userloginvalidate}" method="post">
```

---

## 4.6 `th:value`

作用：把后端值回填到输入框。

示例位置：

- [productsUpdate.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/productsUpdate.html)
- [updateProfile.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/updateProfile.html)

---

## 4.7 `th:selected`

作用：下拉框回显选中项。

示例位置：

- [productsUpdate.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/productsUpdate.html)

---

## 4.8 `th:replace`

作用：复用公共片段。

示例位置：

- [fragments/layout.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/fragments/layout.html)

页面调用例子：

```html
<nav th:replace="fragments/layout :: userNav('products')"></nav>
```

这就是 Thymeleaf 版的“公共头部/导航复用”。

---

## 5. 页面和后端是怎么对上的

### 用户登录页

页面：

- [userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html)

控制器：

- [UserController.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

关键链路：

```text
userLogin.html
  -> POST /userloginvalidate
  -> UserController.userloginAlias()
  -> UserController.userlogin()
  -> UserServiceImpl.checkLogin()
  -> UserDaoImpl.getUser()
  -> 数据库
```

### 商品列表页

页面：

- [uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html)

控制器：

- [UserController.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

关键链路：

```text
GET /user/products
  -> UserController.getproduct()
  -> ProductServiceImpl.getProducts()
  -> ProductDaoImpl.getProducts()
  -> HQL: from Product
  -> 返回 List<Product>
  -> Thymeleaf 用 th:each 渲染
```

### 分类管理页

页面：

- [categories.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/categories.html)

控制器：

- [AdminController.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)

关键链路：

```text
GET /admin/categories
  -> AdminController.getcategory()
  -> CategoryServiceImpl.getCategories()
  -> CategoryDaoImpl.getCategories()
  -> EntityManager.createQuery("from Category")
  -> 返回 List<Category>
  -> Thymeleaf 用 th:each 渲染
```

---

## 6. 这个项目怎么学最有效

推荐一个非常实用的学习动作：

1. 打开一个页面
2. 先只认 `th:*` 属性
3. 去找这个页面对应的 Controller 方法
4. 看 Controller 往模型里塞了什么数据
5. 再去看 Service / DAO 数据来源

这样你会很快建立这个理解：

`Thymeleaf = 后端数据 + HTML 模板属性`

---

## 7. 当前这版最适合你练手的改造任务

1. 把 [categories.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/categories.html) 的“快速更新”改成真正的编辑表单
2. 给 [uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html) 增加商品详情页链接
3. 把 [userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html) 再拆成登录卡片和学习说明卡片两个片段
4. 给 [adminHome.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/adminHome.html) 再补一个统计模块

---

## 8. 一句话总结

如果你要快速记住这个项目里的 Thymeleaf：

`它本质上是把原来 JSP 的页面表达方式，换成了 HTML + th:* 属性，但后端 Controller、Service、DAO 的业务链路基本没变。`
