# 86. Jenkins実行サンプル

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | Jenkins実行サンプル |
| 対象システム | JtProject |
| 文書区分 | 学習用 CI / Batch 実行資料 |
| 版数 | v1.0 |

## 2. 目的

本書は、`JtProject` の模擬バッチを Jenkins から実行するサンプルを整理し、チーム実行、証跡保管、定時実行の流れを学ぶことを目的とする。

## 3. 対象ファイル

| 項目 | 内容 |
|---|---|
| パイプライン定義 | `Jenkinsfile` |
| 実行対象 | `ProductInventoryCheckBatchApplication` |
| 成果物 | `batch-output/*.csv`, `logs/batch/*.log` |
| Maven 実行方式 | `mvnw` / `mvnw.cmd` を優先し、失敗時は `mvn` にフォールバック |

## 4. Jenkinsfile の流れ

1. ソースコードを取得する
2. Maven Wrapper を優先して compile し、失敗時は `mvn` に切り替える
3. 同じ方針で模擬バッチを実行する
4. CSV とログを成果物として保管する

## 5. 学習ポイント

- Jenkins を batch 実行基盤として使う考え方
- 画面から手動実行、定時実行、履歴確認を行うイメージ
- batch の出力ファイルを `archiveArtifacts` で残す運用
- wrapper が壊れている現場でも、ローカル Maven を使って継続実行する考え方

## 関連文書

- [26_バッチ・定期処理一覧.md](../03_database/26_バッチ・定期処理一覧.md)
- [83_模擬バッチ設計書.md](../03_database/83_模擬バッチ設計書.md)
- [85_Quartz定期実行サンプル.md](../03_database/85_Quartz定期実行サンプル.md)
- [86_商品_分類マスタ整合チェック詳細設計書.md](../03_database/86_商品_分類マスタ整合チェック詳細設計書.md)
- [60_ジョブネット一覧.md](../06_operations/60_ジョブネット一覧.md)
- [84_模擬ジョブネット一覧.md](../06_operations/84_模擬ジョブネット一覧.md)
- [33_運用手順書.md](../06_operations/33_運用手順書.md)
- [37_監視・障害対応手順書.md](../06_operations/37_監視・障害対応手順書.md)


