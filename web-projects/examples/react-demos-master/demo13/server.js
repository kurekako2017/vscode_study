'use strict';

// 这是 demo13/src/server.js 编译后的服务端入口
var _app = require('./app');

var _app2 = _interopRequireDefault(_app);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var http = require('http'),
    browserify = require('browserify'),
    literalify = require('literalify'),
    React = require('react'),
    ReactDOMServer = require('react-dom/server');

// export default


http.createServer(function (req, res) {
  if (req.url == '/') {
    res.setHeader('Content-Type', 'text/html');
    // 先准备服务端首屏需要的初始数据
    var props = {
      items: ['Item 0', 'Item 1']
    };
    var html = ReactDOMServer.renderToStaticMarkup(React.createElement(
      'body',
      null,
      // 服务端先输出 HTML，浏览器再接管交互
      React.createElement('div', { id: 'content', dangerouslySetInnerHTML: { __html: ReactDOMServer.renderToString(React.createElement(_app2.default, { items: props.items }))
        } }),
      // 把初始数据注入给浏览器脚本
      React.createElement('script', { dangerouslySetInnerHTML: { __html: 'var APP_PROPS = ' + JSON.stringify(props) + ';'
        } }),
      // 再加载 React 和浏览器端 bundle
      React.createElement('script', { src: 'https://cdn.jsdelivr.net/npm/react@16.7.0/umd/react.production.min.js' }),
      React.createElement('script', { src: 'https://cdn.jsdelivr.net/npm/react-dom@16.7.0/umd/react-dom.production.min.js' }),
      React.createElement('script', { src: '/bundle.js' })
    ));
    res.end(html);
  } else if (req.url == '/bundle.js') {
    res.setHeader('Content-Type', 'text/javascript');
    // Browserify 打包浏览器端代码，literalify 把依赖映射到全局变量
    browserify().add('./browser.js').transform(literalify.configure({
      'react': 'window.React',
      'react-dom': 'window.ReactDOM'
    })).bundle().pipe(res);
  } else {
    res.statusCode = 404;
    res.end();
  }
}).listen(3000, function (err) {
  if (err) throw err;
  // 服务监听 3000 端口
  console.log('Listening on 3000...');
});
