-- create the category table
CREATE TABLE IF NOT EXISTS CATEGORY(
category_id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255)
);

-- insert default categories
INSERT INTO CATEGORY(name) VALUES ('Fruits');
INSERT INTO CATEGORY(name) VALUES ('Vegetables');
INSERT INTO CATEGORY(name) VALUES ('Meat');
INSERT INTO CATEGORY(name) VALUES ('Fish');
INSERT INTO CATEGORY(name) VALUES ('Dairy');
INSERT INTO CATEGORY(name) VALUES ('Bakery');
INSERT INTO CATEGORY(name) VALUES ('Drinks');
INSERT INTO CATEGORY(name) VALUES ('Sweets');
INSERT INTO CATEGORY(name) VALUES ('Other');

-- create the customer table
CREATE TABLE IF NOT EXISTS CUSTOMER(
id INT PRIMARY KEY AUTO_INCREMENT,
address VARCHAR(255),
email VARCHAR(255),
password VARCHAR(255),
role VARCHAR(255),
username VARCHAR(255) UNIQUE
);

-- insert default customers
-- Check if 'admin' user exists before inserting
INSERT INTO CUSTOMER(address, email, password, role, username)
SELECT '123, Albany Street', 'admin@nyan.cat', '123', 'ROLE_ADMIN', 'admin'
WHERE NOT EXISTS (
    SELECT 1 FROM CUSTOMER WHERE username = 'admin'
);

-- Check if 'lisa' user exists before inserting
INSERT INTO CUSTOMER(address, email, password, role, username)
SELECT '765, 5th Avenue', 'lisa@gmail.com', '765', 'ROLE_NORMAL', 'lisa'
WHERE NOT EXISTS (
    SELECT 1 FROM CUSTOMER WHERE username = 'lisa'
);

-- create the product table
CREATE TABLE IF NOT EXISTS PRODUCT(
product_id INT PRIMARY KEY AUTO_INCREMENT,
description VARCHAR(255),
image VARCHAR(255),
name VARCHAR(255),
price INT,
quantity INT,
weight INT,
category_id INT,
customer_id INT
);

-- insert default products
INSERT INTO PRODUCT(description, image, name, price, quantity, weight, category_id) VALUES ('Fresh and juicy', 'https://freepngimg.com/save/9557-apple-fruit-transparent/744x744', 'Apple', 3, 40, 76, 1);
INSERT INTO PRODUCT(description, image, name, price, quantity, weight, category_id) VALUES ('Woops! There goes the eggs...', 'https://www.nicepng.com/png/full/813-8132637_poiata-bunicii-cracked-egg.png', 'Cracked Eggs', 1, 90, 43, 9);

-- create indexes
-- Drop existing indexes if they exist
SET @index_exists := (SELECT COUNT(1) FROM INFORMATION_SCHEMA.STATISTICS WHERE table_schema = 'ecommjava' AND table_name = 'PRODUCT' AND index_name = 'IDX_PRODUCT_CATEGORY');
IF @index_exists > 0 THEN
    ALTER TABLE PRODUCT DROP INDEX IDX_PRODUCT_CATEGORY;
END IF;
CREATE INDEX IDX_PRODUCT_CATEGORY ON PRODUCT (category_id);

SET @index_exists := (SELECT COUNT(1) FROM INFORMATION_SCHEMA.STATISTICS WHERE table_schema = 'ecommjava' AND table_name = 'PRODUCT' AND index_name = 'IDX_PRODUCT_CUSTOMER');
IF @index_exists > 0 THEN
    ALTER TABLE PRODUCT DROP INDEX IDX_PRODUCT_CUSTOMER;
END IF;
CREATE INDEX IDX_PRODUCT_CUSTOMER ON PRODUCT (customer_id);

-- create cart table
CREATE TABLE IF NOT EXISTS CART(
id INT PRIMARY KEY AUTO_INCREMENT,
customer_id INT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
);

-- create cart_product table
CREATE TABLE IF NOT EXISTS CART_PRODUCT (
id INT PRIMARY KEY AUTO_INCREMENT,
cart_id INT NOT NULL,
product_id INT NOT NULL,
FOREIGN KEY (cart_id) REFERENCES CART(id),
FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
);
