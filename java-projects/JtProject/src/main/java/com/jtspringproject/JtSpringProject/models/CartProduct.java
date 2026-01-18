package com.jtspringproject.JtSpringProject.models;

import javax.persistence.*;

/**
 * 购物车商品关联实体类
 *
 * <p>表示购物车和商品之间的多对多关联关系。采用中间表模式，
 * 将Cart和Product的多对多关系拆分为两个多对一关系。</p>
 *
 * <h3>数据库映射：</h3>
 * <ul>
 *   <li>表名：CART_PRODUCT</li>
 *   <li>主键：id（自动生成）</li>
 *   <li>外键：cart_id、product_id</li>
 * </ul>
 *
 * <h3>关系映射：</h3>
 * <ul>
 *   <li>与Cart：多对一关系，多个购物车商品记录属于一个购物车</li>
 *   <li>与Product：多对一关系，多个购物车商品记录可以关联同一个商品</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see Cart
 * @see Product
 */
@Entity
@Table(name = "CART_PRODUCT")
public class CartProduct {

	/** 购物车商品关联ID，主键，自动生成 */
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    /** 所属购物车，多对一关系 */
    @ManyToOne
    @JoinColumn(name="cart_id", nullable = false)
    private Cart cart;

    /** 关联的商品，多对一关系 */
    @ManyToOne
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

	/**
	 * 默认构造方法
	 * 初始化product为null
	 */
    public CartProduct() {
        product = null;
    }

    /**
     * 带参数的构造方法
     *
     * @param cart 购物车对象
     * @param product 商品对象
     */
    public CartProduct(Cart cart, Product product) {
        this.cart=cart;
        this.product = product;
    }

    /**
     * 获取购物车商品关联ID
     * @return 关联ID
     */
    public int getId() {
        return id;
    }

    /**
     * 设置购物车商品关联ID
     * @param id 关联ID
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * 获取所属购物车
     * @return 购物车对象
     */
    public Cart getCart() {
        return cart;
    }

    /**
     * 设置所属购物车
     * @param cart 购物车对象
     */
    public void setCart(Cart cart) {
        this.cart = cart;
    }

    /**
     * 获取关联的商品
     * @return 商品对象
     */
    public Product getProduct() {
        return product;
    }

    /**
     * 设置关联的商品
     * @param product 商品对象
     */
    public void setProduct(Product product) {
        this.product = product;
    }
}
