# JtProject-Thymeleaf 文档导航

这个目录现在以 `Thymeleaf 学习项目` 为主，不再把重点放在原始 JSP 启动记录上。

## 1. 最推荐先看的文档

1. [README.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/README.md)
2. [Thymeleaf学习指南.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/Thymeleaf学习指南.md)
3. [数据访问层与调用链学习文档.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/数据访问层与调用链学习文档.md)
4. [JSP页面 vs Thymeleaf页面逐页对照.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)
5. [JSP改写成Thymeleaf练习题.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/JSP%E6%94%B9%E5%86%99%E6%88%90Thymeleaf%E7%BB%83%E4%B9%A0%E9%A2%98.md)

## 2. reference

路径：`doc/reference/`

当前最有价值的参考文档：

- [Thymeleaf学习指南.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/Thymeleaf学习指南.md)
- [数据访问层与调用链学习文档.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/数据访问层与调用链学习文档.md)
- [JSP页面 vs Thymeleaf页面逐页对照.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/JSP页面%20vs%20Thymeleaf页面逐页对照.md)
- [JSP改写成Thymeleaf练习题.md](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/doc/reference/JSP%E6%94%B9%E5%86%99%E6%88%90Thymeleaf%E7%BB%83%E4%B9%A0%E9%A2%98.md)

## 3. 学习顺序建议

1. 先启动项目，访问 `http://localhost:8085/`
2. 看 `templates/` 下的页面代码
3. 对照 `controller/` 理解页面数据来源
4. 回看 `service/` 和 `dao/`，理解 Thymeleaf 只是视图层变化

## 4. 页面源码入口

- 登录页：[userLogin.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/userLogin.html)
- 商品列表：[uproduct.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/uproduct.html)
- 购物车：[cart.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/cart.html)
- 后台首页：[adminHome.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/adminHome.html)
- 分类管理：[categories.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/categories.html)
- 商品管理：[products.html](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/resources/templates/products.html)

## 5. 后端源码入口

- 用户控制器：[UserController.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/controller/UserController.java)
- 管理员控制器：[AdminController.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/controller/AdminController.java)
- 商品服务：[ProductServiceImpl.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/services/impl/ProductServiceImpl.java)
- 商品 DAO：[ProductDaoImpl.java](D:/dev/source_code/vscode_study/java-projects/JtProject-Thymeleaf/src/main/java/com/jtspringproject/JtSpringProject/dao/impl/ProductDaoImpl.java)
