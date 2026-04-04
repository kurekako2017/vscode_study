# JSP 改写成 Thymeleaf 练习题

这份文档的目标不是讲概念，而是让你真正动手练：

`把 JSP 写法改成 Thymeleaf 写法`

建议你练习时遵循这个顺序：

1. 先看题目
2. 自己先写答案
3. 再看参考答案
4. 最后去项目真实页面里找同类写法

---

## 1. 练习前先记住转换思路

JSP 到 Thymeleaf，最常见的变化就是：

- `${...}` 输出值 -> `th:text`
- `c:if` -> `th:if`
- `c:forEach` -> `th:each`
- `href="/xxx"` -> `th:href="@{/xxx}"`
- `action="/xxx"` -> `th:action="@{/xxx}"`
- `value="${...}"` -> `th:value="${...}"`

一句话记忆：

`JSP 更偏“标签 + 表达式”，Thymeleaf 更偏“HTML 标签 + th:* 属性”。`

---

## 2. 练习 1：输出普通文本

### JSP 写法

```jsp
<h3>${product.name}</h3>
```

### 你的任务

把它改成 Thymeleaf 写法。

### 参考答案

```html
<h3 th:text="${product.name}">商品名称</h3>
```

### 说明

- `th:text` 会替换标签内部文本
- `商品名称` 是占位内容，便于模板源码阅读

---

## 3. 练习 2：输出带说明的文本

### JSP 写法

```jsp
<p>Price: ${product.price}</p>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<p th:text="'Price: ' + ${product.price}">Price: 0</p>
```

### 说明

- Thymeleaf 可以在表达式里拼接字符串

---

## 4. 练习 3：条件渲染消息

### JSP 写法

```jsp
<c:if test="${not empty msg}">
    <div class="alert alert-warning">${msg}</div>
</c:if>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<div class="alert alert-warning" th:if="${msg != null and !#strings.isEmpty(msg)}" th:text="${msg}">
  提示消息
</div>
```

### 说明

- `th:if` 控制标签是否渲染
- `th:text` 输出具体值

---

## 5. 练习 4：遍历商品列表

### JSP 写法

```jsp
<c:forEach var="product" items="${products}">
    <tr>
        <td>${product.name}</td>
        <td>${product.price}</td>
    </tr>
</c:forEach>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<tr th:each="product : ${products}">
  <td th:text="${product.name}">商品名</td>
  <td th:text="${product.price}">0</td>
</tr>
```

### 说明

- `var="product"` 变成 `product : ${products}`
- 每个字段通常用 `th:text` 单独输出

---

## 6. 练习 5：表单 action 改写

### JSP 写法

```jsp
<form action="/userloginvalidate" method="post">
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<form th:action="@{/userloginvalidate}" method="post">
```

### 说明

- `@{...}` 是 Thymeleaf 的 URL 表达式

---

## 7. 练习 6：链接地址改写

### JSP 写法

```jsp
<a href="/register">Register here</a>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<a th:href="@{/register}">Register here</a>
```

---

## 8. 练习 7：隐藏字段回填

### JSP 写法

```jsp
<input type="hidden" name="id" value="${product.id}">
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<input type="hidden" name="id" th:value="${product.id}">
```

---

## 9. 练习 8：输入框回填

### JSP 写法

```jsp
<input type="text" name="username" value="${username}">
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<input type="text" name="username" th:value="${username}">
```

---

## 10. 练习 9：下拉框选中值

### JSP 场景

JSP 里常常会通过脚本或复杂条件让某一项选中。

例如逻辑目标是：

- 遍历所有分类
- 如果 `category.id == product.category.id`，就让当前 option 选中

### Thymeleaf 参考答案

```html
<option th:each="category : ${categories}"
        th:value="${category.id}"
        th:selected="${product.category != null and category.id == product.category.id}"
        th:text="${category.name}">
  分类
</option>
```

### 说明

- 这个练习很适合对照
  [productsUpdate.html](../../src/main/resources/templates/productsUpdate.html)

---

## 11. 练习 10：带参数链接

### JSP 写法

```jsp
<a href="/admin/products/delete?id=${product.id}">Delete</a>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<a th:href="@{/admin/products/delete(id=${product.id})}">Delete</a>
```

### 说明

- Thymeleaf 生成带参数 URL 时非常常用这种写法

---

## 12. 练习 11：组合条件判断

### JSP 写法

```jsp
<c:if test="${empty products}">
    <p>No products found.</p>
</c:if>
```

### 你的任务

改成 Thymeleaf 写法。

### 参考答案

```html
<p th:if="${products == null or #lists.isEmpty(products)}">No products found.</p>
```

---

## 13. 练习 12：公共头部引入

### JSP 常见思路

```jsp
<jsp:include page="/views/common/header.jsp" />
```

### 你的任务

改成 Thymeleaf 片段引入思路。

### 参考答案

```html
<nav th:replace="fragments/layout :: userNav('products')"></nav>
```

### 说明

- JSP 常用 include
- Thymeleaf 常用 `th:replace`
- 对照文件：
  [layout.html](../../src/main/resources/templates/fragments/layout.html)

---

## 14. 综合练习 1：把商品表格的一行改成 Thymeleaf

### JSP 写法

```jsp
<tr>
    <td>${product.name}</td>
    <td>${product.category.name}</td>
    <td>${product.price}</td>
    <td>
        <form action="/products/addtocart" method="get">
            <input type="hidden" name="id" value="${product.id}">
            <input type="submit" value="Add To Cart">
        </form>
    </td>
</tr>
```

### 你的任务

把这一整段改成 Thymeleaf 风格。

### 参考答案

```html
<tr>
  <td th:text="${product.name}">商品名</td>
  <td th:text="${product.category != null ? product.category.name : '未分类'}">分类</td>
  <td th:text="${product.price}">0</td>
  <td>
    <form th:action="@{/products/addtocart}" method="post">
      <input type="hidden" name="id" th:value="${product.id}">
      <button type="submit">Add To Cart</button>
    </form>
  </td>
</tr>
```

---

## 15. 综合练习 2：把登录错误消息块改成 Thymeleaf

### JSP 写法

```jsp
<br><h3 style="color:red;">${msg}</h3><br>
```

### 你的任务

改成“只有在 msg 存在时才显示”的 Thymeleaf 写法。

### 参考答案

```html
<h3 style="color:red;" th:if="${msg != null and !#strings.isEmpty(msg)}" th:text="${msg}">
  错误消息
</h3>
```

---

## 16. 去哪里找真实例子

做完这些练习后，建议你直接去项目里找真实代码：

- 登录页：
  [userLogin.html](../../src/main/resources/templates/userLogin.html)
- 商品列表：
  [uproduct.html](../../src/main/resources/templates/uproduct.html)
- 购物车：
  [cart.html](../../src/main/resources/templates/cart.html)
- 分类管理：
  [categories.html](../../src/main/resources/templates/categories.html)
- 商品编辑：
  [productsUpdate.html](../../src/main/resources/templates/productsUpdate.html)

---

## 17. 推荐练习顺序

最适合你的顺序是：

1. 练习 1 到 4  
   先掌握 `th:text`、`th:if`、`th:each`
2. 练习 5 到 10  
   再掌握 `th:href`、`th:action`、`th:value`
3. 练习 11 到 12  
   再掌握条件判断和片段复用
4. 综合练习  
   开始整段改写

---

## 18. 一句话总结

如果你做完这份练习还能记住一句话，那就记这句：

`把 JSP 改写成 Thymeleaf，本质上就是把“标签库和表达式”改写成“HTML 标签上的 th:* 属性”。`
