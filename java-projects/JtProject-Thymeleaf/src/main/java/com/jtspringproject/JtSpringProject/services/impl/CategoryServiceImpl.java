package com.jtspringproject.JtSpringProject.services.impl;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.jtspringproject.JtSpringProject.dao.CategoryDao;
import com.jtspringproject.JtSpringProject.models.Category;
import com.jtspringproject.JtSpringProject.services.CategoryService;

/**
 * 分类服务实现类
 *
 * <p>实现CategoryService接口，提供商品分类相关的业务逻辑处理。
 * 作为Controller和DAO之间的中间层。</p>
 *
 * <h3>主要功能：</h3>
 * <ul>
 *   <li>分类列表查询</li>
 *   <li>分类详情查询</li>
 *   <li>分类添加</li>
 *   <li>分类更新</li>
 *   <li>分类删除</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see CategoryService
 * @see CategoryDao
 */
@Service
public class CategoryServiceImpl implements CategoryService {
    
    private static final Logger logger = LoggerFactory.getLogger(CategoryServiceImpl.class);

    @Autowired
    private CategoryDao categoryDao;
    
    /**
     * 添加分类
     *
     * @param name 分类名称
     * @return 添加后的分类对象
     */
    @Override
    public Category addCategory(String name) {
        logger.info("服务层：添加分类，名称: {}", name);
        try {
            Category category = this.categoryDao.addCategory(name);
            logger.info("服务层：分类添加成功，ID: {}, 名称: {}", category.getId(), name);
            return category;
        } catch (Exception e) {
            logger.error("服务层：添加分类失败，名称: {}, 错误: {}", name, e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 获取所有分类
     *
     * @return 分类列表
     */
    @Override
    public List<Category> getCategories(){
        logger.info("服务层：获取所有分类");
        try {
            List<Category> categories = this.categoryDao.getCategories();
            logger.info("服务层：成功获取 {} 个分类", categories.size());
            return categories;
        } catch (Exception e) {
            logger.error("服务层：获取分类列表失败: {}", e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 删除分类
     *
     * @param id 分类ID
     * @return 删除成功返回true，失败返回false
     */
    @Override
    public Boolean deleteCategory(int id) {
        logger.info("服务层：删除分类，ID: {}", id);
        try {
            Boolean result = this.categoryDao.deletCategory(id);
            if (result) {
                logger.info("服务层：分类删除成功，ID: {}", id);
            } else {
                logger.warn("服务层：分类删除失败（可能不存在），ID: {}", id);
            }
            return result;
        } catch (Exception e) {
            logger.error("服务层：删除分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }
    
    /**
     * 更新分类
     *
     * @param id 分类ID
     * @param name 新的分类名称
     * @return 更新后的分类对象
     */
    @Override
    public Category updateCategory(int id, String name) {
        logger.info("服务层：更新分类，ID: {}, 新名称: {}", id, name);
        try {
            Category category = this.categoryDao.updateCategory(id, name);
            logger.info("服务层：分类更新成功，ID: {}", id);
            return category;
        } catch (Exception e) {
            logger.error("服务层：更新分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 根据ID获取分类详情
     *
     * @param id 分类ID
     * @return 分类对象
     */
    @Override
    public Category getCategory(int id) {
        logger.info("服务层：获取分类详情，ID: {}", id);
        try {
            Category category = this.categoryDao.getCategory(id);
            if (category != null) {
                logger.info("服务层：成功获取分类，ID: {}, 名称: {}", id, category.getName());
            } else {
                logger.warn("服务层：分类不存在，ID: {}", id);
            }
            return category;
        } catch (Exception e) {
            logger.error("服务层：获取分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }
}
