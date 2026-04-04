# Model 詳細設計書

## 1. 目的

本書は Model / Entity 層の詳細設計を整理する。  
対象は属性、テーブル対応、関連、業務上の意味である。

## 2. 対象クラス

| クラス名 | 対応テーブル | 役割 |
|---|---|---|
| `User` | `CUSTOMER` | 顧客、管理者情報 |
| `Category` | `CATEGORY` | 商品カテゴリ |
| `Product` | `PRODUCT` | 商品情報 |
| `Cart` | `CART` | 顧客別カート |
| `CartProduct` | `CART_PRODUCT` | カート商品明細 |

## 2.1 クラス別文書

- [15d-01_User詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-01_User詳細設計書.md)
- [15d-02_Product詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-02_Product詳細設計書.md)
- [15d-03_Category詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-03_Category詳細設計書.md)
- [15d-04_Cart詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-04_Cart詳細設計書.md)
- [15d-05_CartProduct詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-05_CartProduct詳細設計書.md)

## 2.2 クラス単位文書の読書順

推奨順:

1. [15d-01_User詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-01_User詳細設計書.md)
2. [15d-03_Category詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-03_Category詳細設計書.md)
3. [15d-02_Product詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-02_Product詳細設計書.md)
4. [15d-04_Cart詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-04_Cart詳細設計書.md)
5. [15d-05_CartProduct詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15d-05_CartProduct詳細設計書.md)

読書観点:

- まず利用者主体の `User` を読み、ロールや認証対象の前提を押さえる。
- 次に `Category` と `Product` を読み、商品系マスタと業務エンティティの関係を把握する。
- 最後に `Cart` と `CartProduct` を読み、購買導線の親子関係と中間テーブル構成を理解する。
- Model 層を読んだ後は [11_ER図.md](../../../../JtProject/doc/jp-docs/03_database/11_ER図.md) と [22_クラス図・処理フロー図.md](../../../../JtProject/doc/jp-docs/01_design/22_クラス図・処理フロー図.md) を参照する。

## 3. User

| 項目 | 内容 |
|---|---|
| クラス名 | `User` |
| 対応テーブル | `CUSTOMER` |
| 主な属性 | `id`, `username`, `email`, `password`, `role`, `address` |
| 業務上の意味 | 一般ユーザー、管理者の両方を表す |

### 利用場面

- ログイン認証
- ユーザー登録
- 管理者プロフィール更新
- 顧客一覧表示

## 4. Category

| 項目 | 内容 |
|---|---|
| クラス名 | `Category` |
| 対応テーブル | `CATEGORY` |
| 主な属性 | `id`, `name` |
| 業務上の意味 | 商品分類マスタ |

### 利用場面

- カテゴリ一覧表示
- 商品登録・更新時の選択肢
- 商品分類管理

## 5. Product

| 項目 | 内容 |
|---|---|
| クラス名 | `Product` |
| 対応テーブル | `PRODUCT` |
| 主な属性 | `productId`, `name`, `image`, `quantity`, `price`, `weight`, `description`, `category`, `customer` |
| 業務上の意味 | 商品一覧、商品管理、カート投入対象 |

### 利用場面

- 商品一覧表示
- 商品登録、更新、削除
- カート表示

### 補足

- `category` と関連を持つ
- `customer_id` の用途は現状資料上でも要整理事項として残る

## 6. Cart

| 項目 | 内容 |
|---|---|
| クラス名 | `Cart` |
| 対応テーブル | `CART` |
| 主な属性 | `id`, `customer` |
| 業務上の意味 | 顧客ごとのカートヘッダ |

### 利用場面

- カート存在判定
- 新規カート作成
- カート表示時の親単位

## 7. CartProduct

| 項目 | 内容 |
|---|---|
| クラス名 | `CartProduct` |
| 対応テーブル | `CART_PRODUCT` |
| 主な属性 | `id`, `cart`, `product` |
| 業務上の意味 | カートと商品の中間明細 |

### 利用場面

- カート商品追加
- カート商品削除
- カート商品一覧生成

## 8. Model 層共通設計観点

- Model は Controller 画面データと DB エンティティの両面で使われている。
- 入出力専用 DTO と Entity の分離は行っていない。
- 実案件では監査項目、論理削除、作成者更新者などの共通カラム追加余地がある。

関連資料:

- [11_ER図.md](../../../../JtProject/doc/jp-docs/03_database/11_ER図.md)
- [16_テーブル定義書.md](../../../../JtProject/doc/jp-docs/03_database/16_テーブル定義書.md)

