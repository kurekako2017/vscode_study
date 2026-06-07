var http = require('http'),
    browserify = require('browserify'),
    literalify = require('literalify'),
    React = require('react'),
    ReactDOMServer = require('react-dom/server');

// export default
import App from './app';

// 一个最小的 Node HTTP 服务，用来演示服务端渲染和客户端接管
http.createServer(function(req, res) {
  if (req.url == '/') {
    res.setHeader('Content-Type', 'text/html');
    // 首屏数据先在服务端准备好，供两端复用
    var props = {
      items: [
        'Item 0',
        'Item 1'
      ]
    };
    var html = ReactDOMServer.renderToStaticMarkup(
      <body>
        {/* 先把 App 的 HTML 直接渲染到页面容器中 */}
        <div id="content" dangerouslySetInnerHTML={{__html:
          ReactDOMServer.renderToString(<App items={props.items}/>)
        }} />

        {/* 把初始数据注入到全局变量，给浏览器端脚本读取 */}
        <script dangerouslySetInnerHTML={{__html:
          'var APP_PROPS = ' + JSON.stringify(props) + ';'
        }}/>
        {/* 先加载 React，再加载客户端 bundle */}
        <script src="https://cdn.jsdelivr.net/npm/react@16.7.0/umd/react.production.min.js"/>
        <script src="https://cdn.jsdelivr.net/npm/react-dom@16.7.0/umd/react-dom.production.min.js"/>
        <script src="/bundle.js"/>
      </body>
    );
    res.end(html);

  } else if (req.url == '/bundle.js') {
    res.setHeader('Content-Type', 'text/javascript');
    // Browserify 打包浏览器端代码，literalify 把模块名替换成全局变量
    browserify()
      .add('./browser.js')
      .transform(literalify.configure({
        'react': 'window.React',
        'react-dom': 'window.ReactDOM',
      }))
      .bundle()
      .pipe(res);
  } else {
    res.statusCode = 404;
    res.end();
  }
}).listen(3000, function(err) {
  if (err) throw err;
  // 服务启动后监听 3000 端口
  console.log('Listening on 3000...');
})
