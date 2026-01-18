package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.CartProduct;
import com.jtspringproject.JtSpringProject.models.Product;
import java.util.List;

/**
 * 购物车商品数据访问接口
 * 定义购物车商品数据库操作的契约
 */
public interface CartProductDao {
    
    /**
     * 添加购物车商品
     * @param cartProduct 购物车商品对象
     * @return 添加后的购物车商品
     */
    CartProduct addCartProduct(CartProduct cartProduct);
    
    /**
     * 获取所有购物车商品
     * @return 购物车商品列表
     */
    List<CartProduct> getCartProducts();
    
    /**
     * 根据购物车ID获取商品列表
     * @param cart_id 购物车ID
     * @return 商品列表
     */
    List<Product> getProductByCartID(Integer cart_id);
    
    /**
     * 更新购物车商品
     * @param cartProduct 要更新的购物车商品
     */
    void updateCartProduct(CartProduct cartProduct);
    
    /**
     * 删除购物车商品
     * @param cartProduct 要删除的购物车商品
     */
    void deleteCartProduct(CartProduct cartProduct);

    /**
     * 根据商品ID获取购物车商品
     * @param productId 商品ID
     * @return 购物车商品列表
     */
    List<CartProduct> getCartProductsByProductId(int productId);
}
