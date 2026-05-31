# URL一覧

## 1. 目的

本書は `JtProject-Next` の URL、HTTP メソッド、用途、担当 Controller を一覧化する。

## 2. URL 一覧

| No | Method | URL | 用途 | Controller |
|---|---|---|---|---|
| 1 | GET | `/` | ユーザーログイン画面表示 | `UserController.userloginPage()` |
| 2 | POST | `/userloginvalidate` | ユーザーログイン認証 | `UserController.userloginAlias()` |
| 3 | POST | `/userloginvalidate1` | ユーザーログイン認証本体 | `UserController.userlogin()` |
| 4 | GET | `/register` | ユーザー登録画面表示 | `UserController.registerUser()` |
| 5 | POST | `/newuserregister` | ユーザー登録実行 | `UserController.newUseRegister()` |
| 6 | GET | `/index` | 商品トップ画面 | `UserController.indexPage()` |
| 7 | GET | `/user/products` | 一般商品一覧 | `UserController.getproduct()` |
| 8 | GET/POST | `/products/addtocart` | カート追加 | `UserController.addToCart()` |
| 9 | GET | `/user/cart` | カート表示 | `UserController.showCart()` |
| 10 | GET | `/user/cart/delete` | カート商品削除 | `UserController.deleteFromCart()` |
| 11 | GET | `/logout` | 一般ユーザーログアウト | `UserController.logout()` |
| 12 | GET | `/admin/login` | 管理者ログイン画面 | `AdminController.adminlogin()` |
| 13 | POST | `/admin/loginvalidate` | 管理者認証 | `AdminController.adminlogin()` |
| 14 | GET | `/admin/Dashboard` | 管理者ホーム | `AdminController.adminHome()` |
| 15 | GET | `/admin/categories` | カテゴリ一覧 | `AdminController.getcategory()` |
| 16 | POST | `/admin/categories` | カテゴリ追加 | `AdminController.addCategory()` |
| 17 | GET | `/admin/categories/delete` | カテゴリ削除 | `AdminController.removeCategoryDb()` |
| 18 | GET | `/admin/categories/update` | カテゴリ更新 | `AdminController.updateCategory()` |
| 19 | GET | `/admin/products` | 商品一覧管理 | `AdminController.getproduct()` |
| 20 | GET | `/admin/products/add` | 商品追加画面 | `AdminController.addProduct()` |
| 21 | POST | `/admin/products/add` | 商品追加実行 | `AdminController.addProduct()` |
| 22 | GET | `/admin/products/update/{id}` | 商品更新画面 | `AdminController.updateproduct()` |
| 23 | POST | `/admin/products/update/{id}` | 商品更新実行 | `AdminController.updateProduct()` |
| 24 | GET | `/admin/products/delete` | 商品削除 | `AdminController.removeProduct()` |
| 25 | GET | `/admin/customers` | 顧客一覧 | `AdminController.getCustomerDetail()` |
| 26 | GET | `/admin/profileDisplay` | プロフィール表示 | `AdminController.profileDisplay()` |
| 27 | POST | `/admin/updateuser` | プロフィール更新 | `AdminController.updateUserProfile()` |

## 3. 備考

- 一般ユーザー系と管理者系で URL プレフィックスが異なる
- `userloginvalidate` と `userloginvalidate1` は互換目的で両方存在する
- 実案件では認可要否、画面ID、機能ID、遷移元・遷移先も併記する
