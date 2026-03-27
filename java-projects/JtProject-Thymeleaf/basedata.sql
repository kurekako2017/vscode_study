# SQL configs
SET SQL_MODE ='IGNORE_SPACE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

# drop the database if it exists
DROP DATABASE IF EXISTS ecommjava;

# create database and use it
CREATE DATABASE IF NOT EXISTS ecommjava;
USE ecommjava;

# drop existing tables if they exist
DROP TABLE IF EXISTS ORDER_PRODUCT;
DROP TABLE IF EXISTS `ORDER`;
DROP TABLE IF EXISTS CART_PRODUCT;
DROP TABLE IF EXISTS PRODUCT;
DROP TABLE IF EXISTS CUSTOMER;
DROP TABLE IF EXISTS CATEGORY;

# recreate the tables
CREATE TABLE IF NOT EXISTS CATEGORY(
    category_id int unique key not null auto_increment primary key,
    name varchar(255) null
);

# insert default categories
INSERT INTO CATEGORY(name) VALUES ('Fruits'),
                                  ('Vegetables'),
                                  ('Meat'),
                                  ('Fish'),
                                  ('Dairy'),
                                  ('Bakery'),
                                  ('Drinks'),
                                  ('Sweets'),
                                  ('Other');

CREATE TABLE IF NOT EXISTS CUSTOMER(
    id int unique key not null auto_increment primary key,
    address varchar(255) null,
    email varchar(255) null,
    password varchar(255) null,
    role varchar(255) null,
    username varchar(255) null,
    UNIQUE (username)
);

INSERT INTO CUSTOMER(address, email, password, role, username) VALUES
    ('123, Albany Street', 'admin@nyan.cat', '123', 'ROLE_ADMIN', 'admin'),
    ('765, 5th Avenue', 'lisa@gmail.com', '765', 'ROLE_NORMAL', 'lisa');

CREATE TABLE IF NOT EXISTS PRODUCT(
    product_id int unique key not null auto_increment primary key,
    description varchar(255) null,
    image varchar(255) null,
    name varchar(255) null,
    price int null,
    quantity int null,
    weight int null,
    category_id int null,
    customer_id int null
);

INSERT INTO PRODUCT(description, image, name, price, quantity, weight, category_id) VALUES
    ('Fresh and juicy', 'https://freepngimg.com/save/9557-apple-fruit-transparent/744x744', 'Apple', 3, 40, 76, 1),
    ('Woops! There goes the eggs...', 'https://www.nicepng.com/png/full/813-8132637_poiata-bunicii-cracked-egg.png', 'Cracked Eggs', 1, 90, 43, 9);

CREATE INDEX FK7u438kvwr308xcwr4wbx36uiw ON PRODUCT (category_id);
CREATE INDEX FKt23apo8r9s2hse1dkt95ig0w5 ON PRODUCT (customer_id);

CREATE TABLE IF NOT EXISTS CART_PRODUCT(
    cart_id int unique key not null auto_increment primary key,
    product_id int not null,
    customer_id int not null,
    quantity int not null,
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
);

CREATE TABLE IF NOT EXISTS `ORDER`(
    order_id int unique key not null auto_increment primary key,
    customer_id int not null,
    total_price decimal(10, 2) not null,
    status varchar(50) not null,
    created_at datetime default current_timestamp,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
);

CREATE TABLE IF NOT EXISTS ORDER_PRODUCT(
    order_product_id int unique key not null auto_increment primary key,
    order_id int not null,
    product_id int not null,
    quantity int not null,
    price decimal(10, 2) not null,
    FOREIGN KEY (order_id) REFERENCES `ORDER`(order_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
);
