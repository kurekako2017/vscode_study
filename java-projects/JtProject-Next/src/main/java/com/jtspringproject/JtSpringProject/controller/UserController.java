package com.jtspringproject.JtSpringProject.controller;

import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.http.HttpServletRequest;

import com.jtspringproject.JtSpringProject.common.constants.RoleConstants;
import com.jtspringproject.JtSpringProject.common.constants.SessionConstants;
import com.jtspringproject.JtSpringProject.common.util.InputCheckUtil;
import com.jtspringproject.JtSpringProject.common.util.TypeConversionUtil;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.User;
import com.jtspringproject.JtSpringProject.models.Cart;
import com.jtspringproject.JtSpringProject.models.CartProduct;
import com.jtspringproject.JtSpringProject.services.ProductService;
import com.jtspringproject.JtSpringProject.services.UserService;
import com.jtspringproject.JtSpringProject.services.CartService;
import com.jtspringproject.JtSpringProject.dao.CartProductDao;


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

    @Autowired
    private CartService cartService;

    @Autowired
    private CartProductDao cartProductDao;

    private String resolveLoggedInUsername(HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            String username = TypeConversionUtil.toTrimmedString(session.getAttribute(SessionConstants.USERNAME));
            if (InputCheckUtil.hasText(username)) {
                return username;
            }
        }
        if (request.getCookies() != null) {
            for (javax.servlet.http.Cookie c : request.getCookies()) {
                String cookieValue = TypeConversionUtil.toTrimmedString(c.getValue());
                if (SessionConstants.USERNAME.equals(c.getName()) && InputCheckUtil.hasText(cookieValue)) {
                    request.getSession().setAttribute(SessionConstants.USERNAME, cookieValue);
                    return cookieValue;
                }
            }
        }
        return null;
    }

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
    public ModelAndView userloginPage(HttpServletRequest request) {
        ModelAndView mView = new ModelAndView("userLogin");
        // 如果已登录，自动注入商品列表
        String username = resolveLoggedInUsername(request);
        try {
            List<Product> products = this.productService.getProducts();
            if (InputCheckUtil.hasItems(products)) {
                mView.addObject("products", products);
            }
        } catch (Exception e) {
            mView.addObject("msg", "Error loading products: " + e.getMessage());
        }
        if (username != null) {
            mView.addObject("username", username);
        }
        return mView;
    }

    @GetMapping("/logout")
    public String logout(HttpServletResponse response, HttpServletRequest request) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }
        Cookie cookie = new Cookie(SessionConstants.USERNAME, "");
        cookie.setPath("/");
        cookie.setMaxAge(0);
        response.addCookie(cookie);
        return "redirect:/";
    }

    /**
     * 用户登录验证
     * 路由：POST /userloginvalidate
     *
     * 说明：此方法已增强空值检查和异常处理，避免常见的 NullPointerException
     */
    @RequestMapping(value = "userloginvalidate1", method = RequestMethod.POST)
    public ModelAndView userlogin(
            @RequestParam("username") String username,
            @RequestParam("password") String pass,
            Model model,
            HttpServletResponse res,
            HttpServletRequest request) {

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
                Cookie cookie = new Cookie(SessionConstants.USERNAME, u.getUsername());
                cookie.setPath("/");
                cookie.setMaxAge(7 * 24 * 60 * 60);
                res.addCookie(cookie);
                request.getSession().setAttribute(SessionConstants.USERNAME, u.getUsername());
                request.getSession().setAttribute(SessionConstants.USER_ROLE, u.getRole());

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
                if (!InputCheckUtil.hasItems(products)) {
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

    /**
     * 兼容旧的表单 action: POST /userloginvalidate
     * 直接委托到 userlogin(...) 处理，避免前端 action 名称差异导致登录失败。
     */
    @RequestMapping(value = "userloginvalidate", method = RequestMethod.POST)
    public ModelAndView userloginAlias(
            @RequestParam("username") String username,
            @RequestParam("password") String pass,
            Model model,
            HttpServletResponse res,
            HttpServletRequest request) {
        return userlogin(username, pass, model, res, request);
    }


    @GetMapping("/user/products")
    public ModelAndView getproduct() {

        ModelAndView mView = new ModelAndView("uproduct");

        List<Product> products = this.productService.getProducts();

        if(!InputCheckUtil.hasItems(products)) {
            mView.addObject("msg","No products are available");
        }else {
            mView.addObject("products",products);
        }

        return mView;
    }

    /**
     * 首页（可通过 GET /index 访问）
     * 如果用户已登录（通过 cookie username 判断），将 username 和 products 注入视图
     */
    @GetMapping({"/index"})
    public ModelAndView indexPage(HttpServletRequest request) {
        ModelAndView mView = new ModelAndView("index");
        String username = resolveLoggedInUsername(request);
        if (username != null) {
            mView.addObject("username", username);
        }
        try {
            List<Product> products = this.productService.getProducts();
            if (!InputCheckUtil.hasItems(products)) {
                mView.addObject("msg", "No products are available");
            } else {
                mView.addObject("products", products);
            }
        } catch (Exception e) {
            mView.addObject("msg", "Error loading products: " + e.getMessage());
        }
        return mView;
    }

    @RequestMapping(value = "newuserregister", method = RequestMethod.POST)
    public ModelAndView newUseRegister(@ModelAttribute User user)
    {
        String username = InputCheckUtil.trimToNull(user.getUsername());
        String email = InputCheckUtil.trimToNull(user.getEmail());
        String password = InputCheckUtil.trimToNull(user.getPassword());

        if (!InputCheckUtil.hasText(username) || !InputCheckUtil.hasText(email) || !InputCheckUtil.hasText(password)) {
            ModelAndView mView = new ModelAndView("register");
            mView.addObject("msg", "Username, email and password are required.");
            return mView;
        }

        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(password);
        user.setAddress(InputCheckUtil.trimToEmpty(user.getAddress()));

        // Check if username already exists in database
        boolean exists = this.userService.checkUserExists(user.getUsername());

        if(!exists) {
            System.out.println(user.getEmail());
            user.setRole(RoleConstants.ROLE_NORMAL);
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

    @RequestMapping(value = "products/addtocart", method = {RequestMethod.GET, RequestMethod.POST})
    public String addToCart(@RequestParam("id") int id, HttpServletRequest request) {
        try {
            // 1. 获取当前登录用户名（从 cookie 或 session）
            String username = resolveLoggedInUsername(request);
            if (username == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Please login first");
                return "redirect:/user/products";
            }
            // 2. 查找用户对象
            User user = this.userService.getUserByUsername(username);
            if (user == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "User not found, please login again");
                return "redirect:/user/products";
            }
            // 如果是管理员，不允许作为普通用户加入购物车，重定向到管理员商品管理页面
            if (RoleConstants.isAdmin(user.getRole())) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "管理员请使用后台管理商品。");
                return "redirect:/admin/products";
            }
            // 3. 查找该用户的购物车（如无则新建）
            java.util.List<Cart> allCarts = this.cartService.getCarts();
            Cart cart = null;
            for (Cart c : allCarts) {
                if (c.getCustomer() != null && c.getCustomer().getId() == user.getId()) {
                    cart = c;
                    break;
                }
            }
            if (cart == null) {
                cart = new Cart();
                cart.setCustomer(user);
                cart = this.cartService.addCart(cart);
            }
            // 4. 添加商品到购物车
            Product product = this.productService.getProduct(id);
            if (product == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Product not found");
                return "redirect:/user/products";
            }
            CartProduct cp = new CartProduct(cart, product);
            this.cartProductDao.addCartProduct(cp);
            request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Add Success");
        } catch (Exception e) {
            e.printStackTrace();
            request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Add failed: " + e.getMessage());
        }
        // 添加后直接跳转到购物车页面
        return "redirect:/user/cart";
    }

    @GetMapping("/user/cart")
    public ModelAndView showCart(HttpServletRequest request) {
        ModelAndView mView = new ModelAndView("cart");
        String username = resolveLoggedInUsername(request);
        if (username == null) {
            mView.addObject("msg", "Please login first");
            return mView;
        }
        User user = this.userService.getUserByUsername(username);
        if (user == null) {
            mView.addObject("msg", "User not found");
            return mView;
        }
        // 管理员不使用购物车，重定向到管理员商品管理页
        if (RoleConstants.isAdmin(user.getRole())) {
            ModelAndView redirect = new ModelAndView("redirect:/admin/products");
            redirect.addObject("msg", "管理员请使用后台管理商品。");
            return redirect;
        }
        java.util.List<Cart> allCarts = this.cartService.getCarts();
        Cart cart = null;
        for (Cart c : allCarts) {
            if (c.getCustomer() != null && c.getCustomer().getId() == user.getId()) {
                cart = c;
                break;
            }
        }
        java.util.List<Product> cartProducts = new java.util.ArrayList<>();
        if (cart != null) {
            // 获取购物车内所有商品
            cartProducts = this.cartProductDao.getProductByCartID(cart.getId());
        }
        mView.addObject("products", cartProducts);
        Object cartMsg = request.getSession().getAttribute(SessionConstants.CART_MESSAGE);
        if (cartMsg != null) {
            mView.addObject("cartMsg", cartMsg.toString());
            request.getSession().removeAttribute(SessionConstants.CART_MESSAGE);
        }
        return mView;
    }

    @GetMapping("/user/cart/delete")
    public String deleteFromCart(@RequestParam("id") int productId, HttpServletRequest request) {
        try {
            String username = resolveLoggedInUsername(request);

            if (username == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Please login first");
                return "redirect:/";
            }

            User user = this.userService.getUserByUsername(username);
            if (user == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "User not found");
                return "redirect:/";
            }

            java.util.List<Cart> allCarts = this.cartService.getCarts();
            Cart cart = null;
            for (Cart c : allCarts) {
                if (c.getCustomer() != null && c.getCustomer().getId() == user.getId()) {
                    cart = c;
                    break;
                }
            }
            if (cart == null) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Cart not found");
                return "redirect:/user/cart";
            }

            java.util.List<CartProduct> cartProducts = this.cartProductDao.getCartProductsByCartAndProductId(cart.getId(), productId);
            if (!InputCheckUtil.hasItems(cartProducts)) {
                request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Product not found in cart");
                return "redirect:/user/cart";
            }

            this.cartProductDao.deleteCartProduct(cartProducts.get(0));
            request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Delete Success");
        } catch (Exception e) {
            e.printStackTrace();
            request.getSession().setAttribute(SessionConstants.CART_MESSAGE, "Delete failed: " + e.getMessage());
        }
        return "redirect:/user/cart";
    }

}
