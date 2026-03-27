package com.jtspringproject.JtSpringProject.services.impl;

import com.jtspringproject.JtSpringProject.dao.CartDao;
import com.jtspringproject.JtSpringProject.models.Cart;
import com.jtspringproject.JtSpringProject.services.CartService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 购物车服务实现类
 *
 * <p>实现CartService接口，提供购物车相关的业务逻辑处理。
 * 作为Controller和DAO之间的中间层。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>购物车列表查询</li>
 *   <li>购物车添加</li>
 *   <li>购物车更新</li>
 *   <li>购物车删除</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see CartService
 * @see CartDao
 */
@Service
public class CartServiceImpl implements CartService {
    
    private static final Logger logger = LoggerFactory.getLogger(CartServiceImpl.class);

    @Autowired
    private CartDao cartDao;

    /**
     * 添加购物车
     *
     * @param cart 购物车对象
     * @return 添加后的购物车对象
     */
    @Override
    public Cart addCart(Cart cart) {
        logger.info("服务层：添加购物车，用户ID: {}",
                cart.getCustomer() != null ? cart.getCustomer().getId() : "null");
        try {
            Cart savedCart = cartDao.addCart(cart);
            logger.info("服务层：购物车添加成功，ID: {}", savedCart.getId());
            return savedCart;
        } catch (Exception e) {
            logger.error("服务层：添加购物车失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 获取所有购物车
     *
     * @return 购物车列表
     */
    @Override
    public List<Cart> getCarts() {
        logger.info("服务层：获取所有购物车");
        try {
            List<Cart> carts = this.cartDao.getCarts();
            logger.info("服务层：成功获取 {} 个购物车", carts.size());
            return carts;
        } catch (Exception e) {
            logger.error("服务层：获取购物车列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 更新购物车
     *
     * @param cart 要更新的购物车对象
     */
    @Override
    public void updateCart(Cart cart) {
        logger.info("服务层：更新购物车，ID: {}", cart.getId());
        try {
            cartDao.updateCart(cart);
            logger.info("服务层：购物车更新成功，ID: {}", cart.getId());
        } catch (Exception e) {
            logger.error("服务层：更新购物车失败，ID: {}, 错误: {}",
                    cart.getId(), e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 删除购物车
     *
     * @param cart 要删除的购物车对象
     */
    @Override
    public void deleteCart(Cart cart) {
        logger.info("服务层：删除购物车，ID: {}", cart.getId());
        try {
            cartDao.deleteCart(cart);
            logger.info("服务层：购物车删除成功，ID: {}", cart.getId());
        } catch (Exception e) {
            logger.error("服务层：删除购物车失败，ID: {}, 错误: {}",
                    cart.getId(), e.getMessage(), e);
            throw e;
        }
    }
}
