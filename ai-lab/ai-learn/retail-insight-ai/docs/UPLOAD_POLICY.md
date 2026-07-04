# Upload Policy / 上传策略 / アップロードポリシー

## 1. Scope / 范围 / 範囲

This policy freezes upload limits and file handling rules before Upload API implementation.
本策略在 Upload API 实现前冻结上传限制与文件处理规则。
本ポリシーは Upload API 実装前にアップロード制限とファイル処理規約を凍結します。

## 2. Core Policy Terms / 核心术语 / 基本用語

| English | 中文（简体） | 日本語 |
|---|---|---|
| File Size Limit | 文件大小限制 | ファイルサイズ制限 |
| MIME Type | MIME 类型 | MIME タイプ |
| Extension | 扩展名 | 拡張子 |
| Encoding | 编码 | エンコーディング |
| Idempotency | 幂等性 | 冪等性 |

## 3. File Policy / 文件策略 / ファイルポリシー

| Rule | English | 中文（简体） | 日本語 |
|---|---|---|---|
| Max file size | 20 MB for MVP. | MVP 阶段最大 20 MB。 | MVP の最大サイズは 20MB。 |
| Allowed extensions | `.md`, `.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json` | 允许 `.md`、`.txt`、`.pdf`、`.docx`、`.xlsx`、`.csv`、`.json` | 許可拡張子は `.md`、`.txt`、`.pdf`、`.docx`、`.xlsx`、`.csv`、`.json` |
| Allowed MIME types | Match the frozen extension allowlist. | MIME 类型必须与扩展名白名单一致。 | MIME タイプは拡張子ホワイトリストと一致する必要があります。 |
| Filename rule | UTF-8 safe; preserve original name when possible. | 文件名必须 UTF-8 安全，尽量保留原名。 | ファイル名は UTF-8 安全で、可能なら元名を保持します。 |
| Encoding rule | UTF-8 preferred; other encodings must be validated. | 优先 UTF-8，其他编码必须显式校验。 | UTF-8 を優先し、他のエンコーディングは明示的に検証します。 |
| Checksum rule | SHA-256 is the frozen checksum family. | 冻结使用 SHA-256 作为校验族。 | チェックサムは SHA-256 系を凍結します。 |

## 4. Duplicate and Idempotency / 重复与幂等 / 重複と冪等

| Rule | English | 中文（简体） | 日本語 |
|---|---|---|---|
| Duplicate handling | Duplicate checksum returns the existing result or a conflict based on idempotency context. | 重复 checksum 需要返回已有结果，或在幂等上下文冲突时返回冲突。 | 重複 checksum は既存結果を返すか、冪等コンテキスト不一致なら競合を返します。 |
| Idempotency rule | `Idempotency-Key` is optional in MVP, required in future production. | MVP 阶段可选，未来生产必须要求 `Idempotency-Key`。 | MVP では任意、将来本番では `Idempotency-Key` 必須です。 |
| Archive/delete rule | Delete means archive/soft delete; preserve version history. | 删除语义冻结为 archive / soft delete，保留版本历史。 | 削除は archive / soft delete とし、履歴を保持します。 |

## 5. Future Enhancements / 未来扩展 / 将来拡張

- Virus scan is future-only and does not block this freeze.
- OCR is future-only and only applies to supported image/PDF pipelines.
- PDF parsing is future-only and must preserve checksum and source metadata.
- Office parsing is future-only and must preserve file provenance.
- Image handling is future-only and remains out of MVP scope.

## 6. Filename Language Handling / 文件名语言处理 / ファイル名言語処理

- English, Japanese, and Chinese filenames are allowed when UTF-8 safe.
- Normalization should preserve the original filename and store a safe display name if needed.
- Slugs or storage keys may be normalized internally, but the user-facing name should remain human readable.

