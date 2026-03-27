package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.Cart;
import java.util.List;

/**
 * 购物车数据访问接口
 * 定义购物车数据库操作的契约
 */
public interface CartDao {
    
    /**
     * 添加购物车
     * @param cart 购物车对象
     * @return 添加后的购物车
     */
    Cart addCart(Cart cart);
    
    /**
     * 获取所有购物车
     * @return 购物车列表
     */
    List<Cart> getCarts();
    
    /**
     * 更新购物车
     * @param cart 要更新的购物车
     */
    void updateCart(Cart cart);
    
    /**
     * 删除购物车
     * @param cart 要删除的购物车
     */
    void deleteCart(Cart cart);
}
