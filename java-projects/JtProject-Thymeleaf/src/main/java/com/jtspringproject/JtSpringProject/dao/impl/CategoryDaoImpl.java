package com.jtspringproject.JtSpringProject.dao.impl;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.jtspringproject.JtSpringProject.dao.CategoryDao;
import com.jtspringproject.JtSpringProject.models.Category;

/**
 * 分类数据访问实现类
 *
 * <p>实现CategoryDao接口，使用Hibernate EntityManager直接操作数据库。
 * 所有方法都使用@Transactional注解确保事务管理。</p>
 *
 * <h3>技术特点：</h3>
 * <ul>
 *   <li>使用Hibernate EntityManager进行数据库操作</li>
 *   <li>使用HQL查询语言</li>
 *   <li>方法级别的声明式事务管理</li>
 * </ul>
 *
 * @author JT Spring Project Team
 * @version 1.0
 * @see CategoryDao
 * @see Category
 */
@Repository
public class CategoryDaoImpl implements CategoryDao {
    
    private static final Logger logger = LoggerFactory.getLogger(CategoryDaoImpl.class);

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * 添加分类
     *
     * @param name 分类名称
     * @return 添加后的分类对象（包含自动生成的ID）
     */
    @Override
    @Transactional
    public Category addCategory(String name) {
        logger.info("添加分类: {}", name);
        try {
            Category category = new Category();
            category.setName(name);
            entityManager.persist(category);
            logger.info("分类添加成功，ID: {}", category.getId());
            return category;
        } catch (Exception e) {
            logger.error("添加分类失败: {}", e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 获取所有分类
     *
     * @return 分类列表
     */
    @Override
    @Transactional
    public List<Category> getCategories() {
        logger.info("获取所有分类");
        try {
            List<Category> categories = entityManager.createQuery("from Category", Category.class).getResultList();
            logger.info("成功获取 {} 个分类", categories.size());
            return categories;
        } catch (Exception e) {
            logger.error("获取分类列表失败: {}", e.getMessage(), e);
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
    @Transactional
    public Boolean deletCategory(int id) {
        logger.info("删除分类，ID: {}", id);
        try {
            Category category = entityManager.find(Category.class, id);
            if (category != null) {
                entityManager.remove(category);
                logger.info("分类删除成功，ID: {}", id);
                return true;
            }
            logger.warn("分类不存在，无法删除，ID: {}", id);
            return false;
        } catch (Exception e) {
            logger.error("删除分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
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
    @Transactional
    public Category updateCategory(int id, String name) {
        logger.info("更新分类，ID: {}, 新名称: {}", id, name);
        try {
            Category category = entityManager.find(Category.class, id);
            if (category == null) {
                logger.error("分类不存在，无法更新，ID: {}", id);
                throw new RuntimeException("分类不存在: " + id);
            }
            category.setName(name);
            entityManager.merge(category);
            logger.info("分类更新成功，ID: {}", id);
            return category;
        } catch (Exception e) {
            logger.error("更新分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }

    /**
     * 根据ID获取分类
     *
     * @param id 分类ID
     * @return 分类对象，不存在则返回null
     */
    @Override
    @Transactional
    public Category getCategory(int id) {
        logger.info("获取分类详情，ID: {}", id);
        try {
            Category category = entityManager.find(Category.class, id);
            if (category != null) {
                logger.info("成功获取分类，ID: {}, 名称: {}", id, category.getName());
            } else {
                logger.warn("分类不存在，ID: {}", id);
            }
            return category;
        } catch (Exception e) {
            logger.error("获取分类失败，ID: {}, 错误: {}", id, e.getMessage(), e);
            throw e;
        }
    }
}
