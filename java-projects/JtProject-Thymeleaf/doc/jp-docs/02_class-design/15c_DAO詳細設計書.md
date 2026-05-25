# DAO 詳細設計書

## 1. 目的

本書は DAO 層の詳細設計を整理する。  
対象は DB アクセス方式、検索条件、更新対象、戻り値、業務上の注意点である。

## 2. 対象クラス

| インタフェース | 実装クラス | 主な対象テーブル |
|---|---|---|
| `UserDao` | `UserDaoImpl` | `CUSTOMER` |
| `ProductDao` | `ProductDaoImpl` | `PRODUCT` |
| `CategoryDao` | `CategoryDaoImpl` | `CATEGORY` |
| `CartDao` | `CartDaoImpl` | `CART` |
| `CartProductDao` | `CartProductDaoImpl` | `CART_PRODUCT` |

## 2.1 クラス別文書

- [15c-01_UserDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-01_UserDao詳細設計書.md)
- [15c-02_ProductDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-02_ProductDao詳細設計書.md)
- [15c-03_CategoryDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-03_CategoryDao詳細設計書.md)
- [15c-04_CartDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-04_CartDao詳細設計書.md)
- [15c-05_CartProductDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-05_CartProductDao詳細設計書.md)

## 2.2 クラス単位文書の読書順

推奨順:

1. [15c-01_UserDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-01_UserDao詳細設計書.md)
2. [15c-02_ProductDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-02_ProductDao詳細設計書.md)
3. [15c-03_CategoryDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-03_CategoryDao詳細設計書.md)
4. [15c-04_CartDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-04_CartDao詳細設計書.md)
5. [15c-05_CartProductDao詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c-05_CartProductDao詳細設計書.md)

読書観点:

- `UserDao` で基本的な Hibernate アクセスと認証系取得方針を把握する。
- 次に商品、カテゴリの CRUD を読み、マスタ系 DB アクセスを理解する。
- 最後に `Cart`、`CartProduct` を読み、購買系の親子構造と明細取得ロジックを追う。
- DAO 層を読んだ後は [15d_Model詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d_Model詳細設計書.md) と [16_テーブル定義書.md](../../../../JtProject/doc/jp-docs/03_database/16_テーブル定義書.md) を参照する。

## 3. UserDao / UserDaoImpl

| 項目 | 内容 |
|---|---|
| 役割 | 顧客一覧取得、保存、ログイン照合、重複判定 |
| アクセス技術 | Hibernate `SessionFactory` |
| 対象 | `CUSTOMER` |

### 主なメソッド

| メソッド | 処理概要 |
|---|---|
| `getAllUser()` | 顧客全件取得 |
| `saveUser(user)` | 顧客保存または更新 |
| `getUser(username, password)` | ユーザー名検索 + Java 側パスワード照合 |
| `getUserByUsername(username)` | ユーザー名検索 |
| `getUserById(id)` | 主キー取得 |
| `userExists(username)` | 件数ベース重複判定 |

### DB ロジック

- `getAllUser()` は `from User` の HQL で全件取得する。
- `saveUser()` は `saveOrUpdate()` を利用し、新規・更新を兼用する。
- `getUser()` は `username` で検索後、Java 側でパスワード比較を行う。
- 該当なしまたはパスワード不一致時は `new User()` を返す実装である。
- `userExists()` は `COUNT` により重複有無を返す。

## 4. ProductDao / ProductDaoImpl

| 項目 | 内容 |
|---|---|
| 役割 | 商品 CRUD |
| アクセス技術 | Hibernate `SessionFactory` |
| 対象 | `PRODUCT` |

### 主なメソッド

| メソッド | 処理概要 |
|---|---|
| `getProducts()` | 商品全件取得 |
| `getProduct(id)` | 商品 1 件取得 |
| `addProduct(product)` | 商品追加 |
| `updateProduct(product)` | 商品更新 |
| `deletProduct(id)` | 商品削除 |

### DB ロジック

- 商品一覧は全件取得ベースである。
- 追加は `save`、更新は `update`、削除は対象取得後削除の形を取る。
- 実案件では論理削除や在庫更新履歴管理の追加余地がある。

## 5. CategoryDao / CategoryDaoImpl

| 項目 | 内容 |
|---|---|
| 役割 | カテゴリ CRUD |
| アクセス技術 | `EntityManager` |
| 対象 | `CATEGORY` |

### 主なメソッド

| メソッド | 処理概要 |
|---|---|
| `getCategories()` | カテゴリ全件取得 |
| `getCategory(id)` | カテゴリ取得 |
| `addCategory(name)` | カテゴリ追加 |
| `updateCategory(id, name)` | カテゴリ更新 |
| `deletCategory(id)` | カテゴリ削除 |

### DB ロジック

- 追加時は `persist` を用いる。
- 更新時は対象取得後に属性を変更し `merge` する。
- 不存在更新は例外処理対象となる。

## 6. CartDao / CartDaoImpl

| 項目 | 内容 |
|---|---|
| 役割 | カートヘッダ取得、保存 |
| アクセス技術 | Hibernate / JPA |
| 対象 | `CART` |

### 主なメソッド

| メソッド | 処理概要 |
|---|---|
| `getCarts()` | カート全件取得 |
| `addCart(cart)` | カート追加 |
| `updateCart(cart)` | カート更新 |
| `deleteCart(cart)` | カート削除 |

### DB ロジック

- 顧客単位カート取得を専用メソッドで持たず、上位層で全件から絞り込む設計である。
- 実案件では `customer_id` 指定取得メソッドを追加した方が効率的である。

## 7. CartProductDao / CartProductDaoImpl

| 項目 | 内容 |
|---|---|
| 役割 | カート明細追加、取得、削除 |
| アクセス技術 | Hibernate / JPA |
| 対象 | `CART_PRODUCT` |

### 主なメソッド

| メソッド | 処理概要 |
|---|---|
| `addCartProduct(cp)` | カート商品明細追加 |
| `getCartProducts()` | カート商品明細全件取得 |
| `getProductByCartID(cartId)` | カート ID から商品一覧取得 |
| `updateCartProduct(cp)` | カート商品明細更新 |
| `getCartProductsByCartAndProductId(cartId, productId)` | 明細特定 |
| `getCartProductsByProductId(productId)` | 商品 ID 指定明細取得 |
| `deleteCartProduct(cp)` | 明細削除 |

### DB ロジック

- カート画面表示時はカート明細から商品一覧を再構成する。
- 削除時は `cartId` と `productId` の組み合わせで対象明細を絞り込む。
- 実案件では数量カラム追加や重複明細統合ロジックが必要となる。

## 8. DAO 層共通設計観点

- 例外処理方式と戻り値ポリシーにばらつきがある。
- `UserDao.getUser()` のように `null` ではなく空オブジェクトを返す実装が存在する。
- HQL / SessionFactory / EntityManager が混在しているため、統一余地がある。
- 詳細なテーブル構造は [16_テーブル定義書.md](../../../../JtProject/doc/jp-docs/03_database/16_テーブル定義書.md) と [27_DDL一覧.md](../../../../JtProject/doc/jp-docs/03_database/27_DDL一覧.md) を参照する。

