package com.jtspringproject.JtSpringProject.controller;

import com.jtspringproject.JtSpringProject.common.constants.RoleConstants;
import com.jtspringproject.JtSpringProject.common.constants.SessionConstants;
import com.jtspringproject.JtSpringProject.common.util.InputCheckUtil;
import com.jtspringproject.JtSpringProject.common.util.TypeConversionUtil;
import com.jtspringproject.JtSpringProject.dao.CartProductDao;
import com.jtspringproject.JtSpringProject.models.Cart;
import com.jtspringproject.JtSpringProject.models.CartProduct;
import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.User;
import com.jtspringproject.JtSpringProject.services.CartService;
import com.jtspringproject.JtSpringProject.services.CategoryService;
import com.jtspringproject.JtSpringProject.services.ProductService;
import com.jtspringproject.JtSpringProject.services.UserService;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin(
        origins = {
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:5177",
            "http://127.0.0.1:5177"
        },
        allowCredentials = "true")
public class ApiController {

    @Autowired private UserService userService;
    @Autowired private ProductService productService;
    @Autowired private CategoryService categoryService;
    @Autowired private CartService cartService;
    @Autowired private CartProductDao cartProductDao;

    @GetMapping("/health")
    public Map<String, Object> health() {
        return ok("JtProject Spring Boot + TypeScript API is running", "ok");
    }

    @GetMapping("/session")
    public Map<String, Object> session(HttpServletRequest request) {
        return ok("Session loaded", sessionData(request));
    }

    @PostMapping("/auth/login")
    public ResponseEntity<Map<String, Object>> userLogin(
            @RequestBody LoginBody body,
            HttpServletRequest request,
            HttpServletResponse response) {
        String username = InputCheckUtil.trimToNull(body.username);
        String password = InputCheckUtil.trimToNull(body.password);
        if (!InputCheckUtil.hasText(username) || !InputCheckUtil.hasText(password)) {
            return badRequest("Username and password are required.");
        }
        User user = userService.checkLogin(username, password);
        if (user == null || user.getId() <= 0 || !RoleConstants.isNormalUser(user.getRole())) {
            return unauthorized("Invalid user credentials.");
        }
        signInUser(user, request, response);
        return ResponseEntity.ok(ok("User login successful.", sessionData(request)));
    }

    @PostMapping("/auth/register")
    public ResponseEntity<Map<String, Object>> register(
            @RequestBody RegisterBody body,
            HttpServletRequest request,
            HttpServletResponse response) {
        String username = InputCheckUtil.trimToNull(body.username);
        String email = InputCheckUtil.trimToNull(body.email);
        String password = InputCheckUtil.trimToNull(body.password);
        String address = InputCheckUtil.trimToEmpty(body.address);
        if (!InputCheckUtil.hasText(username) || !InputCheckUtil.hasText(email) || !InputCheckUtil.hasText(password)) {
            return badRequest("Username, email and password are required.");
        }
        if (userService.checkUserExists(username)) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(fail("Username already exists."));
        }
        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(password);
        user.setAddress(address);
        user.setRole(RoleConstants.ROLE_NORMAL);
        userService.addUser(user);
        signInUser(userService.getUserByUsername(username), request, response);
        return ResponseEntity.status(HttpStatus.CREATED).body(ok("Registration successful.", sessionData(request)));
    }

    @PostMapping("/auth/logout")
    public Map<String, Object> userLogout(HttpServletRequest request, HttpServletResponse response) {
        HttpSession session = request.getSession();
        session.removeAttribute(SessionConstants.USERNAME);
        session.removeAttribute(SessionConstants.USER_ROLE);
        Cookie cookie = new Cookie(SessionConstants.USERNAME, "");
        cookie.setPath("/");
        cookie.setMaxAge(0);
        response.addCookie(cookie);
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("authenticated", false);
        data.put("username", "");
        data.put("role", "");
        data.put("adminLoggedIn", isAdminLoggedIn(session));
        data.put("adminUsername", adminUsername(session));
        return ok("User logout successful.", data);
    }

    @GetMapping("/products")
    public Map<String, Object> products() {
        return ok("Products loaded.", productMaps(productService.getProducts()));
    }

    @GetMapping("/categories")
    public Map<String, Object> categories() {
        return ok("Categories loaded.", categoryMaps(categoryService.getCategories()));
    }

    @GetMapping("/cart")
    public ResponseEntity<Map<String, Object>> cart(HttpServletRequest request) {
        User user = resolveCurrentUser(request);
        if (user == null || !RoleConstants.isNormalUser(user.getRole())) {
            return unauthorized("Please login as a normal user first.");
        }
        Cart cart = getOrCreateCart(user);
        return ResponseEntity.ok(ok("Cart loaded.", productMaps(cartProductDao.getProductByCartID(cart.getId()))));
    }

    @PostMapping("/cart/items/{productId}")
    public ResponseEntity<Map<String, Object>> addCartItem(@PathVariable int productId, HttpServletRequest request) {
        User user = resolveCurrentUser(request);
        if (user == null || !RoleConstants.isNormalUser(user.getRole())) {
            return unauthorized("Please login as a normal user first.");
        }
        Product product = productService.getProduct(productId);
        if (product == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(fail("Product not found."));
        }
        Cart cart = getOrCreateCart(user);
        cartProductDao.addCartProduct(new CartProduct(cart, product));
        return ResponseEntity.ok(ok("Product added to cart.", productMaps(cartProductDao.getProductByCartID(cart.getId()))));
    }

    @DeleteMapping("/cart/items/{productId}")
    public ResponseEntity<Map<String, Object>> deleteCartItem(@PathVariable int productId, HttpServletRequest request) {
        User user = resolveCurrentUser(request);
        if (user == null || !RoleConstants.isNormalUser(user.getRole())) {
            return unauthorized("Please login as a normal user first.");
        }
        Cart cart = findCartByUser(user);
        if (cart == null) {
            return ResponseEntity.ok(ok("Cart is already empty.", new ArrayList<>()));
        }
        List<CartProduct> items = cartProductDao.getCartProductsByCartAndProductId(cart.getId(), productId);
        if (!InputCheckUtil.hasItems(items)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(fail("Product was not found in the cart."));
        }
        cartProductDao.deleteCartProduct(items.get(0));
        return ResponseEntity.ok(ok("Product removed from cart.", productMaps(cartProductDao.getProductByCartID(cart.getId()))));
    }

    @PostMapping("/admin/login")
    public ResponseEntity<Map<String, Object>> adminLogin(@RequestBody LoginBody body, HttpServletRequest request) {
        String username = InputCheckUtil.trimToNull(body.username);
        String password = InputCheckUtil.trimToNull(body.password);
        if (!InputCheckUtil.hasText(username) || !InputCheckUtil.hasText(password)) {
            return badRequest("Username and password are required.");
        }
        User user = userService.checkLogin(username, password);
        if (user == null || user.getId() <= 0 || !RoleConstants.isAdmin(user.getRole())) {
            return unauthorized("Invalid admin credentials.");
        }
        HttpSession session = request.getSession();
        session.setAttribute(SessionConstants.ADMIN_LOGGED_IN, true);
        session.setAttribute(SessionConstants.ADMIN_USERNAME, user.getUsername());
        return ResponseEntity.ok(ok("Admin login successful.", sessionData(request)));
    }

    @PostMapping("/admin/logout")
    public Map<String, Object> adminLogout(HttpServletRequest request) {
        HttpSession session = request.getSession();
        session.removeAttribute(SessionConstants.ADMIN_LOGGED_IN);
        session.removeAttribute(SessionConstants.ADMIN_USERNAME);
        return ok("Admin logout successful.", sessionData(request));
    }

    @GetMapping("/admin/overview")
    public ResponseEntity<Map<String, Object>> adminOverview(HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("categoryCount", categoryService.getCategories().size());
        data.put("productCount", productService.getProducts().size());
        data.put("customerCount", userService.getUsers().size());
        data.put("adminUsername", adminUsername(request.getSession()));
        return ResponseEntity.ok(ok("Admin overview loaded.", data));
    }

    @GetMapping("/admin/categories")
    public ResponseEntity<Map<String, Object>> adminCategories(HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        return ResponseEntity.ok(ok("Categories loaded.", categoryMaps(categoryService.getCategories())));
    }

    @PostMapping("/admin/categories")
    public ResponseEntity<Map<String, Object>> createCategory(@RequestBody CategoryBody body, HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        String name = InputCheckUtil.trimToNull(body.name);
        if (!InputCheckUtil.hasText(name)) {
            return badRequest("Category name is required.");
        }
        categoryService.addCategory(name);
        return ResponseEntity.status(HttpStatus.CREATED).body(ok("Category created.", categoryMaps(categoryService.getCategories())));
    }

    @PutMapping("/admin/categories/{id}")
    public ResponseEntity<Map<String, Object>> updateCategory(
            @PathVariable int id,
            @RequestBody CategoryBody body,
            HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        String name = InputCheckUtil.trimToNull(body.name);
        if (!InputCheckUtil.hasText(name)) {
            return badRequest("Category name is required.");
        }
        categoryService.updateCategory(id, name);
        return ResponseEntity.ok(ok("Category updated.", categoryMaps(categoryService.getCategories())));
    }

    @DeleteMapping("/admin/categories/{id}")
    public ResponseEntity<Map<String, Object>> deleteCategory(@PathVariable int id, HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        categoryService.deleteCategory(id);
        return ResponseEntity.ok(ok("Category deleted.", categoryMaps(categoryService.getCategories())));
    }

    @GetMapping("/admin/products")
    public ResponseEntity<Map<String, Object>> adminProducts(HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        return ResponseEntity.ok(ok("Products loaded.", productMaps(productService.getProducts())));
    }

    @PostMapping("/admin/products")
    public ResponseEntity<Map<String, Object>> createProduct(@RequestBody ProductBody body, HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        ResponseEntity<Map<String, Object>> invalid = validateProductBody(body);
        if (invalid != null) {
            return invalid;
        }
        productService.addProduct(copyProduct(new Product(), body));
        return ResponseEntity.status(HttpStatus.CREATED).body(ok("Product created.", productMaps(productService.getProducts())));
    }

    @PutMapping("/admin/products/{id}")
    public ResponseEntity<Map<String, Object>> updateProduct(
            @PathVariable int id,
            @RequestBody ProductBody body,
            HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        Product existing = productService.getProduct(id);
        if (existing == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(fail("Product not found."));
        }
        ResponseEntity<Map<String, Object>> invalid = validateProductBody(body);
        if (invalid != null) {
            return invalid;
        }
        productService.updateProduct(id, copyProduct(existing, body));
        return ResponseEntity.ok(ok("Product updated.", productMaps(productService.getProducts())));
    }

    @DeleteMapping("/admin/products/{id}")
    public ResponseEntity<Map<String, Object>> deleteProduct(@PathVariable int id, HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        productService.deleteProduct(id);
        return ResponseEntity.ok(ok("Product deleted.", productMaps(productService.getProducts())));
    }

    @GetMapping("/admin/customers")
    public ResponseEntity<Map<String, Object>> customers(HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        return ResponseEntity.ok(ok("Customers loaded.", userMaps(userService.getUsers())));
    }

    @GetMapping("/admin/profile")
    public ResponseEntity<Map<String, Object>> adminProfile(HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        User user = userService.getUserByUsername(adminUsername(request.getSession()));
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(fail("Admin user not found."));
        }
        return ResponseEntity.ok(ok("Admin profile loaded.", userMap(user)));
    }

    @PutMapping("/admin/profile")
    public ResponseEntity<Map<String, Object>> updateAdminProfile(@RequestBody RegisterBody body, HttpServletRequest request) {
        if (!isAdminLoggedIn(request.getSession())) {
            return unauthorized("Please login as admin first.");
        }
        User user = userService.getUserByUsername(adminUsername(request.getSession()));
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(fail("Admin user not found."));
        }
        String username = InputCheckUtil.trimToNull(body.username);
        String email = InputCheckUtil.trimToNull(body.email);
        String password = InputCheckUtil.trimToNull(body.password);
        String address = InputCheckUtil.trimToEmpty(body.address);
        if (!InputCheckUtil.hasText(username) || !InputCheckUtil.hasText(email) || !InputCheckUtil.hasText(password)) {
            return badRequest("Username, email and password are required.");
        }
        User duplicate = userService.getUserByUsername(username);
        if (duplicate != null && duplicate.getId() != user.getId()) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(fail("Username already exists."));
        }
        user.setUsername(username);
        user.setEmail(email);
        user.setPassword(password);
        user.setAddress(address);
        userService.addUser(user);
        request.getSession().setAttribute(SessionConstants.ADMIN_USERNAME, username);
        return ResponseEntity.ok(ok("Admin profile updated.", userMap(user)));
    }

    private ResponseEntity<Map<String, Object>> validateProductBody(ProductBody body) {
        if (!InputCheckUtil.hasText(InputCheckUtil.trimToNull(body.name))) {
            return badRequest("Product name is required.");
        }
        if (categoryService.getCategory(body.categoryId) == null) {
            return badRequest("Category not found.");
        }
        return null;
    }

    private Product copyProduct(Product target, ProductBody body) {
        target.setName(InputCheckUtil.trimToEmpty(body.name));
        target.setCategory(categoryService.getCategory(body.categoryId));
        target.setPrice(body.price);
        target.setWeight(body.weight);
        target.setQuantity(body.quantity);
        target.setDescription(InputCheckUtil.trimToEmpty(body.description));
        target.setImage(InputCheckUtil.trimToEmpty(body.image));
        return target;
    }

    private void signInUser(User user, HttpServletRequest request, HttpServletResponse response) {
        HttpSession session = request.getSession();
        session.setAttribute(SessionConstants.USERNAME, user.getUsername());
        session.setAttribute(SessionConstants.USER_ROLE, user.getRole());
        Cookie cookie = new Cookie(SessionConstants.USERNAME, user.getUsername());
        cookie.setPath("/");
        cookie.setMaxAge(7 * 24 * 60 * 60);
        response.addCookie(cookie);
    }

    private User resolveCurrentUser(HttpServletRequest request) {
        String username = TypeConversionUtil.toTrimmedString(request.getSession().getAttribute(SessionConstants.USERNAME));
        if (!InputCheckUtil.hasText(username) && request.getCookies() != null) {
            for (Cookie cookie : request.getCookies()) {
                if (SessionConstants.USERNAME.equals(cookie.getName()) && InputCheckUtil.hasText(cookie.getValue())) {
                    username = cookie.getValue().trim();
                    request.getSession().setAttribute(SessionConstants.USERNAME, username);
                    break;
                }
            }
        }
        return InputCheckUtil.hasText(username) ? userService.getUserByUsername(username) : null;
    }

    private boolean isAdminLoggedIn(HttpSession session) {
        return Boolean.TRUE.equals(session.getAttribute(SessionConstants.ADMIN_LOGGED_IN));
    }

    private String adminUsername(HttpSession session) {
        String value = TypeConversionUtil.toTrimmedString(session.getAttribute(SessionConstants.ADMIN_USERNAME));
        return value == null ? "" : value;
    }

    private Cart getOrCreateCart(User user) {
        Cart cart = findCartByUser(user);
        if (cart != null) {
            return cart;
        }
        Cart created = new Cart();
        created.setCustomer(user);
        return cartService.addCart(created);
    }

    private Cart findCartByUser(User user) {
        for (Cart cart : cartService.getCarts()) {
            if (cart.getCustomer() != null && cart.getCustomer().getId() == user.getId()) {
                return cart;
            }
        }
        return null;
    }

    private Map<String, Object> sessionData(HttpServletRequest request) {
        User user = resolveCurrentUser(request);
        HttpSession session = request.getSession();
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("authenticated", user != null);
        data.put("username", user != null ? user.getUsername() : "");
        data.put("role", user != null ? user.getRole() : "");
        data.put("adminLoggedIn", isAdminLoggedIn(session));
        data.put("adminUsername", adminUsername(session));
        return data;
    }

    private List<Map<String, Object>> productMaps(List<Product> products) {
        List<Map<String, Object>> items = new ArrayList<>();
        if (products == null) {
            return items;
        }
        for (Product product : products) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", product.getId());
            item.put("name", product.getName());
            item.put("image", product.getImage());
            item.put("price", product.getPrice());
            item.put("weight", product.getWeight());
            item.put("quantity", product.getQuantity());
            item.put("description", product.getDescription());
            item.put("categoryId", product.getCategory() != null ? product.getCategory().getId() : 0);
            item.put("categoryName", product.getCategory() != null ? product.getCategory().getName() : "");
            items.add(item);
        }
        return items;
    }

    private List<Map<String, Object>> categoryMaps(List<Category> categories) {
        List<Map<String, Object>> items = new ArrayList<>();
        if (categories == null) {
            return items;
        }
        for (Category category : categories) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", category.getId());
            item.put("name", category.getName());
            items.add(item);
        }
        return items;
    }

    private List<Map<String, Object>> userMaps(List<User> users) {
        List<Map<String, Object>> items = new ArrayList<>();
        if (users == null) {
            return items;
        }
        for (User user : users) {
            items.add(userMap(user));
        }
        return items;
    }

    private Map<String, Object> userMap(User user) {
        Map<String, Object> item = new LinkedHashMap<>();
        item.put("id", user.getId());
        item.put("username", user.getUsername());
        item.put("email", user.getEmail());
        item.put("role", user.getRole());
        item.put("address", user.getAddress());
        item.put("password", user.getPassword());
        return item;
    }

    private Map<String, Object> ok(String message, Object data) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("success", true);
        result.put("message", message);
        result.put("data", data);
        return result;
    }

    private Map<String, Object> fail(String message) {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("success", false);
        result.put("message", message);
        return result;
    }

    private ResponseEntity<Map<String, Object>> badRequest(String message) {
        return ResponseEntity.badRequest().body(fail(message));
    }

    private ResponseEntity<Map<String, Object>> unauthorized(String message) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(fail(message));
    }

    public static class LoginBody {
        public String username;
        public String password;
    }

    public static class RegisterBody {
        public String username;
        public String email;
        public String password;
        public String address;
    }

    public static class CategoryBody {
        public String name;
    }

    public static class ProductBody {
        public String name;
        public int categoryId;
        public int price;
        public int weight;
        public int quantity;
        public String description;
        public String image;
    }
}
