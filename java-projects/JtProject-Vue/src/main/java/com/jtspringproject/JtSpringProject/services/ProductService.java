package com.jtspringproject.JtSpringProject.services;

import com.jtspringproject.JtSpringProject.models.Product;
import java.util.List;

/**
 * 商品服务接口
 *
 * <p>定义商品业务逻辑的契约，提供商品管理的业务方法。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.services.impl.ProductServiceImpl
 */
public interface ProductService {

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
     * @param id 商品ID
     * @param product 新的商品信息
     * @return 更新后的商品
     */
    Product updateProduct(int id, Product product);

    /**
     * 删除商品
     * @param id 商品ID
     * @return 是否删除成功
     */
    boolean deleteProduct(int id);
}

