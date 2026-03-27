package com.jtspringproject.JtSpringProject.dao.impl;

import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.jtspringproject.JtSpringProject.dao.ProductDao;
import com.jtspringproject.JtSpringProject.models.Product;

/**
 * 商品数据访问实现类
 *
 * <p>实现ProductDao接口，使用Hibernate SessionFactory直接操作数据库。
 * 提供商品的增删改查功能。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>获取所有商品列表</li>
 *   <li>添加新商品</li>
 *   <li>根据ID获取商品详情</li>
 *   <li>更新商品信息</li>
 *   <li>删除商品</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see ProductDao
 * @see Product
 */
@Repository
public class ProductDaoImpl implements ProductDao {
    
    private static final Logger logger = LoggerFactory.getLogger(ProductDaoImpl.class);

    @Autowired
    @Qualifier("secondarySessionFactory")
    @Lazy
    private SessionFactory sessionFactory;

    /**
     * 获取所有商品
     *
     * @return 商品列表
     */
    @Override
    @Transactional
    public List<Product> getProducts(){
        logger.info("获取所有商品");
        try {
                List<Product> products = this.sessionFactory.getCurrentSession()
                    .createQuery("from Product", Product.class).list();
            logger.info("成功获取 {} 个商品", products.size());
            return products;
        } catch (Exception e) {
            logger.error("获取商品列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 添加商品
     *
     * @param product 商品对象
     * @return 添加后的商品对象（包含自动生成的ID）
     */
    @Override
    @Transactional
    public Product addProduct(Product product) {
        logger.info("添加商品: {}", product.getName());
        try {
            this.sessionFactory.getCurrentSession().save(product);
            logger.info("商品添加成功，ID: {}, 名称: {}", product.getId(), product.getName());
            return product;
        } catch (Exception e) {
            logger.error("添加商品失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 根据ID获取商品
     *
     * @param id 商品ID
     * @return 商品对象，不存在则返回null
     */
    @Override
    @Transactional
    public Product getProduct(int id) {
        logger.info("获取商品详情，ID: {}", id);
        try {
            Product product = this.sessionFactory.getCurrentSession().get(Product.class, id);
            if (product != null) {
                logger.info("成功获取商品，ID: {}, 名称: {}", id, product.getName());
            } else {
                logger.warn("商品不存在，ID: {}", id);
            }
            return product;
        } catch (Exception e) {
            logger.error("获取商品失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 更新商品信息
     *
     * @param product 要更新的商品对象
     * @return 更新后的商品对象
     */
    @Override
    public Product updateProduct(Product product){
        logger.info("更新商品，ID: {}, 名称: {}", product.getId(), product.getName());
        try {
            this.sessionFactory.getCurrentSession().update(product);
            logger.info("商品更新成功，ID: {}", product.getId());
            return product;
        } catch (Exception e) {
            logger.error("更新商品失败，ID: {}, 错误: {}", product.getId(), e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 删除商品
     *
     * @param id 商品ID
     * @return 删除成功返回true，失败返回false
     */
    @Override
    @Transactional
    public Boolean deletProduct(int id) {
        logger.info("删除商品，ID: {}", id);
        try {
            Session session = this.sessionFactory.getCurrentSession();
            Object persistanceInstance = session.load(Product.class, id);

            if (persistanceInstance != null) {
                session.delete(persistanceInstance);
                logger.info("商品删除成功，ID: {}", id);
                return true;
            }
            logger.warn("商品不存在，无法删除，ID: {}", id);
            return false;
        } catch (Exception e) {
            logger.error("删除商品失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }
}
