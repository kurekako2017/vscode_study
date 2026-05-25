# Service 詳細設計書

## 1. 目的

本書は Service 層の詳細設計を整理する。  
対象は業務ロジック、判定条件、DAO 呼出、戻り値制御である。

## 2. 対象クラス

| インタフェース | 実装クラス | 主な役割 |
|---|---|---|
| `UserService` | `UserServiceImpl` | ユーザー認証、登録、取得、重複チェック |
| `ProductService` | `ProductServiceImpl` | 商品一覧、詳細、登録、更新、削除 |
| `CategoryService` | `CategoryServiceImpl` | カテゴリ一覧、追加、更新、削除 |
| `CartService` | `CartServiceImpl` | カート一覧、追加、取得 |

## 2.1 クラス別文書

- [15b-01_UserService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-01_UserService詳細設計書.md)
- [15b-02_ProductService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-02_ProductService詳細設計書.md)
- [15b-03_CategoryService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-03_CategoryService詳細設計書.md)
- [15b-04_CartService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-04_CartService詳細設計書.md)

## 2.2 クラス単位文書の読書順

推奨順:

1. [15b-01_UserService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-01_UserService詳細設計書.md)
2. [15b-02_ProductService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-02_ProductService詳細設計書.md)
3. [15b-03_CategoryService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-03_CategoryService詳細設計書.md)
4. [15b-04_CartService詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15b-04_CartService詳細設計書.md)

読書観点:

- 先に認証と利用者判定を持つ `UserService` を読む。
- 次に商品、カテゴリの主業務を読み、一覧取得と更新系の流れを把握する。
- 最後にカート系を読み、購買導線における周辺処理を理解する。
- Service 層を読んだ後は [15c_DAO詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c_DAO詳細設計書.md) へ進む。

## 3. UserService / UserServiceImpl

| 項目 | 内容 |
|---|---|
| 役割 | ユーザー認証、取得、登録、重複判定 |
| 呼出元 | `UserController`、`AdminController` |
| 委譲先 | `UserDao` |
| 主な戻り値 | `User`、`List<User>`、`boolean` |

### 主なメソッド

| メソッド | 役割 |
|---|---|
| `getUsers()` | 顧客一覧取得 |
| `addUser()` | 顧客追加または更新 |
| `checkLogin()` | ログイン認証 |
| `getUserByUsername()` | ユーザー名で顧客取得 |
| `getUserById()` | ID で顧客取得 |
| `checkUserExists()` | ユーザー名重複チェック |

### 業務ロジック

- `checkLogin()` は `UserDao.getUser()` を呼び出し、`id > 0` を成功条件の基準として扱う。
- `addUser()` は新規登録と更新の両方に使われる。
- `checkUserExists()` は登録前チェックとして利用する。
- 管理者プロフィール更新でも `addUser()` を再利用する。

## 4. ProductService / ProductServiceImpl

| 項目 | 内容 |
|---|---|
| 役割 | 商品参照、登録、更新、削除 |
| 呼出元 | `UserController`、`AdminController` |
| 委譲先 | `ProductDao` |

### 主なメソッド

| メソッド | 役割 |
|---|---|
| `getProducts()` | 商品一覧取得 |
| `getProduct(id)` | 商品詳細取得 |
| `addProduct(product)` | 商品登録 |
| `updateProduct(id, product)` | 商品更新 |
| `deleteProduct(id)` | 商品削除 |

### 業務ロジック

- 一覧表示系は DB から取得した商品一覧をそのまま返す。
- 更新時は呼出元から受領した `Product` に対し、対象 ID を紐付けて更新する。
- 画像未入力時の既存画像保持は主に Controller 側で補完している。

## 5. CategoryService / CategoryServiceImpl

| 項目 | 内容 |
|---|---|
| 役割 | カテゴリ参照、追加、更新、削除 |
| 呼出元 | `AdminController` |
| 委譲先 | `CategoryDao` |

### 主なメソッド

| メソッド | 役割 |
|---|---|
| `getCategories()` | カテゴリ一覧取得 |
| `getCategory(id)` | カテゴリ詳細取得 |
| `addCategory(name)` | カテゴリ追加 |
| `updateCategory(id, name)` | カテゴリ更新 |
| `deleteCategory(id)` | カテゴリ削除 |

### 業務ロジック

- 追加時はカテゴリ名を受領し、新規 `Category` を作成して保存する。
- 更新時は対象カテゴリ存在を前提に名称更新する。
- 削除時は対象 ID 指定で削除する。

## 6. CartService / CartServiceImpl

| 項目 | 内容 |
|---|---|
| 役割 | カート一覧取得、カート作成、カート取得 |
| 呼出元 | `UserController` |
| 委譲先 | `CartDao` |

### 主なメソッド

| メソッド | 役割 |
|---|---|
| `getCarts()` | 全カート取得 |
| `addCart(cart)` | 新規カート保存 |
| `updateCart(cart)` | カート更新 |
| `deleteCart(cart)` | カート削除 |

### 業務ロジック

- カート自体の存在判定は Controller 側で全件走査により実施している。
- カート未存在時に新規作成する際の窓口として利用する。
- 明細追加削除の前段となるカートヘッダ管理を担当する。

## 7. Service 層共通設計観点

- Service 層は Controller と DAO の仲介だけでなく、認証成否や重複可否などの業務判断も持つ。
- 例外はログ出力後に再送出する実装が多い。
- 実案件ではトランザクション境界、入力妥当性、共通例外変換を Service 層へさらに集約する余地がある。

関連資料:

- [13_機能設計書.md](../../../../JtProject/doc/jp-docs/01_design/13_機能設計書.md)
- [15c_DAO詳細設計書.md](../../../../JtProject/doc/jp-docs/02_class-design/15c_DAO詳細設計書.md)

