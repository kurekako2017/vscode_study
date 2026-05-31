# DDL一覧

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DDL一覧 |
| 対象システム | JtProject |
| 作成日 | 2026-03-15 |
| 作成者 | Codex |
| 関連資料 | `11_ER図.md`、`12_データベース一覧表.md`、`16_テーブル定義書.md`、`28_変更履歴一覧.md` |

## 2. 目的

本書は、主要テーブルの作成定義を DDL 形式で整理し、開発・レビュー・DB 構築時の参照資料とするものである。

## 3. 前提

- 本資料は学習用プロジェクト `JtProject-Next` のエンティティ定義および既存テーブル定義書をもとに整理した論理 DDL である。
- DB 製品差異により、自動採番や文字列型、制約名は環境に応じて調整が必要である。
- ここでは可読性を優先し、一般的な SQL 記法で記載する。

## 4. テーブル作成 DDL

### 4.1 CUSTOMER

用途: 顧客情報管理、ログイン認証、権限判定に使用

```sql
CREATE TABLE CUSTOMER (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(200),
    password VARCHAR(255),
    role VARCHAR(50),
    address VARCHAR(255)
);
```

### 4.2 CATEGORY

用途: 商品カテゴリ管理に使用

```sql
CREATE TABLE CATEGORY (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);
```

### 4.3 PRODUCT

用途: 商品情報管理、商品一覧表示、商品管理に使用

```sql
CREATE TABLE PRODUCT (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200),
    image VARCHAR(255),
    quantity INT,
    price INT,
    weight INT,
    description VARCHAR(500),
    category_id INT,
    customer_id INT,
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES CATEGORY(category_id),
    CONSTRAINT fk_product_customer
        FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
);
```

### 4.4 CART

用途: 顧客ごとのカートヘッダ管理に使用

```sql
CREATE TABLE CART (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    CONSTRAINT fk_cart_customer
        FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id)
);
```

### 4.5 CART_PRODUCT

用途: カート内商品明細管理に使用

```sql
CREATE TABLE CART_PRODUCT (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    CONSTRAINT fk_cart_product_cart
        FOREIGN KEY (cart_id) REFERENCES CART(id),
    CONSTRAINT fk_cart_product_product
        FOREIGN KEY (product_id) REFERENCES PRODUCT(product_id)
);
```

## 5. インデックス・制約方針

| テーブル | 項目 | 種別 | 目的 |
|---|---|---|---|
| `CUSTOMER` | `id` | PK | 顧客識別 |
| `CUSTOMER` | `username` | UK | ログイン ID 重複防止 |
| `CATEGORY` | `category_id` | PK | カテゴリ識別 |
| `PRODUCT` | `product_id` | PK | 商品識別 |
| `PRODUCT` | `category_id` | FK | カテゴリ紐付け |
| `PRODUCT` | `customer_id` | FK | 登録者または関連顧客紐付け |
| `CART` | `id` | PK | カート識別 |
| `CART` | `customer_id` | FK | 顧客紐付け |
| `CART_PRODUCT` | `id` | PK | 明細識別 |
| `CART_PRODUCT` | `cart_id` | FK | カート紐付け |
| `CART_PRODUCT` | `product_id` | FK | 商品紐付け |

## 6. 初期データ投入用サンプル DML

### 6.1 CUSTOMER

```sql
INSERT INTO CUSTOMER (username, email, password, role, address)
VALUES ('admin01', 'admin@example.com', 'admin01', 'ROLE_ADMIN', 'Tokyo'),
       ('user01', 'user01@example.com', 'pass01', 'ROLE_NORMAL', 'Osaka');
```

### 6.2 CATEGORY

```sql
INSERT INTO CATEGORY (name)
VALUES ('PC'), ('Book'), ('Accessory');
```

### 6.3 PRODUCT

```sql
INSERT INTO PRODUCT (name, image, quantity, price, weight, description, category_id, customer_id)
VALUES ('Laptop A', 'laptop-a.jpg', 10, 120000, 1800, 'Business laptop', 1, 1),
       ('Java Book', 'java-book.jpg', 25, 3800, 700, 'Java learning book', 2, 1);
```

## 7. DDL 運用上の注意

- `AUTO_INCREMENT` は MySQL 系を想定しているため、H2 利用時は `IDENTITY` など環境に応じて読み替える。
- 実案件では `NOT NULL`、デフォルト値、インデックス名、コメント句、監査カラムを追加する。
- パスワード平文保持は学習用前提であり、本番ではハッシュ化が必須である。
- `PRODUCT.customer_id` の扱いは業務定義に応じて再確認する。

## 8. 補足

- 本書は構築用 SQL の基礎資料であり、実 DB 反映前に `16_テーブル定義書.md` と差異がないことを確認する。
- 物理名、制約名、桁数を正式化する場合は DBA レビューを実施する。
