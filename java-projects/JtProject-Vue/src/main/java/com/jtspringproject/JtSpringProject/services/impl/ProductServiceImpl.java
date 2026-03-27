package com.jtspringproject.JtSpringProject.services.impl;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jtspringproject.JtSpringProject.dao.ProductDao;
import com.jtspringproject.JtSpringProject.models.Product;
import com.jtspringproject.JtSpringProject.services.ProductService;

/**
 * 商品服务实现类
 *
 * <p>实现ProductService接口，作为Controller和DAO之间的中间层。
 * 提供商品业务逻辑处理和事务协调。</p>
 *
 * <h3>架构层次：</h3>
 * <ul>
 *   <li>Controller层调用Service层方法</li>
 *   <li>Service层协调业务逻辑，调用DAO层</li>
 *   <li>DAO层直接操作数据库</li>
 * </ul>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>商品列表查询</li>
 *   <li>商品详情查询</li>
 *   <li>商品添加</li>
 *   <li>商品更新</li>
 *   <li>商品删除</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see ProductService
 * @see ProductDao
 */
@Service
public class ProductServiceImpl implements ProductService {
    
    private static final Logger logger = LoggerFactory.getLogger(ProductServiceImpl.class);

    @Autowired
    private ProductDao productDao;
    
    /**
     * 获取所有商品
     *
     * @return 商品列表
     */
    @Override
    public List<Product> getProducts(){
        logger.info("服务层：获取所有商品");
        try {
            List<Product> products = this.productDao.getProducts();
            logger.info("服务层：成功获取 {} 个商品", products.size());
            return products;
        } catch (Exception e) {
            logger.error("服务层：获取商品列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 添加商品
     *
     * @param product 商品对象
     * @return 添加后的商品对象
     */
    @Override
    public Product addProduct(Product product) {
        logger.info("服务层：添加商品，名称: {}", product.getName());
        try {
            Product savedProduct = this.productDao.addProduct(product);
            logger.info("服务层：商品添加成功，ID: {}", savedProduct.getId());
            return savedProduct;
        } catch (Exception e) {
            logger.error("服务层：添加商品失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 根据ID获取商品详情
     *
     * @param id 商品ID
     * @return 商品对象
     */
    @Override
    public Product getProduct(int id) {
        logger.info("服务层：获取商品详情，ID: {}", id);
        try {
            Product product = this.productDao.getProduct(id);
            if (product != null) {
                logger.info("服务层：成功获取商品，ID: {}, 名称: {}", id, product.getName());
            } else {
                logger.warn("服务层：商品不存在，ID: {}", id);
            }
            return product;
        } catch (Exception e) {
            logger.error("服务层：获取商品失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 更新商品信息
     *
     * @param id 商品ID
     * @param product 商品对象
     * @return 更新后的商品对象
     */
    @Override
    public Product updateProduct(int id, Product product){
        logger.info("服务层：更新商品，ID: {}, 名称: {}", id, product.getName());
        try {
            product.setId(id);
            Product updatedProduct = this.productDao.updateProduct(product);
            logger.info("服务层：商品更新成功，ID: {}", id);
            return updatedProduct;
        } catch (Exception e) {
            logger.error("服务层：更新商品失败，ID: {}, 错误: {}", id, e.getMessage(), e);
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
    public boolean deleteProduct(int id) {
        logger.info("服务层：删除商品，ID: {}", id);
        try {
            boolean result = this.productDao.deletProduct(id);
            if (result) {
                logger.info("服务层：商品删除成功，ID: {}", id);
            } else {
                logger.warn("服务层：商品删除失败（可能不存在），ID: {}", id);
            }
            return result;
        } catch (Exception e) {
            logger.error("服务层：删除商品失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }
}
