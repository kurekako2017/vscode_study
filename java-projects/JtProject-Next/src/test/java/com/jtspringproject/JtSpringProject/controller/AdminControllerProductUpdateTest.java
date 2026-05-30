package com.jtspringproject.JtSpringProject.controller;

import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.services.CategoryService;
import com.jtspringproject.JtSpringProject.services.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.test.util.ReflectionTestUtils;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AdminControllerProductUpdateTest {

    @InjectMocks
    private AdminController adminController;

    @Mock
    private ProductService productService;

    @Mock
    private CategoryService categoryService;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(adminController, "productService", productService);
        ReflectionTestUtils.setField(adminController, "categoryService", categoryService);
    }

    @Test
    void updateProduct_shouldKeepOldImage_whenImageParamIsBlank() {
        int productId = 1;
        int categoryId = 2;

        Category category = new Category();
        category.setId(categoryId);

        Product existingProduct = new Product();
        existingProduct.setId(productId);
        existingProduct.setImage("old-image.png");

        when(categoryService.getCategory(categoryId)).thenReturn(category);
        when(productService.getProduct(productId)).thenReturn(existingProduct);

        String result = adminController.updateProduct(
                productId,
                "Updated Name",
                categoryId,
                100,
                200,
                10,
                "Updated Desc",
                ""
        );

        ArgumentCaptor<Product> productCaptor = ArgumentCaptor.forClass(Product.class);
        verify(productService).updateProduct(eq(productId), productCaptor.capture());

        Product updated = productCaptor.getValue();
        assertEquals("Updated Name", updated.getName());
        assertEquals(categoryId, updated.getCategory().getId());
        assertEquals(100, updated.getPrice());
        assertEquals(200, updated.getWeight());
        assertEquals(10, updated.getQuantity());
        assertEquals("Updated Desc", updated.getDescription());
        assertEquals("old-image.png", updated.getImage());
        assertEquals("redirect:/admin/products", result);
    }

    @Test
    void logout_shouldRedirectToRoot() {
        MockHttpServletResponse response = new MockHttpServletResponse();
        MockHttpServletRequest request = new MockHttpServletRequest();
        UserController userController = new UserController();

        String result = userController.logout(response, request);

        assertEquals("redirect:/", result);
    }
}
