package com.jtspringproject.JtSpringProject.models;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * 用户实体类
 *
 * <p>表示电商系统中的用户信息，包含用户基本属性和角色信息。</p>
 *
 * <h3>数据库映射：</h3>
 * <ul>
 *   <li>表名：CUSTOMER</li>
 *   <li>主键：id（自动生成）</li>
 *   <li>唯一约束：username</li>
 * </ul>
 *
 * <h3>用户角色：</h3>
 * <ul>
 *   <li>ROLE_ADMIN - 管理员角色，拥有商品管理、用户管理等权限</li>
 *   <li>ROLE_NORMAL - 普通用户角色，可以浏览商品、下单等</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see Cart
 */
@Entity
@Table(name="CUSTOMER")
public class User {

	/** 用户ID，主键，自动生成 */
	@Id
	@GeneratedValue(strategy=GenerationType.AUTO)
	private int id;

	/** 用户名，唯一约束 */
	@Column(unique = true)
	private String username;
	
	/** 电子邮箱 */
	private String email;
	
	/** 密码（明文存储，生产环境应加密） */
	private String password;
	
	/** 用户角色（ROLE_ADMIN 或 ROLE_NORMAL） */
	private String role;
	
	/** 用户地址 */
	private String address;
	
	/**
	 * 获取用户ID
	 * @return 用户ID
	 */
	public int getId() {
		return id;
	}

	/**
	 * 设置用户ID
	 * @param id 用户ID
	 */
	public void setId(int id) {
		this.id = id;
	}

	/**
	 * 获取用户名
	 * @return 用户名
	 */
	public String getUsername() {
		return username;
	}

	/**
	 * 设置用户名
	 * @param username 用户名
	 */
	public void setUsername(String username) {
		this.username = username;
	}

	/**
	 * 获取电子邮箱
	 * @return 电子邮箱
	 */
	public String getEmail() {
		return email;
	}

	/**
	 * 设置电子邮箱
	 * @param email 电子邮箱
	 */
	public void setEmail(String email) {
		this.email = email;
	}

	/**
	 * 获取密码
	 * @return 密码
	 */
	public String getPassword() {
		return password;
	}

	/**
	 * 设置密码
	 * @param password 密码
	 */
	public void setPassword(String password) {
		this.password = password;
	}

	/**
	 * 获取用户角色
	 * @return 角色（ROLE_ADMIN 或 ROLE_NORMAL）
	 */
	public String getRole() {
		return role;
	}

	/**
	 * 设置用户角色
	 * @param role 角色（ROLE_ADMIN 或 ROLE_NORMAL）
	 */
	public void setRole(String role) {
		this.role = role;
	}

	/**
	 * 获取用户地址
	 * @return 用户地址
	 */
	public String getAddress() {
		return address;
	}

	/**
	 * 设置用户地址
	 * @param address 用户地址
	 */
	public void setAddress(String address) {
		this.address = address;
	}

}
