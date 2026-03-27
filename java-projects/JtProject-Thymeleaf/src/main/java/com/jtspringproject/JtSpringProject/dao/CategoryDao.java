package com.jtspringproject.JtSpringProject.dao;

import com.jtspringproject.JtSpringProject.models.Category;
import java.util.List;

/**
 * 分类数据访问接口
 * 定义分类数据库操作的契约
 */
public interface CategoryDao {
    
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
    Boolean deletCategory(int id);
    
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
