package com.jtspringproject.JtSpringProject.services;

import com.jtspringproject.JtSpringProject.models.User;
import java.util.List;

/**
 * 用户服务接口
 *
 * <p>定义用户业务逻辑的契约，提供用户管理和认证的业务方法。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.services.impl.UserServiceImpl
 */
public interface UserService {

    /**
     * 获取所有用户
     * @return 用户列表
     */
    List<User> getUsers();

    /**
     * 添加用户
     * @param user 用户对象
     * @return 添加后的用户
     */
    User addUser(User user);

    /**
     * 验证用户登录
     * @param username 用户名
     * @param password 密码
     * @return 用户对象，如果验证失败返回空对象
     */
    User checkLogin(String username, String password);

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
    boolean checkUserExists(String username);
}

