package com.jtspringproject.JtSpringProject.controller;

import com.jtspringproject.JtSpringProject.models.Cart;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.User;

import java.io.Console;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;

import com.jtspringproject.JtSpringProject.services.CartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import com.jtspringproject.JtSpringProject.services.UserService;
import com.jtspringproject.JtSpringProject.services.ProductService;


/**
 * 用户控制器
 * 负责处理所有普通用户相关的HTTP请求，包括：
 * - 用户登录认证
 * - 用户注册
 * - 商品浏览
 * - 购买操作
 * - 测试页面（用于学习Model和ModelAndView的使用）
 *
 * 此控制器不使用路径前缀，直接映射到根路径
 */
@Controller
public class UserController{
	
	// 依赖注入：用户服务，用于处理用户相关业务逻辑
	@Autowired
	private UserService userService;

	// 依赖注入：商品服务，用于处理商品相关业务逻辑
	@Autowired
	private ProductService productService;

	/**
	 * 用户注册页面
	 * 路由：GET /register
	 *
	 * 📝 调用流程：
	 * 1. 用户在登录页面点击 "Register here" 链接
	 * 2. 浏览器发送 GET /register 请求
	 * 3. DispatcherServlet 路由到此方法
	 * 4. 返回 "register" 视图名称
	 * 5. ViewResolver 解析为 /views/register.jsp
	 * 6. 渲染注册表单页面返回给浏览器
	 *
	 * 功能：显示用户注册表单页面
	 *
	 * @return 返回注册页面视图名称
	 */
	@GetMapping("/register")
	public String registerUser()
	{
		return "register";
	}

	/**
	 * 购买页面
	 * 路由：GET /buy
	 *
	 * 📝 功能说明：
	 * 显示购买页面，用户可以在此页面完成购买操作
	 *
	 * 注意：这是预留功能，具体业务逻辑待完善
	 *
	 * @return 返回购买页面视图名称
	 */
	@GetMapping("/buy")
	public String buy()
	{
		return "buy";
	}
	

	/**
	 * 用户登录页面（根路径）
	 * 路由：GET /
	 *
	 * 📝 调用时机：
	 * 1. 用户首次访问网站（http://localhost:8080/）
	 * 2. 用户点击退出登录
	 * 3. 需要重新登录时
	 *
	 * 功能：显示用户登录页面，作为应用的默认首页
	 *
	 * @param model Spring MVC模型对象（当前方法未使用，预留参数）
	 * @return 返回用户登录页面视图名称
	 */
	@GetMapping("/")
	public String userlogin(Model model) {
		
		return "userLogin";
	}

	/**
	 * 用户登录验证
	 * 路由：POST /userloginvalidate
	 *
	 * 📝 完整调用流程：
	 * ┌──────────────────────────────────────────────────────────────┐
	 * │ 步骤1: 用户在 userLogin.jsp 输入用户名和密码                 │
	 * │ 步骤2: 点击 Login 按钮                                       │
	 * │ 步骤3: 浏览器发送 POST /userloginvalidate 请求               │
	 * │ 步骤4: DispatcherServlet 接收请求                            │
	 * │ 步骤5: 路由匹配到此方法（@RequestMapping匹配）               │
	 * │ 步骤6: Spring自动注入参数（username, password等）            │
	 * │ 步骤7: 执行此方法的业务逻辑                                  │
	 * │ 步骤8: 返回 ModelAndView                                     │
	 * │ 步骤9: ViewResolver 解析视图名称                             │
	 * │ 步骤10: 渲染 JSP 页面返回给浏览器                            │
	 * └──────────────────────────────────────────────────────────────┘
	 *
	 * 功能详解：
	 * 1. 接收用户名和密码参数
	 *    - @RequestParam("username") 从表单获取 username 字段
	 *    - @RequestParam("password") 从表单获取 password 字段
	 *
	 * 2. 调用 userService.checkLogin() 验证用户身份
	 *    - Service层会调用 DAO层查询数据库
	 *    - 比对用户名和密码是否匹配
	 *
	 * 3. 验证成功的处理：
	 *    - 创建Cookie保存用户名（用于会话管理）
	 *    - 查询所有商品列表
	 *    - 返回首页（index.jsp），显示商品列表
	 *
	 * 4. 验证失败的处理：
	 *    - 返回登录页面（userLogin.jsp）
	 *    - 显示错误消息"请输入正确的邮箱和密码"
	 *
	 * @param username 用户名（来自表单的 name="username" 字段）
	 * @param pass 密码（来自表单的 name="password" 字段）
	 * @param model Spring MVC模型对象（用于传递数据到视图）
	 * @param res HttpServletResponse对象（用于添加Cookie）
	 * @return ModelAndView对象，包含视图名称和数据
	 */
	@RequestMapping(value = "userloginvalidate", method = RequestMethod.POST)
	public ModelAndView userlogin(
			@RequestParam("username") String username,
			@RequestParam("password") String pass,
			Model model,
			HttpServletResponse res) {

		// 打印接收到的参数（用于调试）
		System.out.println("收到登录请求 - 用户名: " + username);
		System.out.println("收到登录请求 - 密码: " + pass);

		// 调用 Service 层验证用户登录
		// 流程: Controller → UserService → UserDao → 数据库
		User u = this.userService.checkLogin(username, pass);

		// 打印查询结果（用于调试）
		System.out.println("数据库查询结果 - 用户名: " + u.getUsername());

		// 判断用户名是否匹配（验证登录是否成功）
		if(username.equals(u.getUsername())) {
			// ✅ 登录成功的处理逻辑

			// 1. 创建Cookie保存用户名（用于客户端会话管理）
			res.addCookie(new Cookie("username", u.getUsername()));

			// 2. 创建 ModelAndView，指定返回首页视图
			ModelAndView mView  = new ModelAndView("index");

			// 3. 将用户对象添加到模型中（视图可以访问用户信息）
			mView.addObject("user", u);

			// 4. 查询所有商品列表（用于首页展示）
			List<Product> products = this.productService.getProducts();

			// 5. 判断商品列表是否为空
			if (products.isEmpty()) {
				// 商品列表为空，添加提示信息
				mView.addObject("msg", "No products are available");
			} else {
				// 商品列表不为空，将商品数据传递到视图
				mView.addObject("products", products);
			}

			// 6. 返回 ModelAndView（会渲染 index.jsp 页面）
			return mView;

		} else {
			// ❌ 登录失败的处理逻辑

			// 1. 创建 ModelAndView，返回登录页面
			ModelAndView mView = new ModelAndView("userLogin");

			// 2. 添加错误消息（会在登录页面显示）
			mView.addObject("msg", "Please enter correct email and password");

			// 3. 返回登录页面（用户可以重新尝试登录）
			return mView;
		}
		
	}
	
	
	/**
	 * 用户查看商品列表
	 * 路由：GET /user/products
	 *
	 * 功能：
	 * 1. 查询所有商品
	 * 2. 如果商品列表为空，显示"无商品可用"的消息
	 * 3. 如果有商品，将商品列表传递给视图
	 * 4. 返回用户商品列表页面
	 *
	 * @return ModelAndView对象，包含商品列表数据和视图名称
	 */
	@GetMapping("/user/products")
	public ModelAndView getproduct() {

		ModelAndView mView = new ModelAndView("uproduct");

		List<Product> products = this.productService.getProducts();

		if(products.isEmpty()) {
			mView.addObject("msg","No products are available");
		}else {
			mView.addObject("products",products);
		}

		return mView;
	}

	/**
	 * 处理新用户注册
	 * 路由：POST /newuserregister
	 *
	 * 功能：
	 * 1. 接收用户注册信息（通过@ModelAttribute自动绑定到User对象）
	 * 2. 检查用户名是否已存在
	 * 3. 用户名不存在：
	 *    - 设置用户角色为ROLE_NORMAL（普通用户）
	 *    - 调用userService.addUser()保存新用户
	 *    - 返回登录页面，提示用户可以登录
	 * 4. 用户名已存在：
	 *    - 返回注册页面
	 *    - 显示错误消息，提示用户名已被占用
	 *
	 * @param user 用户对象，包含注册表单提交的所有信息
	 * @return ModelAndView对象，返回登录页面或注册页面
	 */
	@RequestMapping(value = "newuserregister", method = RequestMethod.POST)
	public ModelAndView newUseRegister(@ModelAttribute User user)
	{
		// Check if username already exists in database
		boolean exists = this.userService.checkUserExists(user.getUsername());

		if(!exists) {
			System.out.println(user.getEmail());
			user.setRole("ROLE_NORMAL");
			this.userService.addUser(user);

			System.out.println("New user created: " + user.getUsername());
			ModelAndView mView = new ModelAndView("userLogin");
			return mView;
		} else {
			System.out.println("New user not created - username taken: " + user.getUsername());
			ModelAndView mView = new ModelAndView("register");
			mView.addObject("msg", user.getUsername() + " is taken. Please choose a different username.");
			return mView;
		}
	}
	
	
	
	// ========================== 学习测试模块 ==========================
	// 以下方法用于演示Spring MVC中Model和ModelAndView的使用方式

	/**
	 * 测试页面1：演示Model的使用
	 * 路由：GET /test
	 *
	 * 功能：用于学习如何使用Model对象向视图传递数据
	 * 演示内容：
	 * 1. 向模型添加简单属性（字符串、整数）
	 * 2. 向模型添加集合对象（List）
	 * 3. 展示如何在视图中访问这些数据
	 *
	 * @param model Spring MVC模型对象，用于向视图传递数据
	 * @return 返回test视图名称
	 */
	@GetMapping("/test")
	public String Test(Model model)
	{
		System.out.println("test page");
		model.addAttribute("author","jay gajera");
		model.addAttribute("id",40);

		List<String> friends = new ArrayList<String>();
		model.addAttribute("f",friends);
		friends.add("xyz");
		friends.add("abc");

		return "test";
	}

	/**
	 * 测试页面2：演示ModelAndView的使用
	 * 路由：GET /test2
	 *
	 * 功能：用于学习如何使用ModelAndView对象
	 * 演示内容：
	 * 1. 创建ModelAndView对象
	 * 2. 使用addObject()方法添加数据到模型
	 * 3. 使用setViewName()方法设置视图名称
	 * 4. 展示如何同时处理数据和视图
	 *
	 * 说明：ModelAndView是Model和View的组合，可以在一个对象中同时设置模型数据和视图名称
	 *
	 * @return ModelAndView对象，包含模型数据和视图名称
	 */
	@GetMapping("/test2")
	public ModelAndView Test2()
	{
		System.out.println("test page");
		//create modelandview object
		ModelAndView mv=new ModelAndView();
		mv.addObject("name","jay gajera 17");
		mv.addObject("id",40);
		mv.setViewName("test2");

		List<Integer> list=new ArrayList<Integer>();
		list.add(10);
		list.add(25);
		mv.addObject("marks",list);
		return mv;


	}


	// ========================== 待实现功能 ==========================
	// 以下是购物车功能的预留代码，尚未实现

//	@GetMapping("carts")
//	public ModelAndView  getCartDetail()
//	{
//		ModelAndView mv= new ModelAndView();
//		List<Cart>carts = cartService.getCarts();
//	}
	  
}
