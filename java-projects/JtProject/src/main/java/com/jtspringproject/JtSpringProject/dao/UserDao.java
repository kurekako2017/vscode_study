package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.User;
import java.util.List;

/**
 * 用户数据访问接口
 *
 * <p>定义用户数据库操作的契约，包括用户管理和认证功能。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.dao.impl.UserDaoImpl
 */
public interface UserDao {

    /**
     * 获取所有用户
     * @return 用户列表
     */
    List<User> getAllUser();

    /**
     * 保存或更新用户
     * @param user 用户对象
     * @return 保存后的用户
     */
    User saveUser(User user);

    /**
     * 根据用户名和密码获取用户（用于登录验证）
     * @param username 用户名
     * @param password 密码
     * @return 用户对象，如果验证失败返回空对象
     */
    User getUser(String username, String password);

    /**
     * 根据用户名获取用户
     * @param username 用户名
     * @return 用户对象，不存在返回null
     */
    User getUserByUsername(String username);

    /**
     * 根据ID获取用户
     * @param id 用户ID
     * @return 用户对象，不存在返回null
     */
    User getUserById(int id);

    /**
     * 检查用户是否存在
     * @param username 用户名
     * @return 用户是否存在
     */
    boolean userExists(String username);
}

