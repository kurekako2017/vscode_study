package com.jtspringproject.JtSpringProject.dao.impl;

import java.util.List;

import com.jtspringproject.JtSpringProject.dao.CartDao;
import com.jtspringproject.JtSpringProject.models.Cart;
import org.hibernate.SessionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

/**
 * 购物车数据访问实现类
 *
 * <p>实现CartDao接口，使用Hibernate SessionFactory直接操作数据库。
 * 提供购物车的增删改查功能。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>添加购物车</li>
 *   <li>获取所有购物车列表</li>
 *   <li>更新购物车信息</li>
 *   <li>删除购物车</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see CartDao
 * @see Cart
 */
@Repository
public class CartDaoImpl implements CartDao {
    
    private static final Logger logger = LoggerFactory.getLogger(CartDaoImpl.class);

    private SessionFactory sessionFactory;

    @Autowired
    public void setSessionFactory(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }

    /**
     * 添加购物车
     *
     * @param cart 购物车对象
     * @return 添加后的购物车对象（包含自动生成的ID）
     */
    @Override
    @Transactional
    public Cart addCart(Cart cart) {
        logger.info("添加购物车，用户ID: {}",
                cart.getCustomer() != null ? cart.getCustomer().getId() : "null");
        try {
            this.sessionFactory.getCurrentSession().save(cart);
            logger.info("购物车添加成功，ID: {}", cart.getId());
            return cart;
        } catch (Exception e) {
            logger.error("添加购物车失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 获取所有购物车
     *
     * @return 购物车列表
     */
    @Override
    @Transactional
    public List<Cart> getCarts() {
        logger.info("获取所有购物车");
        try {
                List<Cart> carts = this.sessionFactory.getCurrentSession()
                    .createQuery("from Cart", Cart.class)
                    .list();
            logger.info("成功获取 {} 个购物车", carts.size());
            return carts;
        } catch (Exception e) {
            logger.error("获取购物车列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 更新购物车
     *
     * @param cart 要更新的购物车对象
     */
    @Override
    @Transactional
    public void updateCart(Cart cart) {
        logger.info("更新购物车，ID: {}", cart.getId());
        try {
            this.sessionFactory.getCurrentSession().update(cart);
            logger.info("购物车更新成功，ID: {}", cart.getId());
        } catch (Exception e) {
            logger.error("更新购物车失败，ID: {}, 错误: {}", cart.getId(), e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 删除购物车
     *
     * @param cart 要删除的购物车对象
     */
    @Override
    @Transactional
    public void deleteCart(Cart cart) {
        logger.info("删除购物车，ID: {}", cart.getId());
        try {
            this.sessionFactory.getCurrentSession().delete(cart);
            logger.info("购物车删除成功，ID: {}", cart.getId());
        } catch (Exception e) {
            logger.error("删除购物车失败，ID: {}, 错误: {}", cart.getId(), e.getMessage(), e);
            throw e;
        }
    }
}
