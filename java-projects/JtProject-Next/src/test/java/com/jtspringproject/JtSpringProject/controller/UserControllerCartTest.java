package com.jtspringproject.JtSpringProject.controller;

import com.jtspringproject.JtSpringProject.dao.CartProductDao;
import com.jtspringproject.JtSpringProject.models.Cart;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.models.User;
import com.jtspringproject.JtSpringProject.services.CartService;
import com.jtspringproject.JtSpringProject.services.ProductService;
import com.jtspringproject.JtSpringProject.services.UserService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentMatchers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class UserControllerCartTest {

    @InjectMocks
    private UserController userController;

    @Mock
    private UserService userService;

    @Mock
    private ProductService productService;

    @Mock
    private CartService cartService;

    @Mock
    private CartProductDao cartProductDao;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(userController, "userService", userService);
        ReflectionTestUtils.setField(userController, "productService", productService);
        ReflectionTestUtils.setField(userController, "cartService", cartService);
        ReflectionTestUtils.setField(userController, "cartProductDao", cartProductDao);
    }

    @Test
    void addToCart_shouldRequireLogin_whenNoUsernameCookie() {
        MockHttpServletRequest request = new MockHttpServletRequest();

        String result = userController.addToCart(1, request);

        assertEquals("redirect:/user/products", result);
        assertEquals("Please login first", request.getSession().getAttribute("cartMsg"));
        verify(cartProductDao, never()).addCartProduct(ArgumentMatchers.any());
    }

    @Test
    void addToCart_shouldAddProduct_whenUserAndProductAreValid() {
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setCookies(new javax.servlet.http.Cookie("username", "lisa"));

        User user = new User();
        user.setId(10);
        user.setUsername("lisa");
        user.setRole("ROLE_NORMAL");

        Cart cart = new Cart();
        cart.setId(20);
        cart.setCustomer(user);

        Product product = new Product();
        product.setId(30);

        when(userService.getUserByUsername("lisa")).thenReturn(user);
        when(cartService.getCarts()).thenReturn(List.of(cart));
        when(productService.getProduct(30)).thenReturn(product);

        String result = userController.addToCart(30, request);

        assertEquals("redirect:/user/cart", result);
        assertEquals("Add Success", request.getSession().getAttribute("cartMsg"));
        verify(cartProductDao).addCartProduct(ArgumentMatchers.any());
    }

    @Test
    void addToCart_shouldHandleMissingProduct() {
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.setCookies(new javax.servlet.http.Cookie("username", "lisa"));

        User user = new User();
        user.setId(10);
        user.setUsername("lisa");
        user.setRole("ROLE_NORMAL");

        when(userService.getUserByUsername("lisa")).thenReturn(user);
        when(cartService.getCarts()).thenReturn(Collections.emptyList());

        Cart createdCart = new Cart();
        createdCart.setId(99);
        createdCart.setCustomer(user);

        when(cartService.addCart(ArgumentMatchers.any(Cart.class))).thenReturn(createdCart);
        when(productService.getProduct(404)).thenReturn(null);

        String result = userController.addToCart(404, request);

        assertEquals("redirect:/user/products", result);
        assertEquals("Product not found", request.getSession().getAttribute("cartMsg"));
        verify(cartProductDao, never()).addCartProduct(ArgumentMatchers.any());
    }
}
