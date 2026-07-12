# Frontend Learning Guide

这个项目的学习路径按真实源码组织，不按概念堆文档。

## React 在企业项目中的位置

```text
Browser
↓
React
↓
Router
↓
Component
↓
Hooks
↓
HTTP
↓
Backend
↓
Database
↓
Response
↓
React Render
```

这个路径说明：

- React 不是最终目的
- React 是企业前端系统中的组织层
- Router、Component、Hooks、HTTP 是一起工作的
- 页面渲染结果来自后端数据和前端状态的共同作用

## 架构路径

```text
main.jsx
↓
App.jsx
↓
Router
↓
Page
↓
Component
↓
Hook
↓
Event
↓
State
↓
Render
↓
Test
```

## 当前项目入口

- `src/main.jsx`：挂载 React、包住 `BrowserRouter`
- `src/App.jsx`：定义外层 Layout、导航、Routes
- `src/data/chapters.js`：生成首页和顶部导航
- `src/learning/`：统一 Trace、学习面板、路由桥接

## 页面怎么找源码

1. 先看右侧 `Learning Panel`
2. 读 `Current Route` 和 `Current Page`
3. 看 `Component Tree` 找到页面组件和子组件
4. 看 `Source Files` 找到真实源码文件
5. 看 `Test File` 找到对应测试
6. 对照页面上的按钮、状态和 Trace，回到源码找对应函数

## 页面怎么用浏览器调试

- `Console` 看报错、日志和状态打印
- `Network` 看请求地址、请求参数、响应数据和耗时
- `Trace` 看页面的渲染顺序和状态变化
- `Learning Panel` 看组件树、源码和测试文件的对应关系

## 页面到源码示例

- `HooksPage` → `src/chapters/hooks/HooksPage.jsx`
- `CounterDemo` → `src/chapters/hooks/useState/CounterDemo.jsx`
- `TimerDemo` → `src/chapters/hooks/useEffect/TimerDemo.jsx`
- `RouterPage` → `src/chapters/router/RouterPage.jsx`
- `ThemeContextDemo` → `src/chapters/context/ThemeContextDemo.jsx`
- `PostsDemo` → `src/chapters/api/PostsDemo.jsx`
- `Counter` → `src/chapters/test/Counter.jsx`
- `Counter.test.jsx` → `src/chapters/test/Counter.test.jsx`

## 章节对应的企业开发场景

### Hooks

企业开发对应：

`Retail Insight AI` → `Task` → `State` → `Create` → `Report`

企业中负责：

- 页面状态
- 输入框
- 分页
- Loading
- Modal
- Form
- Task 创建
- 搜索条件

和后端如何协作：

- 用状态控制请求前后 UI
- 用副作用处理接口请求
- 用条件状态驱动列表刷新

### Router

企业开发对应：

`Dashboard` → `Documents` → `Approval` → `RAG`

企业中负责：

- 后台菜单
- 详情页
- 用户中心
- 权限页面
- 审批页面

和后端如何协作：

- 通过路由区分不同业务域
- 通过参数加载不同记录
- 通过权限控制页面访问

### API

企业开发对应：

`GET` → `POST` → `DELETE` → `Upload` → `Download` → `Streaming`

企业中负责：

- `React`
- `Axios / fetch`
- `REST API`
- `Service`
- `Repository`
- `Database`

和后端如何协作：

- 前端发起请求和更新界面
- 后端校验请求并返回 JSON
- 网络层错误要先看 `Network`

### Context

企业开发对应：

当前项目中的主题切换

以后扩展到：

- `JWT`
- `RBAC`

企业中负责：

- 登录用户
- `JWT`
- `Token`
- `RBAC`
- 主题
- 国际化
- 全局配置

和后端如何协作：

- 后端返回用户和权限信息
- 前端用 Context 在组件树中共享
- Context 不负责数据库持久化

## Test

企业中负责：

- 前端回归验证
- 后端回归验证
- `CI` 自动检查

和后端如何协作：

- 前端测试保证交互没坏
- 后端测试保证业务没坏
- `CI` 把两边一起跑起来

## Retail Insight AI 对应

这个项目的页面、Trace、请求和测试都可以映射到 `Retail Insight AI` 的业务链路。

你可以把当前项目理解为：

- React 基础能力
- 页面学习入口
- 源码与运行时的对照样板

`Retail Insight AI` 则会继续扩展到：

- FastAPI
- Workflow
- RAG
- Approval
- PostgreSQL
- LLM

## Trace 阅读顺序

```text
BOOT
→ ROUTE
→ RENDER
→ COMPONENT
→ HOOK
→ EVENT
→ CALL
→ STATE
→ EFFECT
→ CLEANUP
→ ERROR
```

## 学习建议

- 先看页面，再看 `Learning Panel`
- 再回到对应源码和测试
- 如果你改了按钮，先找 `EVENT` 和 `CALL`
- 如果你改了状态，先找 `STATE`
- 如果页面重渲染，先看 `Why render`
- 不要死记 React API，要理解 `State`、`Props`、`Hook`、`Router`、`Context`、`API`、`Test` 为什么一起构成企业 React 架构
