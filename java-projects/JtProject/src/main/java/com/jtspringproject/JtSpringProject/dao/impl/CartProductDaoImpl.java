package com.jtspringproject.JtSpringProject.dao.impl;

import com.jtspringproject.JtSpringProject.dao.CartProductDao;
import com.jtspringproject.JtSpringProject.models.CartProduct;
import com.jtspringproject.JtSpringProject.models.Product;
import org.hibernate.SessionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 购物车商品数据访问实现类
 *
 * <p>实现CartProductDao接口，使用Hibernate SessionFactory直接操作数据库。
 * 提供购物车商品关联的增删改查功能。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>添加购物车商品关联</li>
 *   <li>获取所有购物车商品关联列表</li>
 *   <li>根据购物车ID获取商品列表</li>
 *   <li>更新购物车商品关联</li>
 *   <li>删除购物车商品关联</li>
 * </ul>
 *
 * <h3>技术特点：</h3>
 * <p>使用原生SQL查询实现复杂的关联查询，提高查询效率。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see CartProductDao
 * @see CartProduct
 */
@Repository
public class CartProductDaoImpl implements CartProductDao {
    
    private static final Logger logger = LoggerFactory.getLogger(CartProductDaoImpl.class);

    private SessionFactory sessionFactory;

    @Autowired
    public void setSessionFactory(SessionFactory sessionFactory) {
        this.sessionFactory = sessionFactory;
    }

    /**
     * 添加购物车商品关联
     *
     * @param cartProduct 购物车商品关联对象
     * @return 添加后的对象（包含自动生成的ID）
     */
    @Override
    @Transactional
    public CartProduct addCartProduct(CartProduct cartProduct) {
        logger.info("添加购物车商品，购物车ID: {}, 商品ID: {}",
                cartProduct.getCart() != null ? cartProduct.getCart().getId() : "null",
                cartProduct.getProduct() != null ? cartProduct.getProduct().getId() : "null");
        try {
            this.sessionFactory.getCurrentSession().save(cartProduct);
            logger.info("购物车商品添加成功，ID: {}", cartProduct.getId());
            return cartProduct;
        } catch (Exception e) {
            logger.error("添加购物车商品失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 获取所有购物车商品关联
     *
     * @return 购物车商品关联列表
     */
    @Override
    @Transactional
    public List<CartProduct> getCartProducts() {
        logger.info("获取所有购物车商品");
        try {
            List<CartProduct> cartProducts = this.sessionFactory.getCurrentSession()
                .createQuery("from CartProduct", CartProduct.class)
                .list();
            logger.info("成功获取 {} 个购物车商品关联", cartProducts.size());
            return cartProducts;
        } catch (Exception e) {
            logger.error("获取购物车商品列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 根据购物车ID获取商品列表
     *
     * <p>使用原生SQL查询，分两步：</p>
     * <ol>
     *   <li>从cart_product表查询商品ID列表</li>
     *   <li>根据商品ID列表查询商品详情</li>
     * </ol>
     *
     * @param cart_id 购物车ID
     * @return 商品列表
     */
    @Override
    @Transactional
    public List<Product> getProductByCartID(Integer cart_id) {
        logger.info("根据购物车ID获取商品列表，购物车ID: {}", cart_id);
        try {
            // 先查询 CartProduct 实体，再在 Java 层提取 Product，避免 join/返回类型问题
            String hqlCp = "from CartProduct cp where cp.cart.id = :cart_id";
            List<CartProduct> cps = this.sessionFactory.getCurrentSession()
                    .createQuery(hqlCp, CartProduct.class)
                    .setParameter("cart_id", cart_id)
                    .list();

            List<Product> products = new java.util.ArrayList<>();
            if (cps != null) {
                for (CartProduct cp : cps) {
                    if (cp != null && cp.getProduct() != null) {
                        products.add(cp.getProduct());
                    }
                }
            }
            logger.info("成功获取购物车 {} 的 {} 个商品", cart_id, products.size());
            return products;
        } catch (Exception e) {
            logger.error("根据购物车ID获取商品失败，购物车ID: {}，异常: {}，原因: {}",
                    cart_id, e.getClass().getName(), e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 更新购物车商品关联
     *
     * @param cartProduct 要更新的购物车商品关联对象
     */
    @Override
    @Transactional
    public void updateCartProduct(CartProduct cartProduct) {
        logger.info("更新购物车商品，ID: {}", cartProduct.getId());
        try {
            this.sessionFactory.getCurrentSession().update(cartProduct);
            logger.info("购物车商品更新成功，ID: {}", cartProduct.getId());
        } catch (Exception e) {
            logger.error("更新购物车商品失败，ID: {}, 错误: {}",
                    cartProduct.getId(), e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 删除购物车商品关联
     *
     * @param cartProduct 要删除的购物车商品关联对象
     */
    @Override
    @Transactional
    public void deleteCartProduct(CartProduct cartProduct) {
        logger.info("删除购物车商品，ID: {}", cartProduct.getId());
        try {
            this.sessionFactory.getCurrentSession().delete(cartProduct);
            logger.info("购物车商品删除成功，ID: {}", cartProduct.getId());
        } catch (Exception e) {
            logger.error("删除购物车商品失败，ID: {}, 错误: {}",
                    cartProduct.getId(), e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 根据商品ID获取购物车商品
     *
     * @param productId 商品ID
     * @return 购物车商品列表
     */
    @Override
    @Transactional
    public List<CartProduct> getCartProductsByProductId(int productId) {
        logger.info("根据商品ID获取购物车商品，商品ID: {}", productId);
        try {
            // 修正HQL，CartProduct中应为product.id
            String hql = "FROM CartProduct cp WHERE cp.product.id = :productId";
            return this.sessionFactory.getCurrentSession()
                    .createQuery(hql, CartProduct.class)
                    .setParameter("productId", productId)
                    .getResultList();
        } catch (Exception e) {
            logger.error("获取购物车商品失败，商品ID: {}, 错误: {}", productId, e.getMessage(), e);
            throw e;
        }
    }
}
