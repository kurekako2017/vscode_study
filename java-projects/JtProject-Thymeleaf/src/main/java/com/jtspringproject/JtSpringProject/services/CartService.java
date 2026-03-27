package com.jtspringproject.JtSpringProject.services;

import com.jtspringproject.JtSpringProject.models.Cart;
import java.util.List;

/**
 * 购物车服务接口
 *
 * <p>定义购物车业务逻辑的契约，提供购物车管理的业务方法。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.services.impl.CartServiceImpl
 */
public interface CartService {

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

