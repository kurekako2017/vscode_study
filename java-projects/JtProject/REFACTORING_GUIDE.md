# 接口重构指南 - 依赖倒置原则实现

## 📋 重构概览

本次重构为项目的Service层和DAO层全面引入了接口，遵循**依赖倒置原则（Dependency Inversion Principle）**，这是SOLID原则中的核心设计原则。

### 重构前架构
```
Controller
    ↓ 直接依赖
具体实现类 (categoryService, productService...)
    ↓ 直接依赖
具体实现类 (categoryDao, productDao...)
```

### 重构后架构
```
Controller
    ↓ 依赖接口
Service Interface (CategoryService, ProductService...)
    ↓ 实现
ServiceImpl (CategoryServiceImpl, ProductServiceImpl...)
    ↓ 依赖接口
DAO Interface (CategoryDao, ProductDao...)
    ↓ 实现
DaoImpl (CategoryDaoImpl, ProductDaoImpl...)
```

## 🎯 重构目标

1. **遵循依赖倒置原则** - 高层模块不依赖低层模块，两者都依赖抽象
2. **提高可测试性** - 便于使用Mock对象进行单元测试
3. **增强扩展性** - 同一接口可有多个实现（如不同数据源）
4. **降低耦合度** - Controller不需要知道Service的具体实现
5. **符合Spring最佳实践** - 遵循Spring官方推荐的分层架构

## 📂 新增接口列表

### Service层接口 (`src/main/java/.../services/`)

| 接口名 | 说明 | 方法数 |
|--------|------|--------|
| **CartService** | 购物车服务接口 | 4 |
| **CategoryService** | 分类服务接口 | 5 |
| **ProductService** | 商品服务接口 | 5 |
| **UserService** | 用户服务接口 | 4 |

### DAO层接口 (`src/main/java/.../dao/`)

| 接口名 | 说明 | 方法数 |
|--------|------|--------|
| **CartDao** | 购物车数据访问接口 | 4 |
| **CartProductDao** | 购物车商品数据访问接口 | 5 |
| **CategoryDao** | 分类数据访问接口 | 5 |
| **ProductDao** | 商品数据访问接口 | 5 |
| **UserDao** | 用户数据访问接口 | 4 |

## 🔄 文件变更详情

### 新增文件

#### Service接口 + 实现类
```
services/
├── CartService.java              (新增接口)
├── CategoryService.java          (新增接口)
├── ProductService.java           (新增接口)
├── UserService.java              (新增接口)
└── impl/                         (新增目录)
    ├── CartServiceImpl.java      
    ├── CategoryServiceImpl.java
    ├── ProductServiceImpl.java
    └── UserServiceImpl.java
```

#### DAO接口 + 实现类
```
dao/
├── CartDao.java                  (新增接口)
├── CartProductDao.java           (新增接口)
├── CategoryDao.java              (新增接口)
├── ProductDao.java               (新增接口)
├── UserDao.java                  (新增接口)
└── impl/                         (新增目录)
    ├── CartDaoImpl.java
    ├── CartProductDaoImpl.java
    ├── CategoryDaoImpl.java
    ├── ProductDaoImpl.java
    └── UserDaoImpl.java
```

### 删除文件（旧实现类）
```
services/
├── cartService.java          (已删除)
├── categoryService.java      (已删除)
├── productService.java       (已删除)
└── userService.java          (已删除)

dao/
├── cartDao.java              (已删除)
├── cartProductDao.java       (已删除)
├── categoryDao.java          (已删除)
├── productDao.java           (已删除)
└── userDao.java              (已删除)
```

### 修改文件
```
controller/
├── AdminController.java      (更新依赖注入)
└── UserController.java       (更新依赖注入)

test/.../controller/
├── AdminControllerTest.java  (更新import)
└── UserControllerTest.java   (更新import)
```

## 💡 代码示例

### 1. Service接口定义
```java
package com.jtspringproject.JtSpringProject.services;

import com.jtspringproject.JtSpringProject.models.Product;
import java.util.List;

/**
 * 商品服务接口
 * 定义商品业务逻辑的契约
 */
public interface ProductService {
    List<Product> getProducts();
    Product addProduct(Product product);
    Product getProduct(int id);
    Product updateProduct(int id, Product product);
    boolean deleteProduct(int id);
}
```

### 2. Service实现类
```java
package com.jtspringproject.JtSpringProject.services.impl;

import com.jtspringproject.JtSpringProject.dao.ProductDao;
import com.jtspringproject.JtSpringProject.services.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ProductServiceImpl implements ProductService {
    
    @Autowired
    private ProductDao productDao;  // 依赖DAO接口
    
    @Override
    public List<Product> getProducts() {
        return this.productDao.getProducts();
    }
    
    // ...其他方法实现
}
```

### 3. Controller依赖接口
```java
@Controller
public class AdminController {
    
    @Autowired
    private UserService userService;        // 依赖接口（首字母大写）
    
    @Autowired
    private CategoryService categoryService;  // 依赖接口
    
    @Autowired
    private ProductService productService;   // 依赖接口
    
    // Spring自动注入接口的唯一实现类
}
```

### 4. 单元测试使用Mock
```java
@SpringBootTest
public class ProductServiceTest {
    
    @Mock
    private ProductDao productDao;  // Mock DAO接口
    
    @InjectMocks
    private ProductServiceImpl productService;
    
    @Test
    void testGetProducts() {
        // 可以轻松mock接口行为
        when(productDao.getProducts()).thenReturn(mockList);
        
        List<Product> result = productService.getProducts();
        
        assertNotNull(result);
        verify(productDao, times(1)).getProducts();
    }
}
```

## ✅ 架构优势

### 1. 依赖倒置原则（DIP）
- **之前**: Controller → 具体Service类 → 具体DAO类
- **现在**: Controller → Service接口 ← ServiceImpl → DAO接口 ← DaoImpl
- **优势**: 高层模块和低层模块都依赖抽象，降低耦合

### 2. 开闭原则（OCP）
```java
// 扩展新实现，无需修改Controller代码
@Service
@Primary  // 如果有多个实现，使用@Primary指定默认实现
public class ProductServiceRedisImpl implements ProductService {
    // Redis缓存实现
}

@Service
@Qualifier("mysql")
public class ProductServiceMySQLImpl implements ProductService {
    // MySQL数据库实现
}
```

### 3. 里氏替换原则（LSP）
```java
// 任何使用ProductService接口的地方
// 都可以透明地替换为不同的实现
@Autowired
@Qualifier("redis")
private ProductService productService;  // 可切换为Redis实现
```

### 4. 单元测试优势
```java
// 测试时可以轻松替换为Mock对象
@Test
void testAdminLogin() {
    UserService mockUserService = Mockito.mock(UserService.class);
    when(mockUserService.checkLogin("admin", "123"))
        .thenReturn(adminUser);
    
    // 测试业务逻辑，无需真实数据库
}
```

## 🔧 Spring依赖注入机制

### 自动注入规则
```java
@Autowired
private ProductService productService;  // Spring自动查找ProductService接口的实现类
```

Spring查找顺序：

---

## 🛠️ 近期功能修复（2026-02）

以下功能已完成修复并可直接使用：

1. **后台商品更新功能打通**
    - `AdminController.updateProduct(...)` 已接入 `productService.updateProduct(...)`。
    - 更新时若未传图片，保留原图片地址。

2. **路由与导航修复**
    - 多个 JSP 页面的历史错误路由（如 `/adminhome`）已统一修复为有效路由（如 `/admin/index`）。
    - 管理员退出统一使用 `/admin/logout`，用户退出使用 `/logout`。

3. **用户退出功能补齐**
    - 新增用户登出路由 `/logout`，会清理 `username` Cookie 并返回登录首页。

4. **购物车能力增强**
    - 加购时支持商品不存在校验，避免空对象入库。
    - 新增从购物车删除商品功能：`GET /user/cart/delete?id={productId}`。
    - `cart.jsp` 已接入删除按钮。

5. **遗留页面兼容**
    - `cartproduct.jsp` 已改为兼容跳转页，统一重定向到 `/user/cart`，避免旧 JDBC 页面继续使用。

---

## 🧪 测试类使用教程

> 说明：当前项目 `pom.xml` 中默认 `skipTests=true`，需要在命令行显式关闭跳过测试。

### 1) 运行单个测试类

```powershell
mvn -q -DskipTests=false "-Dtest=UserControllerCartTest" test
```

### 2) 运行多个测试类

```powershell
mvn -q -DskipTests=false "-Dtest=AdminControllerProductUpdateTest,UserControllerCartTest" test
```

### 3) 运行单个测试方法

```powershell
mvn -q -DskipTests=false "-Dtest=UserControllerCartTest#addToCart_shouldAddProduct_whenUserAndProductAreValid" test
```

### 4) 测试文件位置

- `src/test/java/com/jtspringproject/JtSpringProject/controller/AdminControllerProductUpdateTest.java`
- `src/test/java/com/jtspringproject/JtSpringProject/controller/UserControllerCartTest.java`

### 5) 常见问题

- **PowerShell 报 `Missing argument in parameter list`**
  - 原因：`-Dtest=A,B` 在 PowerShell 被错误解析。
  - 解决：给 `-Dtest` 参数加引号：`"-Dtest=A,B"`。

- **命令执行后看不到测试输出**
  - 可去掉 `-q`：

```powershell
mvn -DskipTests=false "-Dtest=UserControllerCartTest" test
```
1. 查找类型匹配的Bean（ProductService类型）
2. 如果只有一个实现类（ProductServiceImpl），自动注入
3. 如果有多个实现类：
   - 使用 `@Primary` 标记默认实现
   - 使用 `@Qualifier("name")` 指定具体实现

### 多实现场景示例
```java
// 场景：支付服务有微信和支付宝两种实现

// 接口
public interface PaymentService {
    void pay(double amount);
}

// 实现1：微信支付
@Service("wechat")
public class WeChatPaymentServiceImpl implements PaymentService {
    @Override
    public void pay(double amount) {
        // 微信支付逻辑
    }
}

// 实现2：支付宝支付
@Service("alipay")
@Primary  // 默认使用支付宝
public class AlipayPaymentServiceImpl implements PaymentService {
    @Override
    public void pay(double amount) {
        // 支付宝支付逻辑
    }
}

// 使用
@Controller
public class OrderController {
    
    @Autowired
    private PaymentService paymentService;  // 默认注入支付宝实现
    
    @Autowired
    @Qualifier("wechat")
    private PaymentService wechatPayment;   // 明确指定微信实现
}
```

## 📊 命名规范对比

### 重构前（非标准）
- Service实现类: `categoryService`（小写开头）
- DAO实现类: `categoryDao`（小写开头）
- 问题：违反Java命名规范，类名应首字母大写

### 重构后（符合规范）
- Service接口: `CategoryService`（首字母大写）
- Service实现类: `CategoryServiceImpl`（首字母大写 + Impl后缀）
- DAO接口: `CategoryDao`（首字母大写）
- DAO实现类: `CategoryDaoImpl`（首字母大写 + Impl后缀）
- 优势：符合Java和Spring规范，易于区分接口和实现

## 🚀 验证重构成功

### 1. 编译检查
```bash
cd /workspaces/study/java-projects/JtProject
mvn clean compile
# 输出: BUILD SUCCESS
```

### 2. 查看项目结构
```bash
tree src/main/java/com/jtspringproject/JtSpringProject/

src/main/java/com/jtspringproject/JtSpringProject/
├── services/
│   ├── CartService.java           ← 接口
│   ├── CategoryService.java       ← 接口
│   ├── ProductService.java        ← 接口
│   ├── UserService.java           ← 接口
│   └── impl/
│       ├── CartServiceImpl.java
│       ├── CategoryServiceImpl.java
│       ├── ProductServiceImpl.java
│       └── UserServiceImpl.java
└── dao/
    ├── CartDao.java               ← 接口
    ├── CategoryDao.java           ← 接口
    ├── ProductDao.java            ← 接口
    ├── UserDao.java               ← 接口
    └── impl/
        ├── CartDaoImpl.java
        ├── CategoryDaoImpl.java
        ├── ProductDaoImpl.java
        └── UserDaoImpl.java
```

### 3. 运行应用
```bash
mvn spring-boot:run
# 应用正常启动，访问 http://localhost:8082
```

### 4. 检查依赖注入
```bash
# 查看Spring容器中的Bean
# 应该能看到所有接口的实现类都被正确注册
```

## 📝 最佳实践建议

### 1. 接口设计原则
- ✅ 接口应定义契约，不包含实现细节
- ✅ 方法命名清晰，返回值明确
- ✅ 添加完整的JavaDoc注释
- ❌ 避免接口中定义常量（除非是真正的常量契约）

### 2. 实现类规范
- ✅ 实现类添加 `Impl` 后缀
- ✅ 实现类放在 `impl` 子包中
- ✅ 使用 `@Service` 或 `@Repository` 注解
- ✅ 使用 `@Override` 注解标记实现方法

### 3. 依赖注入建议
- ✅ 优先使用构造器注入（便于测试）
- ✅ Controller和Service层依赖接口
- ✅ 接口有多个实现时使用 `@Qualifier`
- ⚠️ 避免循环依赖

### 4. 测试最佳实践
```java
// 推荐：使用Mockito mock接口
@Test
void testService() {
    ProductDao mockDao = Mockito.mock(ProductDao.class);
    ProductService service = new ProductServiceImpl(mockDao);
    // 测试业务逻辑
}

// 集成测试：使用真实Bean
@SpringBootTest
@Transactional
class ProductServiceIntegrationTest {
    @Autowired
    private ProductService productService;  // 注入真实实现
    
    @Test
    void testRealDatabase() {
        // 测试与真实数据库的交互
    }
}
```

## 🔗 相关资源

- [SOLID原则详解](https://en.wikipedia.org/wiki/SOLID)
- [Spring依赖注入文档](https://docs.spring.io/spring-framework/reference/core/beans/dependencies.html)
- [Java接口设计最佳实践](https://www.baeldung.com/java-interface-design)
- [Spring Boot测试指南](https://spring.io/guides/gs/testing-web/)

## 📧 问题反馈

如有问题或建议，请提交Issue或联系开发团队。

---

**重构日期**: 2025-12-30  
**重构人员**: GitHub Copilot  
**Commit Hash**: 3f93a45  
**影响范围**: Service层 + DAO层 + Controller层 + 测试层

