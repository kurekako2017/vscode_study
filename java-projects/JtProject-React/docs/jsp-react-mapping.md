# JSP ↔ React 对照表（JtProject-React）

本文件把项目中传统的 JSP 页面与 React 前端中对应的组件/视图做一一对照，便于按原来 JSP 的结构参照学习 React 实现。

> 使用说明：点击路径可以在编辑器中打开对应文件。JSP 文件保存在 `src/main/webapp/views/` 下，React 源码在 `frontend/src/` 下。

---

## 对照表（按 JSP 文件列出）

- adminlogin.jsp
  - 对应 React：AdminLoginView / AdminAuthForm
  - 路径：[frontend/src/views/AdminLoginView.tsx](frontend/src/views/AdminLoginView.tsx#L1), [frontend/src/components/AdminAuthForm.tsx](frontend/src/components/AdminAuthForm.tsx#L1)
  - 说明：后台管理员登录页，React 将表单作为受控组件并把提交交由 AppShell 处理（调用 /api/admin/login）

- register.jsp
  - 对应 React：UserLoginView / UserAuthForms（Register 区块）
  - 路径：[frontend/src/views/UserLoginView.tsx](frontend/src/views/UserLoginView.tsx#L1), [frontend/src/components/UserAuthForms.tsx](frontend/src/components/UserAuthForms.tsx#L1)
  - 说明：用户注册表单已被合并到用户登录页的组合组件中

- cart.jsp
  - 对应 React：CartView / CartList
  - 路径：[frontend/src/views/CartView.tsx](frontend/src/views/CartView.tsx#L1), [frontend/src/components/CartList.tsx](frontend/src/components/CartList.tsx#L1)
  - 说明：购物车展示与移除项逻辑由组件与父回调分离（AppShell 负责调用 API）

- cartproduct.jsp
  - 对应 React：CartList（购物车项片段）
  - 路径：[frontend/src/components/CartList.tsx](frontend/src/components/CartList.tsx#L1)

- adminHome.jsp
  - 对应 React：AdminDashboardView（后台概览页）
  - 路径：[frontend/src/views/AdminDashboardView.tsx](frontend/src/views/AdminDashboardView.tsx#L1)
  - 说明：概览卡片、分类管理、商品管理、客户列表与资料编辑都聚合在该视图下

- uproduct.jsp
  - 对应 React：ProductsView / ProductGrid（用户商品视图）
  - 路径：[frontend/src/views/ProductsView.tsx](frontend/src/views/ProductsView.tsx#L1), [frontend/src/components/ProductGrid.tsx](frontend/src/components/ProductGrid.tsx#L1)

- index.jsp
  - 对应 React：ProductsView（应用默认页，展示商品）
  - 路径：[frontend/src/views/ProductsView.tsx](frontend/src/views/ProductsView.tsx#L1)

- products.jsp
  - 对应 React：AdminDashboardView 中的 ProductManager（后台商品管理列表） / ProductGrid（预览）
  - 路径：[frontend/src/components/ProductManager.tsx](frontend/src/components/ProductManager.tsx#L1), [frontend/src/components/ProductGrid.tsx](frontend/src/components/ProductGrid.tsx#L1)

- updateProfile.jsp
  - 对应 React：ProfileEditor（管理员个人资料编辑）
  - 路径：[frontend/src/components/ProfileEditor.tsx](frontend/src/components/ProfileEditor.tsx#L1)

- productsUpdate.jsp
  - 对应 React：ProductManager（编辑模式）
  - 路径：[frontend/src/components/ProductManager.tsx](frontend/src/components/ProductManager.tsx#L1)

- productsAdd.jsp
  - 对应 React：ProductManager（新增模式）
  - 路径：[frontend/src/components/ProductManager.tsx](frontend/src/components/ProductManager.tsx#L1)

- categories.jsp
  - 对应 React：CategoryManager
  - 路径：[frontend/src/components/CategoryManager.tsx](frontend/src/components/CategoryManager.tsx#L1)

- displayCustomers.jsp
  - 对应 React：CustomerList
  - 路径：[frontend/src/components/CustomerList.tsx](frontend/src/components/CustomerList.tsx#L1)

- userLogin.jsp
  - 对应 React：UserLoginView / UserAuthForms（Login 区块）
  - 路径：[frontend/src/views/UserLoginView.tsx](frontend/src/views/UserLoginView.tsx#L1), [frontend/src/components/UserAuthForms.tsx](frontend/src/components/UserAuthForms.tsx#L1)

- test.jsp / test2.jsp
  - 对应 React： 无直接对应（测试/示例页），可忽略或参考 Controller 中的示例逻辑
  - 路径（JSP）：[src/main/webapp/views/test.jsp](src/main/webapp/views/test.jsp), [src/main/webapp/views/test2.jsp](src/main/webapp/views/test2.jsp)

---

## 控制器与路由对应（快速索引）

- 传统 MVC 控制器（返回 JSP）:
  - [src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)
  - [src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)
  - 说明：这些控制器包含了大量直接返回 JSP 的路由（例如 `/admin/products` → products.jsp）。React 版已把这些页面移至前端，不再需要在客户端渲染时通过 JSP 返回页面。

- REST API 控制器（React 前端使用）:
  - [src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java](../src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java)
  - 说明：前端的 `frontend/src/services/appService.ts` 调用的就是这些 `/api/...` 接口（加载会话、商品、分类、购物车、管理员接口等）。请优先阅读此文件以了解 API 细节。

---

## 快速跳转（常用前端入口）

- 入口（挂载）: [frontend/src/main.tsx](frontend/src/main.tsx#L1)
- 路由与应用壳: [frontend/src/App.tsx](frontend/src/App.tsx#L1)
- 状态 Hook: [frontend/src/hooks/useAppState.ts](frontend/src/hooks/useAppState.ts#L1)
- API 封装: [frontend/src/api.ts](frontend/src/api.ts#L1)
- 业务 Service: [frontend/src/services/appService.ts](frontend/src/services/appService.ts#L1)
- 类型定义: [frontend/src/types.ts](frontend/src/types.ts#L1)

---

如果需要，我可以：

1. 把每个 JSP 的关键表单字段逐项映射到对应 React 组件的输入字段（逐字段对照）。
2. 把上述对照生成 CSV 或表格，便于离线查阅。 
3. 在 React 组件中添加注释，标注对应 JSP 的具体代码片段（更细粒度）。

请选择要我继续的下一步（例如：“逐字段映射” 或 “生成 CSV”）。
