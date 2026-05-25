package com.jtspringproject.JtSpringProject.dao.impl;

import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.query.Query;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.jtspringproject.JtSpringProject.dao.UserDao;
import com.jtspringproject.JtSpringProject.models.User;

/**
 * 用户数据访问实现类
 *
 * <p>实现UserDao接口，使用Hibernate SessionFactory直接操作数据库。
 * 提供用户的增删改查和认证功能。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>获取所有用户列表</li>
 *   <li>保存/更新用户</li>
 *   <li>用户登录验证</li>
 *   <li>检查用户名是否存在</li>
 * </ul>
 *
 * <h3>安全说明：</h3>
 * <p>当前密码采用明文存储和比对，生产环境建议使用加密方式（如BCrypt）。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see UserDao
 * @see User
 */
@Repository
public class UserDaoImpl implements UserDao {
    
    private static final Logger logger = LoggerFactory.getLogger(UserDaoImpl.class);

    @Autowired
    @Qualifier("secondarySessionFactory")
    @Lazy
    private SessionFactory sessionFactory;

    /**
     * 获取所有用户
     *
     * 📝 数据库操作流程：
     * 1. 获取Hibernate Session（当前事务会话）
     * 2. 执行HQL查询："from CUSTOMER"
     * 3. Hibernate将HQL转换为SQL：SELECT * FROM users
     * 4. 数据库执行查询，返回所有用户记录
     * 5. Hibernate将结果集映射为User对象列表
     * 6. 返回List<User>给Service层
     *
     * @return 用户列表
     */
    @Override
    @Transactional
    public List<User> getAllUser() {
        logger.info("DAO层：获取所有用户");
        try {
            // 获取当前Hibernate Session
            // Session是Hibernate的核心接口，用于执行数据库操作
            Session session = this.sessionFactory.getCurrentSession();

            // 执行HQL（Hibernate Query Language）查询
            // HQL语法：from CUSTOMER
            // 对应SQL：SELECT * FROM users
            // CUSTOMER是User实体类的@Entity注解名称（不是表名）
            // Hibernate会自动将CUSTOMER映射到users表
            List<User> userList = session.createQuery("from User", User.class).list();

            logger.info("DAO层：成功获取 {} 个用户", userList.size());
            return userList;
        } catch (Exception e) {
            logger.error("DAO层：获取用户列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 保存或更新用户
     *
     * 📝 数据库操作流程：
     * 1. 获取当前Hibernate Session
     * 2. 调用saveOrUpdate()方法
     * 3. Hibernate判断：
     *    - 如果user.id为null或0 → 执行INSERT（新增）
     *    - 如果user.id已存在 → 执行UPDATE（更新）
     * 4. 生成对应的SQL语句
     *    - INSERT: INSERT INTO users (...) VALUES (...)
     *    - UPDATE: UPDATE users SET ... WHERE id = ?
     * 5. 数据库执行SQL
     * 6. 如果是INSERT，Hibernate会将自动生成的ID设置到user对象
     * 7. 返回包含ID的user对象
     *
     * @param user 用户对象
     * @return 保存后的用户对象（包含自动生成的ID）
     */
    @Override
    @Transactional
    public User saveUser(User user) {
        logger.info("DAO层：保存用户: {}", user.getUsername());
        try {
            // 调用Hibernate的saveOrUpdate方法
            // 📝 saveOrUpdate自动判断：
            // - 如果是新对象（id为null或0）→ 执行INSERT操作
            //   SQL: INSERT INTO users (username, email, password, address, role)
            //        VALUES (?, ?, ?, ?, ?)
            //
            // - 如果对象已存在（id>0）→ 执行UPDATE操作
            //   SQL: UPDATE users SET username=?, email=?, password=?,
            //        address=?, role=? WHERE id=?
            //
            // Hibernate会自动管理事务，无需手动commit
            this.sessionFactory.getCurrentSession().saveOrUpdate(user);

            logger.info("DAO层：用户保存成功，ID: {}, 用户名: {}", user.getId(), user.getUsername());
            return user;
        } catch (Exception e) {
            logger.error("DAO层：保存用户失败，用户名: {}, 错误: {}", user.getUsername(), e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 用户登录验证
     *
     * <p>根据用户名查询用户，然后比对密码。如果验证成功返回用户对象，失败返回空User对象。</p>
     *
     * 📝 数据库操作流程：
     * 1. 创建HQL查询："from CUSTOMER where username = :username"
     * 2. 绑定参数：username值
     * 3. Hibernate转换为SQL：SELECT * FROM users WHERE username = ?
     * 4. 数据库执行查询
     * 5. 返回结果（可能是0、1或多条）
     * 6. 在Java代码中比对密码
     * 7. 密码正确返回User对象，错误返回空User对象
     *
     * <p><strong>安全警告：</strong>密码采用明文比对，生产环境应使用加密方式（如BCrypt）。</p>
     *
     * @param username 用户名
     * @param password 密码（明文）
     * @return 验证成功返回用户对象，失败返回空User对象
     */
    @Override
    @Transactional
    public User getUser(String username, String password) {
        logger.info("DAO层：用户登录验证: {}", username);
        try {
            // 创建Hibernate Query对象
            Query<User> query = sessionFactory.getCurrentSession()
                    .createQuery("from User where username = :username", User.class);
            query.setParameter("username", username);
            logger.debug("DAO层：执行HQL: {}，参数: username={}", query.getQueryString(), username);
            List<User> results = query.getResultList();
            if (results == null || results.isEmpty()) {
                logger.warn("DAO层：用户不存在: {}", username);
                return new User();
            }
            if (results.size() > 1) {
                logger.warn("DAO层：查询到多条相同用户名的记录: {}，将使用第一条进行验证", username);
            }
            User user = results.get(0);
            logger.debug("DAO层：找到用户: {} (id={})", username, user.getId());
            String stored = user.getPassword();
            if (stored != null && stored.equals(password)) {
                logger.info("DAO层：用户登录成功: {}, 角色: {}", username, user.getRole());
                return user;
            } else {
                logger.warn("DAO层：用户密码错误: {}", username);
                return new User();
            }
        } catch (Exception e) {
            logger.error("DAO层：getUser() 总异常捕获: {} - {}", e.getClass().getName(), e.getMessage(), e);
            return new User();
        }
    }

    @Override
    @Transactional
    public User getUserByUsername(String username) {
        logger.info("DAO层：根据用户名获取用户: {}", username);
        try {
            Query<User> query = sessionFactory.getCurrentSession()
                    .createQuery("from User where username = :username", User.class);
            query.setParameter("username", username);
            List<User> results = query.getResultList();
            if (results == null || results.isEmpty()) {
                return null;
            }
            return results.get(0);
        } catch (Exception e) {
            logger.error("DAO层：根据用户名获取用户失败: {}, 错误: {}", username, e.getMessage(), e);
            throw e;
        }
    }

    @Override
    @Transactional
    public User getUserById(int id) {
        logger.info("DAO层：根据ID获取用户: {}", id);
        try {
            return sessionFactory.getCurrentSession().get(User.class, id);
        } catch (Exception e) {
            logger.error("DAO层：根据ID获取用户失败: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 检查用户名是否存在
     *
     * 📝 数据库操作流程：
     * 1. 创建HQL COUNT查询："SELECT COUNT(u) FROM CUSTOMER u WHERE u.username = :username"
     * 2. 绑定参数：username值
     * 3. Hibernate转换为SQL：SELECT COUNT(*) FROM users WHERE username = ?
     * 4. 数据库执行查询，返回数量
     * 5. 获取查询结果（Long类型）
     * 6. 如果count > 0，表示用户名已存在
     * 7. 返回boolean结果
     *
     * @param username 用户名
     * @return 存在返回true，不存在返回false
     */
    @Override
    @Transactional
    public boolean userExists(String username) {
        logger.info("DAO层：检查用户名是否存在: {}", username);
        try {
            Query<Long> query = sessionFactory.getCurrentSession()
                .createQuery("SELECT COUNT(u) FROM User u WHERE u.username = :username", Long.class);

            query.setParameter("username", username);

            Long count = query.uniqueResult();

            boolean exists = count != null && count > 0;

            logger.info("DAO层：用户名 {} 存在性: {}", username, exists);
            return exists;
        } catch (Exception e) {
            logger.error("DAO层：检查用户名失败: {}, 错误: {}", username, e.getMessage(), e);
            throw e;
        }
    }
}
