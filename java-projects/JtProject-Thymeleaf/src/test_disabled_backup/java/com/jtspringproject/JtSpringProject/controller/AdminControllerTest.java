package com.jtspringproject.JtSpringProject.controller;

import com.jtspringproject.JtSpringProject.controller.AdminController;
import com.jtspringproject.JtSpringProject.models.User;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.services.UserService;
import com.jtspringproject.JtSpringProject.services.ProductService;
import com.jtspringproject.JtSpringProject.services.CategoryService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;

/**
 * 管理员控制器单元测试类
 * 
 * 测试目标：AdminController.java
 * 
 * 测试内容：
 * 1. 管理员登录功能
 * 2. 管理员权限验证
 * 3. 商品管理（增删改查）
 * 4. 分类管理
 * 5. 用户管理
 * 
 * 注解说明：
 * - @SpringBootTest: 启动完整的Spring应用上下文
 * - @AutoConfigureMockMvc: 自动配置MockMvc，用于模拟HTTP请求
 * - @ActiveProfiles("test"): 使用test配置文件（application-test.properties）
 * - @Transactional: 测试后自动回滚数据库操作，保证测试间互不影响
 * 
 * @author Your Name
 * @date 2025-12-30
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("管理员功能测试")
public class AdminControllerTest {

    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private ProductService productService;
    
    @Autowired
    private CategoryService categoryService;
    
    private User adminUser;
    private User normalUser;
    private Category testCategory;
    
    /**
     * 每个测试方法执行前的准备工作
     * - 重置管理员登录状态
     * - 创建测试用的管理员账户
     * - 创建测试用的普通用户账户
     * - 创建测试用的商品分类
     */
    @BeforeEach
    void setUp() {
        // 重置静态登录状态（清除之前测试的影响）
        AdminController.adminlogcheck = 0;
        
        // 创建测试管理员账户
        adminUser = new User();
        adminUser.setUsername("testadmin");
        adminUser.setPassword("admin123");
        adminUser.setEmail("admin@test.com");
        adminUser.setRole("ROLE_ADMIN");
        adminUser.setAddress("Admin Test Address");
        userService.addUser(adminUser);
        
        // 创建测试普通用户账户
        normalUser = new User();
        normalUser.setUsername("testnormal");
        normalUser.setPassword("user123");
        normalUser.setEmail("user@test.com");
        normalUser.setRole("ROLE_NORMAL");
        normalUser.setAddress("User Test Address");
        userService.addUser(normalUser);
        
        // 创建测试商品分类
        testCategory = categoryService.addCategory("Test Category");
    }
    
    // ==================== 登录功能测试 ====================
    
    @Test
    @DisplayName("测试1：访问管理员登录页面应该成功")
    void testAccessAdminLoginPage() throws Exception {
        mockMvc.perform(get("/admin/login"))
                .andDo(print()) // 打印请求和响应详情（调试用）
                .andExpect(status().isOk()) // 期望HTTP状态码为200
                .andExpect(view().name("adminlogin")); // 期望返回adminlogin.jsp视图
    }
    
    @Test
    @DisplayName("测试2：使用正确的管理员账号密码登录应该成功")
    void testAdminLoginWithCorrectCredentials() throws Exception {
        mockMvc.perform(post("/admin/loginvalidate")
                .param("username", "testadmin")
                .param("password", "admin123"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminHome")) // 登录成功跳转到管理员主页
                .andExpect(model().attributeExists("username")); // Model中应包含username属性
        
        // 验证：登录状态标志应该被设置为1
        assert AdminController.adminlogcheck == 1 : "管理员登录状态应该为1";
    }
    
    @Test
    @DisplayName("测试3：使用错误的密码登录应该失败")
    void testAdminLoginWithWrongPassword() throws Exception {
        mockMvc.perform(post("/admin/loginvalidate")
                .param("username", "testadmin")
                .param("password", "wrongpassword"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminlogin")) // 登录失败返回登录页
                .andExpect(model().attribute("mode", "login")); // mode属性为"login"
        
        // 验证：登录状态标志应该保持为0
        assert AdminController.adminlogcheck == 0 : "登录失败时状态应该为0";
    }
    
    @Test
    @DisplayName("测试4：使用不存在的用户名登录应该失败")
    void testAdminLoginWithNonexistentUser() throws Exception {
        mockMvc.perform(post("/admin/loginvalidate")
                .param("username", "nonexistent")
                .param("password", "admin123"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminlogin"));
    }
    
    @Test
    @DisplayName("测试5：普通用户不能以管理员身份登录")
    void testNormalUserCannotLoginAsAdmin() throws Exception {
        mockMvc.perform(post("/admin/loginvalidate")
                .param("username", "testnormal")
                .param("password", "user123"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminlogin")); // 即使密码正确，普通用户也登录失败
        
        assert AdminController.adminlogcheck == 0 : "普通用户不应该能登录管理后台";
    }
    
    @Test
    @DisplayName("测试6：管理员登出功能应该正常工作")
    void testAdminLogout() throws Exception {
        // 先设置为已登录状态
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(get("/admin/logout"))
                .andDo(print())
                .andExpect(status().is3xxRedirection()) // 期望重定向
                .andExpect(redirectedUrl("/admin/login")); // 重定向到登录页
        
        // 验证：登录状态应该被清除
        assert AdminController.adminlogcheck == 0 : "登出后状态应该为0";
    }
    
    // ==================== 权限验证测试 ====================
    
    @Test
    @DisplayName("测试7：未登录时访问管理员主页应该被重定向到登录页")
    void testAccessAdminHomeWithoutLogin() throws Exception {
        AdminController.adminlogcheck = 0; // 确保未登录
        
        mockMvc.perform(get("/admin/"))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/login"));
    }
    
    @Test
    @DisplayName("测试8：已登录时访问管理员主页应该成功")
    void testAccessAdminHomeAfterLogin() throws Exception {
        AdminController.adminlogcheck = 1; // 设置为已登录
        
        mockMvc.perform(get("/admin/index"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminHome"));
    }
    
    @Test
    @DisplayName("测试9：未登录时访问商品管理页应该被重定向")
    void testAccessProductsWithoutLogin() throws Exception {
        AdminController.adminlogcheck = 0;
        
        mockMvc.perform(get("/admin/products"))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/"));
    }
    
    // ==================== 商品管理测试 ====================
    
    @Test
    @DisplayName("测试10：管理员应该能查看商品列表")
    void testViewProductList() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(get("/admin/products"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("products"))
                .andExpect(model().attributeExists("products")); // 应该包含商品列表
    }
    
    @Test
    @DisplayName("测试11：管理员应该能添加新商品")
    void testAddNewProduct() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(post("/admin/products")
                .param("name", "Test Product")
                .param("categoryid", String.valueOf(testCategory.getId()))
                .param("price", "100")
                .param("weight", "500")
                .param("quantity", "10")
                .param("description", "Test product description")
                .param("productImage", "test.jpg"))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/products"));
        
        // 验证：商品应该被成功添加到数据库
        var products = productService.getProducts();
        assert products.stream().anyMatch(p -> "Test Product".equals(p.getName())) 
                : "新商品应该在数据库中";
    }
    
    @Test
    @DisplayName("测试12：管理员应该能删除商品")
    void testDeleteProduct() throws Exception {
        AdminController.adminlogcheck = 1;
        
        // 先创建一个测试商品
        Product product = new Product();
        product.setName("Product to Delete");
        product.setPrice(200);
        product.setQuantity(5);
        product.setWeight(100);
        product.setDescription("Will be deleted");
        productService.addProduct(product);
        
        int productId = product.getId();
        
        mockMvc.perform(get("/admin/deleteProduct")
                .param("id", String.valueOf(productId)))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/products"));
    }
    
    @Test
    @DisplayName("测试13：管理员应该能更新商品信息")
    void testUpdateProduct() throws Exception {
        AdminController.adminlogcheck = 1;
        
        // 先创建一个测试商品
        Product product = new Product();
        product.setName("Original Product");
        product.setPrice(100);
        product.setQuantity(5);
        product.setWeight(100);
        product.setDescription("Original description");
        productService.addProduct(product);
        
        int productId = product.getId();
        
        mockMvc.perform(post("/admin/productsUpdate")
                .param("id", String.valueOf(productId))
                .param("name", "Updated Product")
                .param("categoryid", String.valueOf(testCategory.getId()))
                .param("price", "150")
                .param("weight", "200")
                .param("quantity", "8")
                .param("description", "Updated description")
                .param("productImage", "updated.jpg"))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/products"));
    }
    
    // ==================== 分类管理测试 ====================
    
    @Test
    @DisplayName("测试14：管理员应该能查看分类列表")
    void testViewCategoryList() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(get("/admin/categories"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("categories"))
                .andExpect(model().attributeExists("categories"));
    }
    
    @Test
    @DisplayName("测试15：管理员应该能添加新分类")
    void testAddNewCategory() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(post("/admin/categories")
                .param("categoryname", "New Test Category"))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/categories"));
        
        // 验证：分类应该被成功添加
        var categories = categoryService.getCategories();
        assert categories.stream().anyMatch(c -> "New Test Category".equals(c.getName()))
                : "新分类应该在数据库中";
    }
    
    @Test
    @DisplayName("测试16：管理员应该能删除分类")
    void testDeleteCategory() throws Exception {
        AdminController.adminlogcheck = 1;
        
        Category category = categoryService.addCategory("Category to Delete");
        int categoryId = category.getId();
        
        mockMvc.perform(get("/admin/categories/delete")
                .param("id", String.valueOf(categoryId)))
                .andDo(print())
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/categories"));
    }
    
    // ==================== 用户管理测试 ====================
    
    @Test
    @DisplayName("测试17：管理员应该能查看客户列表")
    void testViewCustomerList() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(get("/admin/customers"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("displayCustomers"))
                .andExpect(model().attributeExists("customers"));
    }
    
    // ==================== 边界条件测试 ====================
    
    @Test
    @DisplayName("测试18：添加商品时缺少必填字段应该处理异常")
    void testAddProductWithMissingFields() throws Exception {
        AdminController.adminlogcheck = 1;
        
        // 缺少商品名称
        mockMvc.perform(post("/admin/products")
                .param("categoryid", "1")
                .param("price", "100"))
                .andDo(print())
                .andExpect(status().is4xxClientError()); // 期望客户端错误
    }
    
    @Test
    @DisplayName("测试19：删除不存在的商品应该处理正常")
    void testDeleteNonexistentProduct() throws Exception {
        AdminController.adminlogcheck = 1;
        
        mockMvc.perform(get("/admin/deleteProduct")
                .param("id", "99999")) // 不存在的ID
                .andDo(print())
                .andExpect(status().is3xxRedirection());
    }
    
    @Test
    @DisplayName("测试20：使用空用户名登录应该失败")
    void testLoginWithEmptyUsername() throws Exception {
        mockMvc.perform(post("/admin/loginvalidate")
                .param("username", "")
                .param("password", "admin123"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(view().name("adminlogin"));
    }
}
