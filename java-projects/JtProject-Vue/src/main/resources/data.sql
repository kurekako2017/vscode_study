-- 测试和开发环境数据初始化SQL脚本
-- 该脚本会在应用启动时自动执行
-- 用途：为开发和测试提供基础数据

-- ==================== 插入默认分类 ====================
INSERT INTO CATEGORY(category_id, name) VALUES 
(1, 'Fruits'),
(2, 'Vegetables'),
(3, 'Meat'),
(4, 'Fish'),
(5, 'Dairy'),
(6, 'Bakery'),
(7, 'Drinks'),
(8, 'Sweets'),
(9, 'Other');

-- ==================== 插入默认用户 ====================
-- 管理员账户
INSERT INTO CUSTOMER(id, address, email, password, role, username) VALUES
(1, '123, Albany Street', 'admin@nyan.cat', '123', 'ROLE_ADMIN', 'admin');

-- 普通用户账户
INSERT INTO CUSTOMER(id, address, email, password, role, username) VALUES
(2, '765, 5th Avenue', 'lisa@gmail.com', '765', 'ROLE_NORMAL', 'lisa');

-- ==================== 插入默认商品 ====================
INSERT INTO PRODUCT(product_id, description, image, name, price, quantity, weight, category_id) VALUES
(1, 'Fresh and juicy', 'https://freepngimg.com/save/9557-apple-fruit-transparent/744x744', 'Apple', 3, 40, 76, 1),
(2, 'Woops! There goes the eggs...', 'https://www.nicepng.com/png/full/813-8132637_poiata-bunicii-cracked-egg.png', 'Cracked Eggs', 1, 90, 43, 9);
