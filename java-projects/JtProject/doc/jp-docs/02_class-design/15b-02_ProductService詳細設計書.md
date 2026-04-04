# ProductService 詳細設計書

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | ProductService 詳細設計書 |
| 対象クラス | `ProductService` / `ProductServiceImpl` |
| パッケージ | `services` / `services.impl` |
| 作成日 | 2026-03-15 |
| 作成者 | Codex |

## 2. クラス概要

| 項目 | 内容 |
|---|---|
| 役割 | 商品一覧取得、商品詳細取得、商品追加、更新、削除を担当する |
| 呼出元 | `UserController`、`AdminController` |
| 委譲先 | `ProductDao` |
| 主な戻り値 | `List<Product>`、`Product`、`boolean` |

## 3. メソッド一覧

| No | メソッド名 | 役割 |
|---|---|---|
| 1 | `getProducts()` | 商品一覧取得 |
| 2 | `addProduct(product)` | 商品登録 |
| 3 | `getProduct(id)` | 商品詳細取得 |
| 4 | `updateProduct(id, product)` | 商品更新 |
| 5 | `deleteProduct(id)` | 商品削除 |

## 4. メソッド詳細

### 4.1 `getProducts()`

処理手順:

1. `ProductDao.getProducts()` を呼び出す。
2. 商品一覧を受領する。
3. 取得件数をログ出力する。
4. 一覧を返却する。

利用場面:

- トップ画面表示
- 商品一覧表示
- 管理者商品一覧表示

### 4.2 `addProduct(product)`

処理手順:

1. `Product` オブジェクトを受領する。
2. `ProductDao.addProduct(product)` を呼び出す。
3. 保存結果の `Product` を返却する。

業務ルール:

- カテゴリ設定済み商品を受け取る前提である。
- 入力値妥当性や画像の扱いは主に Controller 側で調整される。

### 4.3 `getProduct(id)`

処理手順:

1. `ProductDao.getProduct(id)` を呼び出す。
2. 取得結果があれば詳細を返却する。
3. 該当なしの場合は `null` を返却する。

利用場面:

- 商品更新画面表示
- カート追加前の商品存在確認

### 4.4 `updateProduct(id, product)`

処理手順:

1. 更新対象 ID と `Product` を受領する。
2. `product.setId(id)` により更新対象 ID を設定する。
3. `ProductDao.updateProduct(product)` を呼び出す。
4. 更新結果を返却する。

業務ルール:

- 画像未入力時の既存画像維持は Controller 側で実施する。
- Service 層は更新対象 ID と商品オブジェクトの整合を取る役割を持つ。

処理フロー図:

```mermaid
flowchart TD
    A[id と Product受領] --> B[product.setId(id)]
    B --> C[ProductDao.updateProduct]
    C --> D[更新済Product受領]
    D --> E[結果返却]
```

### 4.5 `deleteProduct(id)`

処理手順:

1. `ProductDao.deletProduct(id)` を呼び出す。
2. 削除結果 `boolean` を返却する。

利用場面:

- 管理者商品削除

## 5. 設計上の注意

- Service 層としての加工は比較的薄く、DAO への委譲が中心である。
- 実案件では登録更新時の業務チェック、トランザクション制御、画像ファイル管理を Service 層へ集約する余地がある。

## 6. 関連資料

- [15b_Service詳細設計書.md](15b_Service詳細設計書.md)
- [15c-02_ProductDao詳細設計書.md](15c-02_ProductDao詳細設計書.md)

