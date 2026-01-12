package com.jtspringproject.JtSpringProject.controller;

import java.sql.*;
import java.sql.PreparedStatement;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.User;
import com.jtspringproject.JtSpringProject.services.CategoryService;
import com.jtspringproject.JtSpringProject.services.ProductService;
import com.jtspringproject.JtSpringProject.services.UserService;

/**
 * 管理员控制器
 * 负责处理所有管理员相关的HTTP请求，包括：
 * - 管理员登录认证
 * - 商品管理（CRUD操作）
 * - 分类管理（CRUD操作）
 * - 客户信息查看
 * - 管理员个人信息管理
 *
 * 注意：使用静态变量（adminlogcheck, usernameforclass）进行会话管理
 * 所有路由都以 /admin 为前缀
 */
@Controller
@RequestMapping("/admin")
public class AdminController {
	
	// 依赖注入：用户服务，用于处理用户相关业务逻辑
	@Lazy
	@Autowired
	private UserService userService;

	// 依赖注入：分类服务，用于处理商品分类相关业务逻辑
	@Lazy
	@Autowired
	private CategoryService categoryService;
	
	// 依赖注入：商品服务，用于处理商品相关业务逻辑
	@Lazy
	@Autowired
	private ProductService productService;
	
	// 管理员登录状态标志：0=未登录，1=已登录（静态变量，用于跨请求保持状态）
	static int adminlogcheck = 0;

	// 当前登录管理员的用户名（静态变量，用于跨请求保持状态）
	static String usernameforclass = "";

	/**
	 * 管理员退出登录或返回首页
	 * 路由：GET /admin/ 或 GET /admin/logout
	 *
	 * 功能：
	 * 1. 重置登录状态标志为0
	 * 2. 清空当前登录用户名
	 * 3. 重定向到用户登录页面
	 *
	 * @return 返回用户登录页面视图名称
	 */
	@RequestMapping(value = {"/","/logout"})
	public String returnIndex() {
		adminlogcheck =0;
		usernameforclass = "";
		return "userLogin";
	}
	
	
	
	/**
	 * 管理员首页
	 * 路由：GET /admin/index
	 *
	 * 功能：
	 * 1. 检查是否有用户名（判断是否登录）
	 * 2. 未登录：重定向到用户登录页面
	 * 3. 已登录：将用户名添加到模型中并返回首页视图
	 *
	 * @param model Spring MVC模型对象，用于向视图传递数据
	 * @return 返回index视图或userLogin视图
	 */
	@GetMapping("/index")
	public String index(Model model) {
		if("".equalsIgnoreCase(usernameforclass))
			return "userLogin";
		else {
			model.addAttribute("username", usernameforclass);
			return "index";
		}
			
	}
	
	
	/**
	 * 管理员登录页面
	 * 路由：GET /admin/login
	 *
	 * 功能：显示管理员登录页面
	 *
	 * @return 返回管理员登录页面视图
	 */
	@GetMapping("login")
	public String adminlogin() {
		
		return "adminlogin";
	}

	/**
	 * 管理员主控制台
	 * 路由：GET /admin/Dashboard
	 *
	 * 功能：
	 * 1. 检查管理员登录状态（adminlogcheck）
	 * 2. 已登录（adminlogcheck==1）：返回管理员主页
	 * 3. 未登录：重定向到管理员登录页面
	 *
	 * @param model Spring MVC模型对象
	 * @return 返回adminHome视图或重定向到登录页面
	 */
	@GetMapping("Dashboard")
	public String adminHome(Model model) {
		if(adminlogcheck==1)
			return "adminHome";
		else
			return "redirect:/admin/login";
	}

	/**
	 * 管理员登录验证页面（GET方法）
	 * 路由：GET /admin/loginvalidate
	 *
	 * 功能：返回管理员登录页面
	 *
	 * @param model Spring MVC模型对象
	 * @return 返回管理员登录页面视图
	 */
	@GetMapping("/loginvalidate")
	public String adminlog(Model model) {
		
		return "adminlogin";
	}

	/**
	 * 管理员登录验证（POST方法）
	 * 路由：POST /admin/loginvalidate
	 *
	 * 功能：
	 * 1. 接收用户名和密码参数
	 * 2. 调用userService.checkLogin()验证用户身份
	 * 3. 验证角色是否为ROLE_ADMIN
	 * 4. 成功：设置登录状态为1，返回管理员主页，并将用户信息添加到模型
	 * 5. 失败：返回登录页面，显示错误消息
	 *
	 * @param username 用户名
	 * @param pass 密码
	 * @return ModelAndView对象，包含视图名称和数据
	 */
	@RequestMapping(value = "loginvalidate", method = RequestMethod.POST)
	public ModelAndView adminlogin( @RequestParam("username") String username, @RequestParam("password") String pass) {
		
		User user=this.userService.checkLogin(username, pass);
		
		if("ROLE_ADMIN".equals(user.getRole())) {
			ModelAndView mv = new ModelAndView("adminHome");
			adminlogcheck=1;
			mv.addObject("admin", user);
			return mv;
		}
		else {
			ModelAndView mv = new ModelAndView("adminlogin");
			mv.addObject("msg", "Please enter correct username and password");
			return mv;
		}
	}

	/**
	 * 获取所有商品分类列表
	 * 路由：GET /admin/categories
	 *
	 * 功能：
	 * 1. 检查管理员登录状态
	 * 2. 未登录（adminlogcheck==0）：返回管理员登录页面
	 * 3. 已登录：查询所有分类并返回分类列表页面
	 *
	 * @return ModelAndView对象，包含分类列表数据和视图名称
	 */
	@GetMapping("categories")
	public ModelAndView getcategory() {
		if(adminlogcheck==0){
			ModelAndView mView = new ModelAndView("adminlogin");
			return mView;
		}
		else {
			ModelAndView mView = new ModelAndView("categories");
			List<Category> categories = this.categoryService.getCategories();
			mView.addObject("categories", categories);
			return mView;
		}
	}

	/**
	 * 添加新的商品分类
	 * 路由：POST /admin/categories
	 *
	 * 功能：
	 * 1. 接收分类名称参数
	 * 2. 调用categoryService.addCategory()添加新分类
	 * 3. 重定向到分类列表页面
	 *
	 * @param category_name 分类名称
	 * @return 重定向到分类列表页面
	 */
	@RequestMapping(value = "categories",method = RequestMethod.POST)
	public String addCategory(@RequestParam("categoryname") String category_name)
	{
		System.out.println(category_name);
		
		Category category =  this.categoryService.addCategory(category_name);
		if(category.getName().equals(category_name)) {
			return "redirect:categories";
		}else {
			return "redirect:categories";
		}
	}
	
	/**
	 * 删除指定的商品分类
	 * 路由：GET /admin/categories/delete?id={id}
	 *
	 * 功能：
	 * 1. 接收要删除的分类ID
	 * 2. 调用categoryService.deleteCategory()删除分类
	 * 3. 使用forward转发到分类列表页面（保持在同一请求中）
	 *
	 * @param id 要删除的分类ID
	 * @return ModelAndView对象，转发到分类列表页面
	 */
	@GetMapping("categories/delete")
	public ModelAndView removeCategoryDb(@RequestParam("id") int id)
	{	
			this.categoryService.deleteCategory(id);
			ModelAndView mView = new ModelAndView("forward:/categories");
			return mView;
	}
	
	/**
	 * 更新指定的商品分类
	 * 路由：GET /admin/categories/update?categoryid={id}&categoryname={name}
	 *
	 * 功能：
	 * 1. 接收分类ID和新的分类名称
	 * 2. 调用categoryService.updateCategory()更新分类信息
	 * 3. 重定向到分类列表页面
	 *
	 * @param id 要更新的分类ID
	 * @param categoryname 新的分类名称
	 * @return 重定向到分类列表页面
	 */
	@GetMapping("categories/update")
	public String updateCategory(@RequestParam("categoryid") int id, @RequestParam("categoryname") String categoryname)
	{
		this.categoryService.updateCategory(id, categoryname);
		return "redirect:/admin/categories";
	}

	
	// ========================== 商品管理模块 ==========================

	/**
	 * 获取所有商品列表
	 * 路由：GET /admin/products
	 *
	 * 功能：
	 * 1. 检查管理员登录状态
	 * 2. 未登录（adminlogcheck==0）：返回管理员登录页面
	 * 3. 已登录：查询所有商品并返回商品列表页面
	 * 4. 如果商品列表为空，显示"无商品可用"的消息
	 *
	 * @return ModelAndView对象，包含商品列表数据和视图名称
	 */
	@GetMapping("products")
	public ModelAndView getproduct() {
		if(adminlogcheck==0){
			ModelAndView mView = new ModelAndView("adminlogin");
			return mView;
		}
		else {
			ModelAndView mView = new ModelAndView("products");

			List<Product> products = this.productService.getProducts();

			if (products.isEmpty()) {
				mView.addObject("msg", "No products are available");
			} else {
				mView.addObject("products", products);
			}
			return mView;
		}

	}

	/**
	 * 显示添加商品的表单页面
	 * 路由：GET /admin/products/add
	 *
	 * 功能：
	 * 1. 查询所有商品分类
	 * 2. 将分类列表传递给视图，用于下拉选择
	 * 3. 返回添加商品的表单页面
	 *
	 * @return ModelAndView对象，包含分类列表和添加商品表单视图
	 */
	@GetMapping("products/add")
	public ModelAndView addProduct() {
		ModelAndView mView = new ModelAndView("productsAdd");
		List<Category> categories = this.categoryService.getCategories();
		mView.addObject("categories",categories);
		return mView;
	}

	/**
	 * 处理添加新商品的表单提交
	 * 路由：POST /admin/products/add
	 *
	 * 功能：
	 * 1. 接收商品的所有属性参数（名称、分类ID、价格、重量、数量、描述、图片）
	 * 2. 根据分类ID查询分类对象
	 * 3. 创建新的Product对象并设置所有属性
	 * 4. 调用productService.addProduct()保存商品
	 * 5. 重定向到商品列表页面
	 *
	 * @param name 商品名称
	 * @param categoryId 商品所属分类ID
	 * @param price 商品价格
	 * @param weight 商品重量
	 * @param quantity 商品库存数量
	 * @param description 商品描述
	 * @param productImage 商品图片路径
	 * @return 重定向到商品列表页面
	 */
	@RequestMapping(value = "products/add",method=RequestMethod.POST)
	public String addProduct(@RequestParam("name") String name,@RequestParam("categoryid") int categoryId ,@RequestParam("price") int price,@RequestParam("weight") int weight, @RequestParam("quantity")int quantity,@RequestParam("description") String description,@RequestParam("productImage") String productImage) {
		System.out.println(categoryId);
		Category category = this.categoryService.getCategory(categoryId);
		Product product = new Product();
		product.setId(categoryId);
		product.setName(name);
		product.setCategory(category);
		product.setDescription(description);
		product.setPrice(price);
		product.setImage(productImage);
		product.setWeight(weight);
		product.setQuantity(quantity);
		this.productService.addProduct(product);
		return "redirect:/admin/products";
	}

	/**
	 * 显示更新商品的表单页面
	 * 路由：GET /admin/products/update/{id}
	 *
	 * 功能：
	 * 1. 根据商品ID查询商品详细信息
	 * 2. 查询所有分类列表，用于下拉选择
	 * 3. 将商品信息和分类列表传递给视图
	 * 4. 返回更新商品的表单页面
	 *
	 * @param id 要更新的商品ID（路径变量）
	 * @return ModelAndView对象，包含商品信息、分类列表和更新表单视图
	 */
	@GetMapping("products/update/{id}")
	public ModelAndView updateproduct(@PathVariable("id") int id) {
		
		ModelAndView mView = new ModelAndView("productsUpdate");
		Product product = this.productService.getProduct(id);
		List<Category> categories = this.categoryService.getCategories();

		mView.addObject("categories",categories);
		mView.addObject("product", product);
		return mView;
	}
	
	/**
	 * 处理更新商品的表单提交
	 * 路由：POST /admin/products/update/{id}
	 *
	 * 功能：
	 * 1. 接收商品ID和所有要更新的属性参数
	 * 2. 调用productService.updateProduct()更新商品信息（当前未实现）
	 * 3. 重定向到商品列表页面
	 *
	 * 注意：此方法的业务逻辑尚未完全实现
	 *
	 * @param id 商品ID（路径变量）
	 * @param name 商品名称
	 * @param categoryId 商品所属分类ID
	 * @param price 商品价格
	 * @param weight 商品重量
	 * @param quantity 商品库存数量
	 * @param description 商品描述
	 * @param productImage 商品图片路径
	 * @return 重定向到商品列表页面
	 */
	@RequestMapping(value = "products/update/{id}",method=RequestMethod.POST)
	public String updateProduct(@PathVariable("id") int id ,@RequestParam("name") String name,@RequestParam("categoryid") int categoryId ,@RequestParam("price") int price,@RequestParam("weight") int weight, @RequestParam("quantity")int quantity,@RequestParam("description") String description,@RequestParam("productImage") String productImage)
	{

//		this.productService.updateProduct();
		return "redirect:/admin/products";
	}
	
	/**
	 * 删除指定的商品
	 * 路由：GET /admin/products/delete?id={id}
	 *
	 * 功能：
	 * 1. 接收要删除的商品ID
	 * 2. 调用productService.deleteProduct()删除商品
	 * 3. 重定向到商品列表页面
	 *
	 * @param id 要删除的商品ID
	 * @return 重定向到商品列表页面
	 */
	@GetMapping("products/delete")
	public String removeProduct(@RequestParam("id") int id)
	{
		this.productService.deleteProduct(id);
		return "redirect:/admin/products";
	}
	
	/**
	 * 处理商品相关的POST请求
	 * 路由：POST /admin/products
	 *
	 * 功能：重定向到分类列表页面
	 * 注意：此方法的用途不明确，可能是遗留代码
	 *
	 * @return 重定向到分类列表页面
	 */
	@PostMapping("products")
	public String postproduct() {
		return "redirect:/admin/categories";
	}
	
	/**
	 * 获取所有客户（用户）详细信息
	 * 路由：GET /admin/customers
	 *
	 * 功能：
	 * 1. 检查管理员登录状态
	 * 2. 未登录（adminlogcheck==0）：返回管理员登录页面
	 * 3. 已登录：查询所有用户并返回客户列表页面
	 *
	 * @return ModelAndView对象，包含客户列表数据和视图名称
	 */
	@GetMapping("customers")
	public ModelAndView getCustomerDetail() {
		if(adminlogcheck==0){
			ModelAndView mView = new ModelAndView("adminlogin");
			return mView;
		}
		else {
			ModelAndView mView = new ModelAndView("displayCustomers");
			List<User> users = this.userService.getUsers();
			mView.addObject("customers", users);
			return mView;
		}
	}
	
	
	/**
	 * 显示管理员个人资料页面
	 * 路由：GET /admin/profileDisplay
	 *
	 * 功能：
	 * 1. 使用JDBC直接查询数据库获取当前登录用户的详细信息
	 * 2. 从users表中查询用户ID、用户名、邮箱、密码、地址
	 * 3. 将查询结果添加到模型中
	 * 4. 返回更新个人资料的表单页面
	 *
	 * 注意：此方法直接使用JDBC而非通过Service层，且数据库连接信息硬编码
	 *
	 * @param model Spring MVC模型对象，用于向视图传递数据
	 * @return 返回更新个人资料页面视图
	 */
	@GetMapping("profileDisplay")
	public String profileDisplay(Model model) {
		String displayusername,displaypassword,displayemail,displayaddress;
		try
		{
			Class.forName("com.mysql.jdbc.Driver");
			Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/ecommjava","root","");
			PreparedStatement stmt = con.prepareStatement("select * from users where username = ?"+";");
			stmt.setString(1, usernameforclass);
			ResultSet rst = stmt.executeQuery();
			
			if(rst.next())
			{
			int userid = rst.getInt(1);
			displayusername = rst.getString(2);
			displayemail = rst.getString(3);
			displaypassword = rst.getString(4);
			displayaddress = rst.getString(5);
			model.addAttribute("userid",userid);
			model.addAttribute("username",displayusername);
			model.addAttribute("email",displayemail);
			model.addAttribute("password",displaypassword);
			model.addAttribute("address",displayaddress);
			}
		}
		catch(Exception e)
		{
			System.out.println("Exception:"+e);
		}
		System.out.println("Hello");
		return "updateProfile";
	}
	
	/**
	 * 处理更新用户个人资料的表单提交
	 * 路由：POST /admin/updateuser
	 *
	 * 功能：
	 * 1. 接收用户ID和要更新的所有个人信息（用户名、邮箱、密码、地址）
	 * 2. 使用JDBC直接执行UPDATE SQL语句更新数据库
	 * 3. 更新成功后，将新的用户名赋值给usernameforclass静态变量
	 * 4. 重定向到首页
	 *
	 * 注意：此方法直接使用JDBC而非通过Service层，且数据库连接信息硬编码
	 *
	 * @param userid 用户ID
	 * @param username 新的用户名
	 * @param email 新的邮箱
	 * @param password 新的密码
	 * @param address 新的地址
	 * @return 重定向到首页
	 */
	@RequestMapping(value = "updateuser",method=RequestMethod.POST)
	public String updateUserProfile(@RequestParam("userid") int userid,@RequestParam("username") String username, @RequestParam("email") String email, @RequestParam("password") String password, @RequestParam("address") String address) 
	
	{
		try
		{
			Class.forName("com.mysql.jdbc.Driver");
			Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/ecommjava","root","");
			
			PreparedStatement pst = con.prepareStatement("update users set username= ?,email = ?,password= ?, address= ? where uid = ?;");
			pst.setString(1, username);
			pst.setString(2, email);
			pst.setString(3, password);
			pst.setString(4, address);
			pst.setInt(5, userid);
			int i = pst.executeUpdate();	
			usernameforclass = username;
		}
		catch(Exception e)
		{
			System.out.println("Exception:"+e);
		}
		return "redirect:/index";
	}

}
