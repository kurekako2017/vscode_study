package com.jtspringproject.JtSpringProject.services;

import com.jtspringproject.JtSpringProject.models.Category;
import java.util.List;

/**
 * 分类服务接口
 *
 * <p>定义分类业务逻辑的契约，提供商品分类管理的业务方法。</p>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see com.jtspringproject.JtSpringProject.services.impl.CategoryServiceImpl
 */
public interface CategoryService {

    /**
     * 添加分类
     * @param name 分类名称
     * @return 添加后的分类对象
     */
    Category addCategory(String name);

    /**
     * 获取所有分类
     * @return 分类列表
     */
    List<Category> getCategories();

    /**
     * 删除分类
     * @param id 分类ID
     * @return 是否删除成功
     */
    Boolean deleteCategory(int id);

    /**
     * 更新分类
     * @param id 分类ID
     * @param name 新的分类名称
     * @return 更新后的分类对象
     */
    Category updateCategory(int id, String name);

    /**
     * 根据ID获取分类
     * @param id 分类ID
     * @return 分类对象
     */
    Category getCategory(int id);
}

