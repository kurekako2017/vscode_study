# 上传策略 / Upload Policy / アップロードポリシー

## 范围 / Scope / 範囲

Upload API 实现前的冻结策略。

## 关键术语 / Key Terms / 主要用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| File Size Limit | 文件大小限制 | ファイルサイズ制限 |
| MIME Type | MIME 类型 | MIME タイプ |
| Idempotency | 幂等性 | 冪等性 |

## 规则 / Rules / 規約

| Rule | English | 中文（简体） | 日本語 |
|---|---|---|---|
| Max size | 20 MB MVP limit. | MVP 最大 20 MB。 | MVP 最大 20MB。 |
| Extensions | `.md`, `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json` | 允许这些扩展名。 | これらの拡張子を許可。 |
| MIME types | Must match extension allowlist. | MIME 必须匹配扩展名白名单。 | MIME は拡張子ホワイトリストと一致。 |
| Filename | UTF-8 safe, preserve original when possible. | 文件名 UTF-8 安全，尽量保留原名。 | UTF-8 安全、可能なら原名保持。 |
| Encoding | UTF-8 preferred. | 优先 UTF-8。 | UTF-8 優先。 |
| Checksum | SHA-256 family. | 使用 SHA-256 族。 | SHA-256 系を使用。 |
| Idempotency | `Idempotency-Key` optional in MVP, required later. | MVP 可选，后续强制。 | MVP では任意、将来必須。 |
| Delete | Archive / soft delete. | 删除语义为 archive / soft delete。 | 削除は archive / soft delete。 |

