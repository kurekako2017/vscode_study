# Spring Boot 与 Next.js 公共组件库目录规范 / 命名规则

这页把 Next.js 前端公共组件库的目录规范、命名规则和导出习惯收束成可落地的约定，方便团队长期维护。

## 1. 这页的目标 / このページの目的

- 中文：把组件库从“怎么拆”推进到“怎么统一管理”。
- 日本語：コンポーネントを「どう分割するか」から「どう統一管理するか」へ進めるためのページです。

## 2. 推荐目录规范 / 推奨ディレクトリ規約

```text
frontend/
|-- components/
|   |-- ui/
|   |   |-- button/
|   |   |-- input/
|   |   |-- modal/
|   |   |-- badge/
|   |   `-- table/
|   |-- composite/
|   |   |-- form-row/
|   |   |-- card-header/
|   |   `-- table-toolbar/
|   `-- layout/
|       |-- header/
|       |-- sidebar/
|       `-- footer/
|-- features/
|-- hooks/
|-- services/
|-- types/
|-- styles/
`-- lib/
```

### 目录分工 / ディレクトリの役割

| 目录 | 中文用途 | 日本語の用途 |
|---|---|---|
| ui | 最基础、最可复用的控件 | 最小単位の再利用部品 |
| composite | 常用组合组件 | よく使う組み合わせ部品 |
| layout | 页面布局结构 | ページレイアウト構造 |
| features | 业务组件和场景逻辑 | 業務コンポーネントと場面ロジック |
| hooks | 通用 Hook | 共通 Hook |
| services | API 封装 | API ラッパー |
| types | 类型声明 | 型定義 |
| lib | 工具和客户端配置 | ユーティリティとクライアント設定 |

## 3. 组件目录内部结构 / コンポーネントディレクトリ内部構成

```text
button/
|-- button.tsx
|-- button.types.ts
|-- button.test.tsx
|-- button.stories.tsx
`-- index.ts
```

### 推荐文件职责 / 推奨ファイルの役割

| 文件 | 中文职责 | 日本語の役割 |
|---|---|---|
| button.tsx | 组件实现 | コンポーネント本体 |
| button.types.ts | Props 和类型 | Props と型 |
| button.test.tsx | 单元测试 | 単体テスト |
| button.stories.tsx | Storybook 示例 | Storybook サンプル |
| index.ts | 统一导出 | 一括エクスポート |

## 4. 命名规则 / 命名規則

### 组件命名

- 中文：组件名使用 PascalCase，例如 `Button`、`ProductCard`、`AuthCard`。
- 日本語：コンポーネント名は PascalCase を使い、`Button`、`ProductCard`、`AuthCard` のようにする。
- 中文：目录名可以使用 kebab-case，例如 `product-card`、`table-toolbar`。
- 日本語：ディレクトリ名は kebab-case を使い、`product-card`、`table-toolbar` のようにする。
- 中文：文件名建议与目录名一致，便于检索。
- 日本語：ファイル名はディレクトリ名と揃えると検索しやすい。

### 类型命名

- 中文：Props 类型推荐使用 `ButtonProps`、`ModalProps` 这种明确命名。
- 日本語：Props 型は `ButtonProps`、`ModalProps` のように明示的に命名する。
- 中文：共享类型放到 `types/`，局部类型放在组件目录内。
- 日本語：共有型は `types/` に、局所型はコンポーネント配下に置く。

### Hook 命名

- 中文：自定义 Hook 使用 `useXxx` 形式，例如 `useAuth`、`useProductList`。
- 日本語：カスタム Hook は `useXxx` 形式、例えば `useAuth`、`useProductList` にする。

## 5. 导出规则 / エクスポート規則

```text
components/ui/button/index.ts
components/composite/card-header/index.ts
```

### 统一导出建议 / 一括エクスポートの推奨

- 中文：每个组件目录都通过 `index.ts` 对外导出。
- 日本語：各コンポーネントディレクトリは `index.ts` で外部公開する。
- 中文：上层页面尽量从组件入口导入，不直接引用深层文件。
- 日本語：ページ側はできるだけ入口から import し、深いパスを避ける。
- 中文：如果组件有多个子模块，优先暴露一个稳定入口。
- 日本語：複数のサブモジュールがある場合は、安定した入口を 1 つにまとめる。

## 6. 设计约束 / 設計ルール

- 中文：ui 组件不要直接调用业务 API。
- 日本語：ui コンポーネントは業務 API を直接呼ばない。
- 中文：业务逻辑不要写进 Button、Input 这类原子组件。
- 日本語：Button や Input のような原子コンポーネントに業務ロジックを入れない。
- 中文：如果组件依赖页面状态，就说明它不该再放在 ui 层。
- 日本語：ページ状態に依存するなら、そのコンポーネントは ui 層に置くべきではない。
- 中文：重复使用 3 次以上的 UI 模式，才值得抽成公共组件。
- 日本語：3 回以上再利用する UI パターンだけを共通コンポーネント化する。

## 7. 版本和维护建议 / バージョン管理と保守

- 中文：不要让公共组件库无限膨胀，能收敛到 feature 的就不要升级为公共组件。
- 日本語：共通コンポーネントを無制限に増やさず、feature に閉じるものはそこに置く。
- 中文：如果组件只在一个业务域使用，优先放在 `features/`。
- 日本語：1 つの業務ドメインだけで使うなら `features/` に置く。
- 中文：通用性不确定的组件先放在业务目录，成熟后再提升到公共组件库。
- 日本語：汎用性が不明な部品はまず業務ディレクトリに置き、成熟したら共通化する。

## 8. 适合怎么学 / 学び方

1. 先看 ui 层，确认最小控件边界。
2. 再看 composite 层，理解组合组件如何复用原子组件。
3. 然后看 features 层，区分业务组件与公共组件。
4. 最后检查命名和导出方式是否一致。

日本語：
1. まず ui 層で最小部品の境界を確認する。
2. 次に composite 層で原子部品の組み合わせを理解する。
3. その後 features 層で業務コンポーネントとの違いを見る。
4. 最後に命名とエクスポート方法の統一を確認する。

## 9. 一句话总结 / 一言まとめ

- 中文：这页的重点，是把公共组件库变成“能长期维护的规则”，而不是临时堆出来的目录。
- 日本語：このページの重点は、共通コンポーネントを場当たり的な集まりではなく、長期保守できるルールにすることです。

## 10. 下一步 / 次のステップ

- [Spring Boot 与 Next.js 公共组件库 Storybook / 测试约定](./11-SpringBoot与Nextjs公共组件库Storybook测试约定.md)

中文：如果目录和命名已经统一，下一步就把 Storybook 和测试约定补上。

日本語：ディレクトリと命名がそろったら、次は Storybook とテスト規約を整えるとよいです。
