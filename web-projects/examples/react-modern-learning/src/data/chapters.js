export const chapters = [
  // 章节数据统一从这里读取，首页和导航栏都用它来生成 UI。
  // 这样一来，新增章节时只需要改这里，不用到处复制路由和文案。
  {
    path: '/hooks',
    title: 'Hooks',
    summary: 'useState、useEffect、组件状态与副作用',
  },
  {
    path: '/router',
    title: 'Router',
    summary: '路由、嵌套路由、参数与导航',
  },
  {
    path: '/context',
    title: 'Context',
    summary: '跨层传值、Provider 和 Consumer',
  },
  {
    path: '/api',
    title: 'API',
    summary: 'fetch、加载中、错误态、数据态',
  },
  {
    path: '/test',
    title: 'Test',
    summary: '组件行为测试与断言',
  },
]
