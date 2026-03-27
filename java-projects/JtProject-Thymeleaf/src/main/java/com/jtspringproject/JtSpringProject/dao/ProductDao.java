package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.Product;
import java.util.List;

/**
 * 商品数据访问接口
 *
 * <p>定义商品数据库操作的契约，所有数据库访问操作都通过此接口定义。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.dao.impl.ProductDaoImpl
 */
public interface ProductDao {

    /**
     * 获取所有商品
     * @return 商品列表
     */
    List<Product> getProducts();

    /**
     * 添加商品
     * @param product 商品对象
     * @return 添加后的商品
     */
    Product addProduct(Product product);

    /**
     * 根据ID获取商品
     * @param id 商品ID
     * @return 商品对象
     */
    Product getProduct(int id);

    /**
     * 更新商品
     * @param product 要更新的商品
     * @return 更新后的商品
     */
    Product updateProduct(Product product);

    /**
     * 删除商品
     * @param id 商品ID
     * @return 是否删除成功
     */
    Boolean deletProduct(int id);
}

