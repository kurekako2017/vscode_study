# AdminController 詳細設計書

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | AdminController 詳細設計書 |
| 対象クラス | `AdminController` |
| パッケージ | `com.jtspringproject.JtSpringProject.controller` |
| 作成日 | 2026-03-15 |
| 作成者 | Codex |

## 2. クラス概要

| 項目 | 内容 |
|---|---|
| 役割 | 管理者向けの認証、カテゴリ管理、商品管理、顧客一覧、プロフィール更新を制御する |
| 依存 | `UserService`、`CategoryService`、`ProductService` |
| セッション項目 | `adminLoggedIn`、`adminUsername` |
| パス接頭辞 | `/admin` |

## 3. メソッド一覧

| No | メソッド名 | HTTP / URL | 役割 |
|---|---|---|---|
| 1 | `adminlogin()` | `GET /admin/login` | 管理者ログイン画面表示 |
| 2 | `adminlogin(username, pass)` | `POST /admin/loginvalidate` | 管理者認証 |
| 3 | `adminHome()` | `GET /admin/Dashboard` | 管理者ホーム表示 |
| 4 | `getcategory()` | `GET /admin/categories` | カテゴリ一覧表示 |
| 5 | `addCategory()` | `POST /admin/categories` | カテゴリ追加 |
| 6 | `updateCategory()` | `GET /admin/categories/update` | カテゴリ更新 |
| 7 | `removeCategoryDb()` | `GET /admin/categories/delete` | カテゴリ削除 |
| 8 | `getproduct()` | `GET /admin/products` | 商品一覧表示 |
| 9 | `addProduct()` | `GET/POST /admin/products/add` | 商品登録画面 / 商品登録 |
| 10 | `updateproduct()` | `GET /admin/products/update/{id}` | 商品更新画面表示 |
| 11 | `updateProduct()` | `POST /admin/products/update/{id}` | 商品更新実行 |
| 12 | `removeProduct()` | `GET /admin/products/delete` | 商品削除 |
| 13 | `getCustomerDetail()` | `GET /admin/customers` | 顧客一覧表示 |
| 14 | `profileDisplay()` | `GET /admin/profileDisplay` | プロフィール表示 |
| 15 | `updateUserProfile()` | `POST /admin/updateuser` | プロフィール更新 |

## 4. メソッド詳細

### 4.1 `adminlogin(username, pass)`

処理手順:

1. ログイン画面から `username`、`password` を受領する。
2. `UserService.checkLogin()` で認証する。
3. 取得ユーザーが `ROLE_ADMIN` であることを確認する。
4. 成功時は Session に `adminLoggedIn=true`、`adminUsername` を設定する。
5. `adminHome` を返却する。
6. 失敗時は `adminlogin` にメッセージ設定して戻る。

### 4.2 `getcategory()`

処理手順:

1. Session から管理者ログイン状態を判定する。
2. 未ログイン時は `adminlogin` を返却する。
3. `CategoryService.getCategories()` で一覧取得する。
4. `categories` 画面へ一覧を設定する。

### 4.3 `addCategory()` / `updateCategory()` / `removeCategoryDb()`

業務ルール:

- カテゴリ管理は管理者ログイン前提で実施する。
- 追加はカテゴリ名を受領して新規作成する。
- 更新はカテゴリ ID 指定で名称変更する。
- 削除は対象 ID 指定で削除する。

### 4.4 `addProduct()`

処理手順:

1. 入力値として商品名、カテゴリ ID、価格、重量、数量、説明、画像を受領する。
2. `CategoryService.getCategory(categoryId)` でカテゴリ取得する。
3. `Product` オブジェクトを新規作成し、各属性を設定する。
4. `ProductService.addProduct()` で登録する。
5. 商品一覧へリダイレクトする。

### 4.5 `updateProduct()`

処理手順:

1. 対象商品 ID と更新値を受領する。
2. `CategoryService.getCategory()` でカテゴリ取得する。
3. `ProductService.getProduct(id)` で既存商品取得する。
4. 画像未入力時は既存画像を引き継ぐ。
5. 更新用 `Product` を組み立てて `ProductService.updateProduct()` を呼ぶ。
6. 商品一覧へリダイレクトする。

処理フロー図:

```mermaid
flowchart TD
    A[id と更新値受領] --> B[CategoryService.getCategory]
    B --> C[ProductService.getProduct]
    C --> D{既存商品有?}
    D -- No --> E[一覧へ戻る]
    D -- Yes --> F{画像入力有?}
    F -- No --> G[既存画像を引継ぐ]
    F -- Yes --> H[入力画像を採用]
    G --> I[更新用Product組立]
    H --> I
    I --> J[ProductService.updateProduct]
    J --> K[/admin/productsへリダイレクト]
```

### 4.6 `profileDisplay()` / `updateUserProfile()`

業務ルール:

- 現在ログイン中の管理者名は Session の `adminUsername` から取得する。
- `updateUserProfile()` は既存 `User` を取得後に上書き保存する。
- 更新後は Session の `adminUsername` も更新する。

## 5. 例外・注意事項

- GET で更新系操作を実施しているメソッドがあり、実案件では POST 化が望ましい。
- 認証チェックが各メソッド内に散在しているため、共通化余地がある。
- 一部コメントには JDBC 直叙があるが、現行実装は `UserService` 経由更新である。

## 6. 関連資料

- [15a_Controller詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15a_Controller詳細設計書.md)
- [17_URL一覧.md](../../../../JtProject/doc/jp-docs/03_database/17_URL一覧.md)
- [19_画面遷移図.md](../../../../JtProject/doc/jp-docs/01_design/19_画面遷移図.md)

