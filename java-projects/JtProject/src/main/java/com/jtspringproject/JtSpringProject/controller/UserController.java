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
     */
    @GetMapping("/register")
    public String registerUser()
    {
        return "register";
    }

    @GetMapping("/buy")
    public String buy()
    {
        return "buy";
    }


    @GetMapping("/")
    public String userlogin(Model model) {

        return "userLogin";
    }

    /**
     * 用户登录验证
     * 路由：POST /userloginvalidate
     *
     * 说明：此方法已增强空值检查和异常处理，避免常见的 NullPointerException
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

        try {
            // 调用 Service 层验证用户登录
            // 流程: Controller → UserService → UserDao → 数据库
            User u = this.userService.checkLogin(username, pass);

            // 防御性检查：Service/DAO不应该返回 null（实现中返回 new User() 表示未找到），
            // 但为了健壮性，我们仍然要做 null 检查，防止注入失败或其他异常情况导致 NPE。
            if (u == null) {
                // u 为 null，记录并返回登录页（友好提示）
                System.err.println("登录异常：userService.checkLogin 返回 null（预期应返回 User 或 空 User 对象）");
                ModelAndView mView = new ModelAndView("userLogin");
                mView.addObject("msg", "系统错误：无法验证用户，请联系管理员（user=null）");
                return mView;
            }

            // 输出从数据库（DAO）返回的用户名，可能为 null（表示未找到或空 User）
            System.out.println("数据库查询结果 - 用户名: " + u.getUsername());

            // ===================== 用户名比较（登录成功判断） =====================
            // 这里需要判断表单提交的 username（页面上的值）和从数据库查到的 u.getUsername()（数据库中的值）是否一致
            // 原始做法是: if(username.equals(u.getUsername())) { ... }
            // 说明：如果 u.getUsername() 为 null，会导致 NullPointerException 在 username.equals(...) 中并不会发生（因为 equals 在 username 上）
            // 但更安全的是使用 java.util.Objects.equals(a, b) 做空安全比较，或者先检查 u.getUsername() 是否为 null。
            // 下面我们使用 Objects.equals 做空安全比较，并在必要时通过 u.getId() 判断是否存在用户。

            // 如果 DAO 的约定是：查询不到用户返回 new User()（id=0），则可以优先用 id 判断
            if (u.getId() > 0 && java.util.Objects.equals(username, u.getUsername())) {
                // ✅ 登录成功的处理逻辑

                // 1. 创建Cookie保存用户名（用于客户端会话管理）
                res.addCookie(new Cookie("username", u.getUsername()));

                // 2. 创建 ModelAndView，指定返回首页视图
                ModelAndView mView  = new ModelAndView("index");

                // 3. 将用户对象添加到模型中（视图可以访问用户信息）
                mView.addObject("user", u);

                // 4. 查询所有商品列表（用于首页展示）
                List<Product> products = null;
                try {
                    products = this.productService.getProducts();
                } catch (Exception e) {
                    // 如果 productService 出现异常，不要让整个登录流程崩溃，记录并继续返回空列表提示
                    System.err.println("获取商品列表时出错: " + e.getMessage());
                }

                // 5. 判断商品列表是否为空（注意：products 可能为 null）
                if (products == null || products.isEmpty()) {
                    // 商品列表为空或未获取到，添加提示信息
                    mView.addObject("msg", "No products are available");
                } else {
                    // 商品列表不为空，将商品数据传递到视图
                    mView.addObject("products", products);
                }

                // 6. 返回 ModelAndView（会渲染 index.jsp 页面）
                return mView;

            } else {
                // ❌ 登录失败的处理逻辑
                // 可能原因：用户名不存在（u.id==0）或密码错误（实现中会返回空User）

                ModelAndView mView = new ModelAndView("userLogin");

                // 给用户一个通用的错误提示（不要暴露是用户名不存在还是密码错误）
                mView.addObject("msg", "Please enter correct email and password");

                return mView;
            }

        } catch (Exception ex) {
            // 捕获任何意外异常，避免抛出到容器导致 500 错误页面不可读
            ex.printStackTrace();
            ModelAndView mView = new ModelAndView("userLogin");
            mView.addObject("msg", "系统异常：" + ex.getMessage());
            return mView;
        }
    }


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

}
