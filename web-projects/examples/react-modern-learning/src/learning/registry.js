const commonSources = ['src/main.jsx', 'src/App.jsx', 'src/data/chapters.js']

export const learningPages = [
  {
    id: 'home',
    route: '/',
    pageName: 'HomePage',
    title: '首页',
    componentTree: ['App', '└── Layout', '    └── HomePage'],
    hooksUsed: [],
    propsFlow: ['HomePage → Link → 章节路由'],
    sourceFiles: ['src/chapters/home/HomePage.jsx', ...commonSources],
    testFile: null,
    childPage: 'HomePage',
  },
  {
    id: 'hooks',
    route: '/hooks',
    pageName: 'HooksPage',
    title: 'Hooks',
    componentTree: [
      'App',
      '└── Layout',
      '    └── HooksPage',
      '        ├── CounterDemo',
      '        └── TimerDemo',
    ],
    hooksUsed: ['useState', 'useMemo', 'useEffect'],
    propsFlow: ['HooksPage → CounterDemo', 'HooksPage → TimerDemo'],
    sourceFiles: [
      'src/chapters/hooks/HooksPage.jsx',
      'src/chapters/hooks/useState/CounterDemo.jsx',
      'src/chapters/hooks/useEffect/TimerDemo.jsx',
      ...commonSources,
    ],
    testFile: null,
    childPage: 'HooksPage',
  },
  {
    id: 'router',
    route: '/router',
    pageName: 'RouterPage',
    title: 'Router',
    componentTree: [
      'App',
      '└── Layout',
      '    └── RouterPage',
      '        ├── RouterHome',
      '        ├── AboutPage',
      '        └── UserProfile',
    ],
    hooksUsed: ['useParams'],
    propsFlow: ['RouterPage → Outlet → 当前子页面'],
    sourceFiles: ['src/chapters/router/RouterPage.jsx', 'src/chapters/router/RouterDemo.jsx', ...commonSources],
    testFile: null,
    childPage: 'RouterPage',
  },
  {
    id: 'context',
    route: '/context',
    pageName: 'ContextPage',
    title: 'Context',
    componentTree: ['App', '└── Layout', '    └── ContextPage', '        └── ThemeContextDemo'],
    hooksUsed: ['useContext', 'useMemo', 'useState'],
    propsFlow: ['ThemeContextDemo → ThemeContext.Provider value={theme} → ThemePreview'],
    sourceFiles: [
      'src/chapters/context/ContextPage.jsx',
      'src/chapters/context/ThemeContextDemo.jsx',
      ...commonSources,
    ],
    testFile: null,
    childPage: 'ContextPage',
  },
  {
    id: 'api',
    route: '/api',
    pageName: 'ApiPage',
    title: 'API',
    componentTree: ['App', '└── Layout', '    └── ApiPage', '        └── PostsDemo'],
    hooksUsed: ['useEffect', 'useState'],
    propsFlow: ['ApiPage → PostsDemo'],
    sourceFiles: ['src/chapters/api/ApiPage.jsx', 'src/chapters/api/PostsDemo.jsx', ...commonSources],
    testFile: null,
    childPage: 'ApiPage',
  },
  {
    id: 'test',
    route: '/test',
    pageName: 'TestPage',
    title: 'Test',
    componentTree: ['App', '└── Layout', '    └── TestPage', '        └── Counter'],
    hooksUsed: ['useState'],
    propsFlow: ['TestPage → Counter', 'Counter → button onClick'],
    sourceFiles: [
      'src/chapters/test/TestPage.jsx',
      'src/chapters/test/Counter.jsx',
      'src/chapters/test/Counter.test.jsx',
      ...commonSources,
    ],
    testFile: 'src/chapters/test/Counter.test.jsx',
    childPage: 'TestPage',
  },
]

export function getLearningPage(pathname) {
  if (!pathname || pathname === '/') {
    return learningPages[0]
  }

  if (pathname.startsWith('/router')) {
    return learningPages[2]
  }

  return learningPages.find((page) => page.route === pathname) ?? learningPages[0]
}

export function getRouterChildPage(pathname) {
  if (!pathname.startsWith('/router')) {
    return null
  }

  if (pathname === '/router') {
    return 'RouterHome'
  }

  if (pathname.startsWith('/router/about')) {
    return 'AboutPage'
  }

  if (pathname.startsWith('/router/users/')) {
    return 'UserProfile'
  }

  return 'RouterHome'
}
