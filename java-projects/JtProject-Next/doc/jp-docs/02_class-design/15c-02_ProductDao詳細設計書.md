# ProductDao 詳細設計書

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | ProductDao 詳細設計書 |
| 対象クラス | `ProductDao` / `ProductDaoImpl` |
| パッケージ | `dao` / `dao.impl` |
| 作成日 | 2026-03-15 |
| 作成者 | Codex |

## 2. クラス概要

| 項目 | 内容 |
|---|---|
| 役割 | `PRODUCT` テーブルに対する一覧取得、詳細取得、追加、更新、削除を担当する |
| アクセス技術 | Hibernate `SessionFactory` |
| 対象テーブル | `PRODUCT` |
| 主な呼出元 | `ProductServiceImpl` |

## 3. メソッド一覧

| No | メソッド名 | 役割 |
|---|---|---|
| 1 | `getProducts()` | 商品全件取得 |
| 2 | `addProduct(product)` | 商品追加 |
| 3 | `getProduct(id)` | 商品詳細取得 |
| 4 | `updateProduct(product)` | 商品更新 |
| 5 | `deletProduct(id)` | 商品削除 |

## 4. メソッド詳細

### 4.1 `getProducts()`

処理手順:

1. `SessionFactory.getCurrentSession()` を取得する。
2. HQL `from Product` を実行する。
3. 商品一覧 `List<Product>` を返却する。

### 4.2 `addProduct(product)`

処理手順:

1. 受領した `Product` を Session の `save()` で登録する。
2. 自動採番後の `Product` を返却する。

### 4.3 `getProduct(id)`

処理手順:

1. `Session.get(Product.class, id)` を実行する。
2. 該当ありなら商品を返却する。
3. 該当なしなら `null` を返却する。

### 4.4 `updateProduct(product)`

処理手順:

1. 更新対象 ID を持つ `Product` を受領する。
2. `Session.update(product)` を実行する。
3. 更新後の `Product` を返却する。

業務ルール:

- 更新対象存在確認は主に上位層で行う。
- 更新画像やカテゴリの妥当性判定は上位層に委譲している。

処理フロー図:

[Mermaid source: 15c-02_ProductDao詳細設計書-mermaid-1.mmd](assets/15c-02_ProductDao詳細設計書-mermaid-1.mmd)

<details>
<summary>Mermaid source (editable)</summary>

```mermaid
flowchart TD
    A[更新対象Product受領] --> B[Session.update(product)]
    B --> C[更新完了]
    C --> D[Product返却]
```
</details>



### 4.5 `deletProduct(id)`

処理手順:

1. `Session.load(Product.class, id)` で対象を読み込む。
2. 取得できれば `delete()` を実行する。
3. 成功時は `true` を返却する。
4. 対象なしまたは削除不可時は `false` もしくは例外となる。

処理フロー図:

[Mermaid source: 15c-02_ProductDao詳細設計書-mermaid-2.mmd](assets/15c-02_ProductDao詳細設計書-mermaid-2.mmd)

<details>
<summary>Mermaid source (editable)</summary>

```mermaid
flowchart TD
    A[id受領] --> B[Session.load(Product.class, id)]
    B --> C{対象取得可?}
    C -- No --> D[false or 例外]
    C -- Yes --> E[delete実行]
    E --> F[true返却]
```
</details>



## 5. 設計上の注意

- メソッド名が `deletProduct` となっており、表記揺れがある。
- `@OneToOne` でカテゴリ関連を持つが、設計上はカテゴリ 1 : 商品 N と見なしている。
- 実案件では論理削除や在庫更新履歴を持たせる可能性が高い。

## 6. 関連資料

- [15c_DAO詳細設計書.md](15c_DAO詳細設計書.md)
- [16_テーブル定義書.md](../03_database/16_テーブル定義書.md)
- [27_DDL一覧.md](../03_database/27_DDL一覧.md)

