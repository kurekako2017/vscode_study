# Controller 詳細設計書

## 1. 目的

本書は Controller 層の詳細設計を整理する。  
対象は画面要求受付、入力受領、セッション制御、画面遷移、Service 呼出である。

## 2. 対象クラス

| クラス名 | 役割 | 主な対象画面 |
|---|---|---|
| `UserController` | 一般ユーザー向け画面制御 | ログイン、登録、商品一覧、カート |
| `AdminController` | 管理者向け画面制御 | 管理者ログイン、カテゴリ管理、商品管理、顧客一覧、プロフィール更新 |

## 2.1 クラス別文書

- [15a-01_UserController詳細設計書.md](15a-01_UserController詳細設計書.md)
- [15a-02_AdminController詳細設計書.md](15a-02_AdminController詳細設計書.md)

## 2.2 クラス単位文書の読書順

推奨順:

1. [15a-01_UserController詳細設計書.md](15a-01_UserController詳細設計書.md)
2. [15a-02_AdminController詳細設計書.md](15a-02_AdminController詳細設計書.md)

読書観点:

- 先に一般ユーザー導線を確認し、画面遷移とリクエスト処理の基本形を把握する。
- 次に管理者導線を確認し、商品管理、カテゴリ管理、顧客管理の差分を追う。
- Controller 層を読んだ後は [15b_Service詳細設計書.md](15b_Service詳細設計書.md) へ進む。

## 3. UserController

| 項目 | 内容 |
|---|---|
| クラス名 | `UserController` |
| パッケージ | `controller` |
| 役割 | 一般ユーザー向けの認証、商品表示、カート操作、登録処理 |
| 依存 | `UserService`、`ProductService`、`CartService`、`CartProductDao` |
| セッション | `username`、`userRole`、`cartMsg` |
| Cookie | `username` |

### 3.1 主なメソッド

| メソッド | HTTP / URL | 役割 |
|---|---|---|
| `userloginPage()` | `GET /` | ログイン画面初期表示、既存ログイン情報補完 |
| `userlogin()` | `POST /userloginvalidate1` | ログイン認証本体 |
| `userloginAlias()` | `POST /userloginvalidate` | 旧 URL 互換用エイリアス |
| `newUseRegister()` | `POST /newuserregister` | 一般ユーザー新規登録 |
| `getproduct()` | `GET /user/products` | 商品一覧表示 |
| `indexPage()` | `GET /index` | トップ画面表示 |
| `addToCart()` | `GET/POST /products/addtocart` | カート追加 |
| `showCart()` | `GET /user/cart` | カート表示 |
| `deleteFromCart()` | `GET /user/cart/delete` | カート内商品削除 |
| `logout()` | `GET /logout` | ログアウト |

### 3.2 業務ロジック概要

#### ログイン処理

1. 画面から `username`、`password` を受領する。
2. `UserService.checkLogin()` を呼び出す。
3. 戻り値 `User` の `id > 0` かつ `username` 一致を成功条件とする。
4. 成功時は Cookie、Session を設定し、商品一覧付きで `index` へ遷移する。
5. 失敗時は `userLogin` へ戻り、エラーメッセージを設定する。

#### ユーザー登録処理

1. `User` モデルを受領する。
2. `UserService.checkUserExists()` で重複確認する。
3. 未登録であれば `ROLE_NORMAL` を設定して保存する。
4. 重複時は登録画面へ戻し、メッセージを表示する。

#### カート追加処理

1. Cookie / Session からログインユーザー名を解決する。
2. `UserService.getUserByUsername()` でユーザーを取得する。
3. 管理者の場合はカート利用不可として管理画面へ誘導する。
4. 既存カートを検索し、なければ新規作成する。
5. `ProductService.getProduct()` で商品存在を確認する。
6. `CartProductDao.addCartProduct()` で明細追加する。
7. 結果メッセージを Session に設定してカート画面へ遷移する。

### 3.3 設計上の注意

- 認証結果は `null` ではなく空 `User` が返る実装を前提にしている箇所がある。
- 一般ユーザー系では Cookie と Session を併用している。
- 例外時も極力画面異常終了させず、画面メッセージへ変換している。

## 4. AdminController

| 項目 | 内容 |
|---|---|
| クラス名 | `AdminController` |
| パッケージ | `controller` |
| 役割 | 管理者認証、カテゴリ管理、商品管理、顧客一覧、プロフィール更新 |
| 依存 | `UserService`、`CategoryService`、`ProductService` |
| セッション | `adminLoggedIn`、`adminUsername` |
| パス接頭辞 | `/admin` |

### 4.1 主なメソッド

| メソッド | HTTP / URL | 役割 |
|---|---|---|
| `adminlogin()` | `GET /admin/login` | 管理者ログイン画面表示 |
| `adminlogin(username, pass)` | `POST /admin/loginvalidate` | 管理者ログイン認証 |
| `adminHome()` | `GET /admin/Dashboard` | 管理者ホーム表示 |
| `getcategory()` | `GET /admin/categories` | カテゴリ一覧表示 |
| `addCategory()` | `POST /admin/categories` | カテゴリ追加 |
| `updateCategory()` | `GET /admin/categories/update` | カテゴリ更新 |
| `removeCategoryDb()` | `GET /admin/categories/delete` | カテゴリ削除 |
| `getproduct()` | `GET /admin/products` | 商品一覧表示 |
| `addProduct()` | `GET/POST /admin/products/add` | 商品登録画面 / 登録実行 |
| `updateproduct()` | `GET /admin/products/update/{id}` | 商品更新画面表示 |
| `updateProduct()` | `POST /admin/products/update/{id}` | 商品更新実行 |
| `removeProduct()` | `GET /admin/products/delete` | 商品削除 |
| `getCustomerDetail()` | `GET /admin/customers` | 顧客一覧表示 |
| `profileDisplay()` | `GET /admin/profileDisplay` | 管理者プロフィール表示 |
| `updateUserProfile()` | `POST /admin/updateuser` | 管理者プロフィール更新 |

### 4.2 業務ロジック概要

#### 管理者ログイン

1. `UserService.checkLogin()` を利用してユーザー認証する。
2. `role == ROLE_ADMIN` の場合のみ成功とする。
3. 成功時は `adminLoggedIn=true`、`adminUsername` を Session に設定する。
4. 失敗時は `adminlogin` にメッセージ付きで戻る。

#### カテゴリ管理

1. 一覧表示前に管理者ログイン状態を判定する。
2. `CategoryService.getCategories()` で一覧取得する。
3. 追加、更新、削除は `CategoryService` 経由で実施する。

#### 商品管理

1. 商品登録時はカテゴリ ID から `Category` を取得する。
2. 画面入力値を `Product` オブジェクトへ詰め替える。
3. 更新時は既存画像が未入力なら旧画像を維持する。
4. 削除時は商品 ID 指定で削除する。

#### プロフィール更新

1. Session 上の `adminUsername` から現在ユーザーを特定する。
2. 入力値を既存 `User` に上書きする。
3. `UserService.addUser()` を再利用して更新する。
4. 更新後は Session の `adminUsername` も更新する。

### 4.3 設計上の注意

- 管理者系は Cookie ではなく Session 中心で制御している。
- 一部 GET で更新系操作を行っているため、実案件では POST 化検討余地がある。
- 認証チェックの有無がメソッドごとにばらつくため、共通化余地がある。

## 5. Controller 層共通設計観点

- 入力値妥当性は現状 Controller と Service に分散している。
- 画面メッセージは `msg`、`cartMsg` を利用する実装が多い。
- 権限制御は Session 判定ベースである。
- 詳細な呼出順序は [20_シーケンス図.md](../01_design/20_シーケンス図.md) を参照する。

