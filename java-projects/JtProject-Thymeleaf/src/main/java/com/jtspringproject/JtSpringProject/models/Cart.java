package com.jtspringproject.JtSpringProject.models;

import javax.persistence.*;
import javax.persistence.Table;
import java.util.ArrayList;
import java.util.List;

/**
 * 购物车实体类
 *
 * <p>表示电商系统中用户的购物车信息。每个用户可以拥有一个购物车，
 * 购物车中包含多个商品（通过CartProduct关联）。</p>
 *
 * <h3>数据库映射：</h3>
 * <ul>
 *   <li>表名：CART</li>
 *   <li>主键：id（自动生成）</li>
 * </ul>
 *
 * <h3>关系映射：</h3>
 * <ul>
 *   <li>与User：多对一关系，每个购物车属于一个用户</li>
 *   <li>与Product：通过CartProduct中间表关联多个商品</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see User
 * @see CartProduct
 */
@Entity
@Table(name = "CART")
public class Cart {

	/** 购物车ID，主键，自动生成 */
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    /** 购物车所属用户，多对一关系 */
    @ManyToOne
    @JoinColumn(name="customer_id")
    private User customer;

    // 注释：直接多对多关系已被移除，改用CartProduct中间表
//    @ManyToMany
//    @JoinTable(
//            joinColumns = @JoinColumn(name = "cart_id"),
//            inverseJoinColumns = @JoinColumn(name = "product_id")
//    )
//    private List<Product> products;

	/**
	 * 默认构造方法
	 */
    public Cart() {
    }

    /**
     * 获取购物车ID
     * @return 购物车ID
     */
    public int getId() {
        return id;
    }

    /**
     * 设置购物车ID
     * @param id 购物车ID
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * 获取购物车所属用户
     * @return 用户对象
     */
    public User getCustomer() {
        return customer;
    }

    /**
     * 设置购物车所属用户
     * @param customer 用户对象
     */
    public void setCustomer(User customer) {
        this.customer = customer;
    }

    // 注释：以下方法已弃用，改用CartProduct进行管理
//    public List<Product> getProducts() {
//        return products;
//    }

//    public List<Product> getProductsByUser(int customer_id ) {
//        List<Product> userProducts = new ArrayList<Product>();
//        for (Product product : products) {
//            if (product.getCustomer().getId() == customer_id) {
//                userProducts.add(product);
//            }
//        }
//        return userProducts;
//    }

//    public void setProducts(List<Product> products) {
//        this.products = products;
//    }

//    public void addProduct(Product product) {
//        products.add(product);
//    }
//
//    public void removeProduct(Product product) {
//        products.remove(product);
//    }
}
