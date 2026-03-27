# 85. Quartz定期実行サンプル

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | Quartz定期実行サンプル |
| 対象システム | JtProject |
| 文書区分 | 学習用定期実行資料 |
| 版数 | v1.0 |

## 2. 目的

本書は、`BAT-LAB-001 商品在庫整合チェック` を Quartz で定期実行する学習用サンプルを整理するための資料である。

## 3. 構成

| 項目 | 内容 |
|---|---|
| 起動クラス | `QuartzProductInventoryCheckApplication` |
| Job クラス | `ProductInventoryCheckQuartzJob` |
| 設定クラス | `QuartzBatchLabConfig` |
| プロファイル | `batch`, `quartz-lab` |
| 起動スクリプト | `scripts/start/run-quartz-product-inventory-check.cmd` |
| 実行間隔 | `application-quartz-lab.properties` の `intervalMs` |
| Maven 実行方式 | `mvnw.cmd` を優先し、失敗時は `mvn` にフォールバック |

## 4. 学習ポイント

- Quartz の `JobDetail` と `Trigger` の考え方を学べる
- Java プロジェクト内部で batch を定期実行する形を理解できる
- `JP1` や `Systemwalker` の前段階として、ジョブの概念をコードで確認できる

## 5. 実行方法

```cmd
scripts\start\run-quartz-product-inventory-check.cmd
```

補足:

- 初回実行は約 5 秒後に Job が起動する
- 出力先は `batch-output\product_inventory_check_yyyyMMdd_HHmmss.csv`
- 本リポジトリでは `mvnw.cmd` が利用できない環境があるため、スクリプトは `mvn` へ自動フォールバックする

停止:

```text
Ctrl + C
```
