# JSP 页面 vs Thymeleaf 页面逐页对照

这份文档专门用于做一件事：

把原始 `JtProject` 里的 JSP 页面，和 `JtProject-Thymeleaf` 里的 Thymeleaf 页面一页一页配起来看。

这样你可以清楚理解：

- 同一类页面，在 JSP 里怎么写
- 换成 Thymeleaf 之后怎么写
- 哪些变化只是“模板语法变化”
- 哪些变化是“页面结构和复用方式变化”

---

## 1. 先记住一个总原则

在这两个项目里，业务链路基本没变：

```text
Browser
  -> Controller
  -> Service
  -> DAO
  -> Database
  -> Controller 把数据放到 Model / ModelAndView
  -> JSP 或 Thymeleaf 模板渲染
  -> HTML Response
```

所以你对照学习时最重要的认知是：

`JSP 和 Thymeleaf 的核心区别主要在“页面模板表达方式”，不是后端业务逻辑。`

---

## 2. 页面对应关系总表

| 功能 | JSP 页面 | Thymeleaf 页面 | 学习重点 |
|---|---|---|---|
| 用户登录 | [userLogin.jsp](../../../JtProject/src/main/webapp/views/userLogin.jsp) | [userLogin.html](../../src/main/resources/templates/userLogin.html) | 表单提交、消息显示、链接 |
| 用户注册 | [register.jsp](../../../JtProject/src/main/webapp/views/register.jsp) | [register.html](../../src/main/resources/templates/register.html) | 表单字段、提交流程 |
| 首页 | [index.jsp](../../../JtProject/src/main/webapp/views/index.jsp) | [index.html](../../src/main/resources/templates/index.html) | 模型数据显示 |
| 商品列表 | [uproduct.jsp](../../../JtProject/src/main/webapp/views/uproduct.jsp) | [uproduct.html](../../src/main/resources/templates/uproduct.html) | 列表循环、按钮操作 |
| 购物车 | [cart.jsp](../../../JtProject/src/main/webapp/views/cart.jsp) | [cart.html](../../src/main/resources/templates/cart.html) | 表格渲染、条件提示 |
| 管理员登录 | [adminlogin.jsp](../../../JtProject/src/main/webapp/views/adminlogin.jsp) | [adminlogin.html](../../src/main/resources/templates/adminlogin.html) | 后台登录表单 |
| 后台首页 | [adminHome.jsp](../../../JtProject/src/main/webapp/views/adminHome.jsp) | [adminHome.html](../../src/main/resources/templates/adminHome.html) | 导航和后台入口 |
| 分类管理 | [categories.jsp](../../../JtProject/src/main/webapp/views/categories.jsp) | [categories.html](../../src/main/resources/templates/categories.html) | CRUD 页面表达 |
| 商品管理 | [products.jsp](../../../JtProject/src/main/webapp/views/products.jsp) | [products.html](../../src/main/resources/templates/products.html) | 表格、操作链接 |
| 商品新增 | [productsAdd.jsp](../../../JtProject/src/main/webapp/views/productsAdd.jsp) | [productsAdd.html](../../src/main/resources/templates/productsAdd.html) | 表单、下拉框 |
| 商品编辑 | [productsUpdate.jsp](../../../JtProject/src/main/webapp/views/productsUpdate.jsp) | [productsUpdate.html](../../src/main/resources/templates/productsUpdate.html) | 回填值、选中状态 |
| 客户列表 | [displayCustomers.jsp](../../../JtProject/src/main/webapp/views/displayCustomers.jsp) | [displayCustomers.html](../../src/main/resources/templates/displayCustomers.html) | 表格循环 |
| 资料维护 | [updateProfile.jsp](../../../JtProject/src/main/webapp/views/updateProfile.jsp) | [updateProfile.html](../../src/main/resources/templates/updateProfile.html) | 表单回填 |

---

## 3. 第一组：登录页对照

### JSP

- [userLogin.jsp](../../../JtProject/src/main/webapp/views/userLogin.jsp)

### Thymeleaf

- [userLogin.html](../../src/main/resources/templates/userLogin.html)

### 共同点

- 都是提交到 `/userloginvalidate`
- 都依赖 `UserController.userloginAlias()` / `userlogin()`
- 都显示登录失败消息

对应控制器：

- [UserController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)

### 主要差别

| 点 | JSP 写法 | Thymeleaf 写法 |
|---|---|---|
| 表单 action | `action="/userloginvalidate"` | `th:action="@{/userloginvalidate}"` |
| 注册链接 | `href="/register"` | `th:href="@{/register}"` |
| 错误消息 | `${msg}` | 通过片段 + `th:if` / `th:text` 渲染 |
| 页面结构 | 单页直接写完 | 拆出公共片段 `layout.html` |

### 学习建议

登录页最适合先学这三个点：

1. `th:action`
2. `th:href`
3. `th:replace`

---

## 4. 第二组：商品列表页对照

### JSP

- [uproduct.jsp](../../../JtProject/src/main/webapp/views/uproduct.jsp)

### Thymeleaf

- [uproduct.html](../../src/main/resources/templates/uproduct.html)

### 共同点

- 都来自 `GET /user/products`
- 都依赖 `productService.getProducts()`
- 页面上都遍历商品列表

对应后端：

- [UserController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)
- [ProductServiceImpl.java](../../src/main/java/com/jtspringproject/JtSpringProject/services/impl/ProductServiceImpl.java)
- [ProductDaoImpl.java](../../src/main/java/com/jtspringproject/JtSpringProject/dao/impl/ProductDaoImpl.java)

### 主要差别

| 点 | JSP 写法 | Thymeleaf 写法 |
|---|---|---|
| 列表循环 | `c:forEach` | `th:each` |
| 文本输出 | `${product.name}` | `th:text="${product.name}"` |
| 表单 hidden 值 | `value="${product.id}"` | `th:value="${product.id}"` |
| 页面组织 | Bootstrap 表格为主 | 卡片式布局，更便于学习 |

### 代表性语法对照

JSP:

```jsp
<c:forEach var="product" items="${products}">
  <td>${product.name}</td>
</c:forEach>
```

Thymeleaf:

```html
<article th:each="product : ${products}">
  <h3 th:text="${product.name}">商品名称</h3>
</article>
```

### 学习建议

商品列表页最适合学习：

1. `c:forEach -> th:each`
2. `${...} -> th:text`
3. 表单参数绑定

---

## 5. 第三组：购物车页对照

### JSP

- [cart.jsp](../../../JtProject/src/main/webapp/views/cart.jsp)

### Thymeleaf

- [cart.html](../../src/main/resources/templates/cart.html)

### 共同点

- 都依赖 `UserController.showCart()`
- 都显示 `products` 列表
- 都支持删除购物车商品

### 主要差别

| 点 | JSP 写法 | Thymeleaf 写法 |
|---|---|---|
| 条件消息 | `c:if` | `th:if` |
| 删除按钮 | 表单提交 | 链接生成 `th:href` |
| 空列表提示 | JSTL 条件判断 | `#lists.isEmpty(...)` |

### 学习建议

购物车页最适合练：

1. `c:if -> th:if`
2. 表格中的 `th:each`
3. `th:href` 带参数

---

## 6. 第四组：管理员首页对照

### JSP

- [adminHome.jsp](../../../JtProject/src/main/webapp/views/adminHome.jsp)

### Thymeleaf

- [adminHome.html](../../src/main/resources/templates/adminHome.html)

### 共同点

- 都是管理员登录后的入口页
- 都提供分类、商品、客户等后台入口

### 主要差别

| 点 | JSP 写法 | Thymeleaf 写法 |
|---|---|---|
| 导航 | 当前页自己写 navbar | 通过 `layout.html` 的 `adminNav` 片段复用 |
| 页面结构 | Bootstrap 卡片 | 更轻量的学习型卡片布局 |
| 链接 | 普通 `href` | `th:href` |

### 学习建议

后台首页最适合学习：

1. 公共导航片段复用
2. `th:replace`
3. 页面骨架抽取

---

## 7. 第五组：分类管理页对照

### JSP

- [categories.jsp](../../../JtProject/src/main/webapp/views/categories.jsp)

### Thymeleaf

- [categories.html](../../src/main/resources/templates/categories.html)

### 共同点

- 都依赖 `AdminController.getcategory()`
- 都显示分类列表
- 都支持新增和删除

对应控制器：

- [AdminController.java](../../src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)

### 主要差别

| 点 | JSP 写法 | Thymeleaf 写法 |
|---|---|---|
| 新增分类 | Bootstrap Modal + 表单 | 直接内联表单 |
| 循环 | `c:forEach` | `th:each` |
| 删除链接 | 表单 GET 提交 | `th:href` 生成带参数链接 |
| 更新方式 | JS 给 modal 回填 | 当前做成简化版快速更新链接 |

### 学习建议

这一页最适合你观察：

1. Thymeleaf 更适合“HTML 属性驱动”的表达
2. JSP 页面里常会掺杂更多前端脚本和弹窗结构
3. Thymeleaf 学习初期先做简单表单，理解更快

---

## 8. 你最该优先看的页面顺序

如果只想用最短时间看出区别，按这个顺序：

1. 登录页  
   [userLogin.jsp](../../../JtProject/src/main/webapp/views/userLogin.jsp)  
   [userLogin.html](../../src/main/resources/templates/userLogin.html)

2. 商品列表页  
   [uproduct.jsp](../../../JtProject/src/main/webapp/views/uproduct.jsp)  
   [uproduct.html](../../src/main/resources/templates/uproduct.html)

3. 购物车页  
   [cart.jsp](../../../JtProject/src/main/webapp/views/cart.jsp)  
   [cart.html](../../src/main/resources/templates/cart.html)

4. 分类管理页  
   [categories.jsp](../../../JtProject/src/main/webapp/views/categories.jsp)  
   [categories.html](../../src/main/resources/templates/categories.html)

5. 后台首页  
   [adminHome.jsp](../../../JtProject/src/main/webapp/views/adminHome.jsp)  
   [adminHome.html](../../src/main/resources/templates/adminHome.html)

---

## 9. 一句话总结

如果你要快速记住 JSP 和 Thymeleaf 的差别，可以直接记这句话：

`JSP 更像“标签库 + EL 表达式”，Thymeleaf 更像“原生 HTML + th:* 属性”；这两个项目里，后端调用链大体一样，主要变化在页面模板表达方式和片段复用方式。`
