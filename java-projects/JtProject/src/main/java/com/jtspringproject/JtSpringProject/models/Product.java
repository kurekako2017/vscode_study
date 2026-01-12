package com.jtspringproject.JtSpringProject.models;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToOne;

import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

/**
 * 商品实体类
 *
 * <p>表示电商系统中的商品信息，包含商品基本属性、分类关联和所属用户。</p>
 *
 * <h3>数据库映射：</h3>
 * <ul>
 *   <li>表名：PRODUCT</li>
 *   <li>主键：product_id（自动生成）</li>
 * </ul>
 *
 * <h3>关系映射：</h3>
 * <ul>
 *   <li>与Category：一对一关系，级联所有操作</li>
 *   <li>与User：多对一关系，表示商品所属用户</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see Category
 * @see User
 */
@Entity(name="PRODUCT")
public class Product {

	/** 商品ID，主键，自动生成 */
	@Id
	@Column(name = "product_id")
	@GeneratedValue(strategy=GenerationType.AUTO)
	private int id;
	
	/** 商品名称 */
	private String name;
	
	/** 商品图片路径 */
	private String image;
	
	/** 商品所属分类，一对一关系，级联所有操作（改为可选且延迟加载，缺失时忽略） */
	@OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY, optional = true)
	@JoinColumn(name = "category_id",referencedColumnName = "category_id")
	@NotFound(action = NotFoundAction.IGNORE)
	private Category category;
	
	/** 商品库存数量 */
	private int quantity;
	
	/** 商品价格（单位：分） */
	private int price;
	
	/** 商品重量（单位：克） */
	private int weight;
	
	/** 商品描述信息 */
	private String description;

	/** 商品所属用户，多对一关系 */
	@ManyToOne
    @JoinColumn(name = "customer_id")
    private User customer;

	/**
	 * 获取商品ID
	 * @return 商品ID
	 */
	public int getId() {
		return id;
	}

	/**
	 * 设置商品ID
	 * @param id 商品ID
	 */
	public void setId(int id) {
		this.id = id;
	}

	/**
	 * 获取商品名称
	 * @return 商品名称
	 */
	public String getName() {
		return name;
	}

	/**
	 * 设置商品名称
	 * @param name 商品名称
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * 获取商品图片路径
	 * @return 图片路径
	 */
	public String getImage() {
		return image;
	}

	/**
	 * 设置商品图片路径
	 * @param image 图片路径
	 */
	public void setImage(String image) {
		this.image = image;
	}

	/**
	 * 获取商品所属分类
	 * @return 分类对象
	 */
	public Category getCategory() {
		return category;
	}

	/**
	 * 设置商品所属分类
	 * @param category 分类对象
	 */
	public void setCategory(Category category) {
		this.category = category;
	}

	/**
	 * 获取商品库存数量
	 * @return 库存数量
	 */
	public int getQuantity() {
		return quantity;
	}

	/**
	 * 设置商品库存数量
	 * @param quantity 库存数量
	 */
	public void setQuantity(int quantity) {
		this.quantity = quantity;
	}

	/**
	 * 获取商品价格
	 * @return 价格（单位：分）
	 */
	public int getPrice() {
		return price;
	}

	/**
	 * 设置商品价格
	 * @param price 价格（单位：分）
	 */
	public void setPrice(int price) {
		this.price = price;
	}

	/**
	 * 获取商品重量
	 * @return 重量（单位：克）
	 */
	public int getWeight() {
		return weight;
	}

	/**
	 * 设置商品重量
	 * @param weight 重量（单位：克）
	 */
	public void setWeight(int weight) {
		this.weight = weight;
	}

	/**
	 * 获取商品描述信息
	 * @return 描述信息
	 */
	public String getDescription() {
		return description;
	}

	/**
	 * 设置商品描述信息
	 * @param description 描述信息
	 */
	public void setDescription(String description) {
		this.description = description;
	}
	
}
