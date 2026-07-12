# DocumentsPage 测试学习笔记

这份文档只讲当前项目里的 `DocumentsPage` 测试。

不讲：

- TasksPage
- RagPage
- ApprovalPage

因为本轮目标是先把一个页面看懂。

补充说明：

- 本文保留了原来的讲解结构。
- 但当前真实测试文件已经迁移到 `frontend/src/pages/DocumentsPage.test.tsx`。
- 所以下面凡是涉及“当前真实测试文件”的地方，都应以 `frontend/src/pages/DocumentsPage.test.tsx` 为准。

## 1. DocumentsPage 测试文件在哪里

当前真实测试文件在：

- `frontend/src/pages/DocumentsPage.test.tsx`

也就是说，DocumentsPage 的主要页面测试现在已经从 `App.test.tsx` 拆出来了。

## 2. 测试从哪个入口开始执行

当前前端 `package.json` 里的测试命令是：

```json
"test": "vitest run"
```

所以平时运行：

```bash
npm test -- --run
```

实际上就是 Vitest 去执行 `frontend/src/` 下面匹配到的测试文件。

当前 DocumentsPage 测试会随着 `frontend/src/pages/DocumentsPage.test.tsx` 一起执行。

## 3. describe / it / test 的作用

在 `frontend/src/pages/DocumentsPage.test.tsx` 里可以看到：

```ts
describe("DocumentsPage", () => {
  it("shows document list, detail, and chunk count", async () => {
```

可以这样理解：

- `describe()`：把一组相关测试包在一起，方便阅读和输出测试报告
- `it()`：定义一条具体测试用例
- `test()`：和 `it()` 基本等价，只是写法不同

当前文件主要用的是 `describe + it`。

## 4. render() 做了什么

测试里会写：

```ts
render(<DocumentsPage />);
```

这一步的意思是：

- 把 React 组件挂到测试用的虚拟 DOM
- 让我们可以像用户一样查找按钮、输入框、文本
- 然后触发点击、输入、提交等动作

当前真实测试已经直接渲染 `DocumentsPage`，不是先经过 `App.tsx` 导航。

```ts
render(<DocumentsPage />);
```

也就是：

直接渲染页面组件 → 直接测试这一页自己的行为。

## 5. screen 是什么

`screen` 来自 Testing Library。

它表示“当前测试页面的可见内容查询入口”。

例如：

```ts
screen.findByText("Monthly Policy")
screen.getByLabelText("ファイル")
```

常见区别：

- `getBy...`：立刻查找，找不到就直接报错
- `findBy...`：异步等待，适合等接口返回后再出现的内容

DocumentsPage 里大量使用 `findBy...`，因为列表、详情、上传结果都依赖 API 返回。

## 6. userEvent 是什么

`userEvent` 也是 Testing Library 常见工具，用来更像真实用户那样操作页面。

例如它更适合：

- 连续输入
- tab 切换
- 更接近浏览器真实交互节奏

但要注意：**当前这个项目的真实测试代码里并没有使用 `userEvent`，而是使用 `fireEvent`。**

所以本项目当前真实情况是：

- 你需要认识 `userEvent` 是什么
- 但这份测试文件实际用的是 `fireEvent`

## 7. vi.mock() 是什么

`vi` 是 Vitest 提供的测试工具对象。

在这个文件里，当前真实代码主要用的是：

- `vi.fn()`
- `vi.stubGlobal()`
- `vi.restoreAllMocks()`
- `vi.unstubAllGlobals()`

例如：

```ts
vi.stubGlobal("fetch", fetchMock);
```

这和 `vi.mock()` 的核心思路一样，都是为了把“真实依赖”替换成“测试里的可控实现”。

当前 `DocumentsPage.test.tsx` 没有大量直接写 `vi.mock("module-name")`，
而是直接替换全局 `fetch`：

```ts
vi.stubGlobal("fetch", fetchMock);
```

DocumentsPage 不使用 SSE，因此本文件不需要 Mock `EventSource`。

## 8. Mock API 为什么不调用真实后端

因为前端测试的目标不是验证后端是否正常，而是验证：

- 页面状态是否正确变化
- 按钮是否可点
- 错误是否显示
- 成功后是否刷新

如果这里直接调真实后端，会带来几个问题：

1. 测试速度变慢
2. 结果容易受后端状态影响
3. 前端测试失败时，不容易判断是前端问题还是后端问题

所以当前真实测试做法是：

- 用 `vi.stubGlobal("fetch", fetchMock)`
- 让 `fetchMock` 按顺序返回我们准备好的假响应

## 9. beforeEach() 的作用

当前真实 `DocumentsPage.test.tsx` 没有单独写 `beforeEach()`。

这个文件的真实清理方式是每个测试结束后统一执行：

- `cleanup()`
- `vi.unstubAllGlobals()`
- `vi.restoreAllMocks()`

也就是说：

- 当前文件不会在 `beforeEach()` 里预置 `EventSource`
- 当前文件的重点是替换 `fetch`
- 每条测试跑完后再把 DOM 和 Mock 状态清干净

## 10. act() / waitFor() 的作用

当前真实 `DocumentsPage.test.tsx` 主要使用的是：

- `findByText()`
- `findByRole()`

如果以后你在别的页面测试里看到 `waitFor()`，可以这样理解：

- `waitFor()`：反复等待，直到断言成立或超时
- `act()`：保证 React 状态更新已经完成后再断言

当前这个文件没有显式写很多 `waitFor()` 或 `act()`，因为 Testing Library 的很多异步查询本身已经覆盖了常见等待场景。

对 DocumentsPage 来说，更常见的是：

- `findByText()`
- `findByRole()`

它们本质上也带有“等待页面更新”的意思。

## 11. 如何测试 Loading

DocumentsPage 本身有 loading 状态，例如首次读取列表时会先发请求。

当前测试文件没有专门写一条 “DocumentsPage loading 文案出现” 的单独用例，但写法通常会是：

- 先让 `fetch` 延迟返回
- 然后断言页面出现 loading 文案

这一轮我们在 Approval 页面里就用了类似思路，证明这种测试方式在当前项目里是可行的。

## 12. 如何测试 Empty

真实测试用例：

- `shows empty state when there are no documents`

核心代码流程：

```ts
vi.stubGlobal("fetch", vi.fn().mockResolvedValue(documentList()));

render(<DocumentsPage />);

expect(await screen.findByText("No documents yet. Upload a file to start the document workflow.")).toBeInTheDocument();
```

意思是：

1. Mock 一个空文档列表
2. 直接渲染 DocumentsPage
3. 等页面显示空状态文案

## 13. 如何测试列表显示

真实测试用例：

- `shows document list, detail, and chunk count`

它做了三次 API Mock：

1. 文档列表
2. 文档详情
3. Chunk 列表

然后验证：

- 页面能看到 `Monthly Policy`
- 页面能看到 `Chunk Count`
- 页面能看到 chunk 内容 `Paragraph one`

这说明当前测试不是只测“列表有没有”，而是把 DocumentsPage 的主链路一起测了。

## 14. 如何测试上传成功

真实测试用例名字是：

- `uploads a document successfully and refreshes the list`

这是当前最值得精读的一条。

## 15. 如何测试上传失败

真实测试用例：

- `shows upload failure from backend`

关键点：

- 先返回空列表
- 再让上传接口返回 422 错误
- 最后断言页面出现错误提示

对应断言是：

```ts
expect(await screen.findByRole("alert")).toHaveTextContent("[missing_title] Title required");
```

## 16. 如何测试 Archive

真实测试用例：

- `archives a document and refreshes current detail`

这个测试验证的不是“按钮被点了”这么简单，而是：

1. 页面先加载文档列表
2. 自动加载详情
3. 自动加载 chunk
4. 点击 `Archive`
5. 后端返回归档成功
6. 页面再次刷新列表和详情
7. 页面显示成功反馈

最后断言：

```ts
expect(await screen.findByRole("status")).toHaveTextContent("Archive accepted: doc-1 (archived)");
```

## 17. 为什么操作后要验证 API 再次调用

因为很多页面 bug 不在“第一次请求”，而在“操作成功后页面没刷新”。

比如上传成功后，如果不重新拉列表：

- 页面仍然显示旧数据
- 用户会误以为上传没成功

所以测试里不仅要看成功提示，还要确认新的数据真的被渲染出来。

## 18. 测试数据如何流入 DocumentsPage

当前真实数据流是：

`fetchMock`
→ `DocumentsPage`
→ `DocumentsPage` 调用 `api.ts`
→ `api.ts` 调用被 mock 的 `fetch`
→ mock response 返回
→ `DocumentsPage` 更新 React state
→ DOM 刷新
→ `screen` / `expect` 做断言

也就是说：

测试数据不是直接塞进组件 props，而是走了“接近真实页面”的调用链。

## 19. 一个完整测试用例的逐行调用顺序

这里用真实用例：

- `uploads a document successfully and refreshes the list`

当前真实顺序可以这样读：

### 第 1 步：准备 fetchMock

测试先写：

```ts
const fetchMock = vi.fn()
```

然后按顺序准备返回值：

1. 第一次：文档列表为空
2. 第二次：上传成功
3. 第三次：刷新后的文档列表包含 `budget.csv`
4. 第四次：读取新文档详情
5. 第五次：读取 chunk 列表

### 第 2 步：替换全局 fetch

```ts
vi.stubGlobal("fetch", fetchMock);
```

这样页面里的真实 `fetch()` 就不会发网络请求了。

### 第 3 步：渲染 DocumentsPage

```ts
render(<DocumentsPage />);
```

### 第 4 步：页面启动后自动加载 Documents 列表

这里不需要再点导航按钮。

### 第 5 步：构造一个真实 File 对象

```ts
const file = new File(["month,sales"], "budget.csv", { type: "text/csv" });
```

这里很重要。
因为上传测试不能只改字符串，必须模拟真实文件。

### 第 6 步：选择文件

```ts
fireEvent.change(screen.getByLabelText("ファイル"), { target: { files: [file] } });
```

### 第 7 步：填写标签

```ts
fireEvent.change(screen.getByLabelText("Tags (comma separated)"), { target: { value: "finance" } });
```

### 第 8 步：点击上传按钮

```ts
fireEvent.click(screen.getByRole("button", { name: "Upload Document" }));
```

这一步之后，页面内部会调用：

- `uploadDocument()`
- 上传成功后再调用 `listDocuments()`
- 然后再调用 `getDocument()`
- 最后再调用 `getDocumentChunks()`

### 第 9 步：验证成功反馈

```ts
expect(await screen.findByRole("status")).toHaveTextContent("Upload completed: doc-9");
```

### 第 10 步：验证新文档真的显示出来

```ts
expect((await screen.findAllByText("budget.csv")).length).toBeGreaterThan(0);
```

这一步非常关键。它证明：

- 不只是接口成功了
- 而是页面刷新后真的拿到了新数据

## 20. 如何单独运行 DocumentsPage 测试

当前真实 DocumentsPage 测试文件已经是独立文件，所以最稳妥的单独运行命令是：

```bash
cd frontend
npm test -- --run src/pages/DocumentsPage.test.tsx -t "uploads a document successfully and refreshes the list"
```

如果你想跑 DocumentsPage.test.tsx 里所有测试，可以用：

```bash
cd frontend
npm test -- --run src/pages/DocumentsPage.test.tsx
```

## 21. 初学者建议怎么读这份测试

推荐顺序：

1. 先读 `shows empty state when there are no documents`
2. 再读 `shows document list, detail, and chunk count`
3. 再读 `shows upload failure from backend`
4. 最后精读 `uploads a document successfully and refreshes the list`

这样会比较容易建立感觉：

空状态
→ 列表显示
→ 错误显示
→ 完整成功链路

## 22. 当前这份学习文档的边界

这份文档只解释：

- 当前真实测试代码怎么运行
- 当前真实按钮文本和函数调用链
- 为什么要 Mock API

它不扩展讲：

- Vitest 全部 API
- React Testing Library 全部能力
- E2E 测试
- Playwright

先把这一页看懂，就已经很够用了。
