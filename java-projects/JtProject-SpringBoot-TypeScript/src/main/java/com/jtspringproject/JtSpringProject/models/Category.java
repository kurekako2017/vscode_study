package com.jtspringproject.JtSpringProject.models;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * 商品分类实体类
 *
 * <p>表示电商系统中的商品分类信息，用于对商品进行分类管理。</p>
 *
 * <h3>数据库映射：</h3>
 * <ul>
 *   <li>表名：CATEGORY</li>
 *   <li>主键：category_id（自动生成）</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see Product
 */
@Entity
@Table(name = "CATEGORY")
public class Category {

	/** 分类ID，主键，自动生成 */
	@Id
	@Column(name = "category_id")
	@GeneratedValue(strategy=GenerationType.AUTO)
	private int id;
	
	/** 分类名称 */
	private String name;
	
	/**
	 * 获取分类ID
	 * @return 分类ID
	 */
	public int getId() {
		return id;
	}

	/**
	 * 设置分类ID
	 * @param id 分类ID
	 */
	public void setId(int id) {
		this.id = id;
	}

	/**
	 * 获取分类名称
	 * @return 分类名称
	 */
	public String getName() {
		return name;
	}

	/**
	 * 设置分类名称
	 * @param name 分类名称
	 */
	public void setName(String name) {
		this.name = name;
	}
	
}
