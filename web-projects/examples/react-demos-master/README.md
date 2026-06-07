这是一个 React.js 的简单示例集合。

这些示例刻意写得很朴素、很直接，目的是让你一眼看懂 React 的基本思路。你会发现，入门这个库并没有想象中那么难。

## 相关项目

- [Flux Demo](https://github.com/ruanyf/extremely-simple-flux-demo)
- [Webpack Demos](https://github.com/ruanyf/webpack-demos)
- [React Router Tutorial](https://github.com/reactjs/react-router-tutorial)
- [CSS Modules Demos](https://github.com/ruanyf/css-modules-demos)
- [React Testing Demo](https://github.com/ruanyf/react-testing-demo)
- [React-Babel-Webpack 项目脚手架](https://github.com/ruanyf/react-babel-webpack-boilerplate)

## 如何使用

先把仓库克隆到本地。

```bash
$ git clone git@github.com:ruanyf/react-demos.git
```

然后直接打开 `demo*` 目录里的源码，边看边改，边刷新浏览器边观察结果。

## 如何运行和学习

如果你想“边看边执行、边执行边学习”，推荐这样做：

1. 进入目录：

```bash
cd web-projects/examples/react-demos-master
```

2. 启动一个本地静态服务器，避免直接用 `file://` 打开时遇到兼容性问题：

```bash
python3 -m http.server 8000
```

3. 在浏览器里打开对应示例，例如：

```text
http://localhost:8000/demo01/
http://localhost:8000/demo02/
http://localhost:8000/demo03/
```

4. 推荐按这个顺序学习：

- `demo01` 到 `demo03`：理解 JSX 的基本写法
- `demo04` 到 `demo05`：理解组件、`props`、`children`
- `demo06`：理解 `PropTypes` 和 `defaultProps`
- `demo07`：理解 `ref`
- `demo08` 到 `demo10`：理解 `state`、表单、生命周期
- `demo11` 到 `demo12`：理解异步请求和 Promise
- `demo13`：理解服务端渲染

5. 每学一个示例，都建议做三步：

- 先不改代码，直接运行看效果
- 再只改一处，比如文本、数组、样式或状态值
- 刷新浏览器，观察变化并回到源码对照理解

6. 如果你想更快地建立手感，可以重点练这几件事：

- 改标题文字
- 改数组内容和循环结果
- 给组件增加一个 `state`
- 改一次 `setState()` 的值
- 把 `console.log()` 加到生命周期里看执行顺序

7. 这套示例的学习范围、覆盖点和缺口整理在 [学习说明](./学习说明.md) 里。

## HTML 模板

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <script src="../build/react.development.js"></script>
    <script src="../build/react-dom.development.js"></script>
    <script src="../build/babel.min.js"></script>
  </head>
  <body>
    <div id="example"></div>
    <script type="text/babel">

      // 你的代码写在这里

    </script>
  </body>
</html>
```

## 目录

1. [渲染 JSX](#demo01-渲染-jsx)
1. [在 JSX 中使用 JavaScript](#demo02-在-jsx-中使用-javascript)
1. [在 JSX 中使用数组](#demo03-在-jsx-中使用数组)
1. [定义组件](#demo04-定义组件)
1. [this.props.children](#demo05-thispropschildren)
1. [PropTypes](#demo06-proptypes)
1. [查找 DOM 节点](#demo07-查找-dom-节点)
1. [this.state](#demo08-thisstate)
1. [表单](#demo09-表单)
1. [组件生命周期](#demo10-组件生命周期)
1. [Ajax](#demo11-ajax)
1. [从 Promise 中显示数据](#demo12-从-promise-中显示数据)
1. [服务端渲染](#demo13-服务端渲染)

---

## Demo01: 渲染 JSX

[demo](http://ruanyf.github.io/react-demos/demo01/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo01/index.html)

React 的模板语法叫做 [JSX](http://facebook.github.io/react/docs/displaying-data.html#jsx-syntax)。JSX 允许你在 JavaScript 代码里直接写 HTML 标签。`ReactDOM.render()` 会把 JSX 转成 HTML，并渲染到指定的 DOM 节点上。

```js
// 把一段 JSX 直接传给 ReactDOM.render
ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('example')
);
```

如果你想让浏览器真正执行 JSX 转换，需要使用 `<script type="text/babel">` 来标记这段代码，同时引入 `babel.min.js`。它是 Babel 的浏览器版本，可以直接在前端把 JSX 转成可执行的 JavaScript。

在 React v0.14 之前，React 曾使用 `JSTransform.js` 来转换 `<script type="text/jsx">`，但这套方式现在已经废弃了。

## Demo02: 在 JSX 中使用 JavaScript

[demo](http://ruanyf.github.io/react-demos/demo02/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo02/index.html)

你也可以在 JSX 里直接写 JavaScript。尖括号 `<` 表示 HTML 语法的开始，花括号 `{` 表示 JavaScript 语法的开始。

```js
// 先准备一个数组
var names = ['Alice', 'Emily', 'Kate'];

// 在 JSX 里用 map 生成多个子节点
ReactDOM.render(
  <div>
  {
    names.map(function (name) {
      return <div>Hello, {name}!</div>
    })
  }
  </div>,
  document.getElementById('example')
);
```

## Demo03: 在 JSX 中使用数组

[demo](http://ruanyf.github.io/react-demos/demo03/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo03/index.html)

如果一个 JavaScript 变量是数组，JSX 会自动把数组里的每个成员依次渲染出来。

```js
// JSX 数组里的每个元素都会被依次渲染
var arr = [
  <h1>Hello world!</h1>,
  <h2>React is awesome</h2>,
];
// 直接把数组放进 JSX 容器里
ReactDOM.render(
  <div>{arr}</div>,
  document.getElementById('example')
);
```

## Demo04: 定义组件

[demo](http://ruanyf.github.io/react-demos/demo04/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo04/index.html)

`class ComponentName extends React.Component` 会创建一个组件类。组件类需要实现 `render` 方法，用来返回组件的 UI。

在 React v16.0 之前，React 曾使用 `React.createClass()` 创建组件类，但这个方式现在已经废弃。

```javascript
// 定义一个类组件，render 负责返回界面
class HelloMessage extends React.Component {
  render() {
    // this.props.name 来自父组件传入的属性
    return <h1>Hello {this.props.name}</h1>;
  }
}

// 把组件挂到页面上的指定节点
ReactDOM.render(
  <HelloMessage name="John" />,
  document.getElementById('example')
);
```

你可以通过 `this.props.[属性名]` 访问组件属性。比如 `<HelloMessage name="John" />` 里的 `this.props.name` 就是 `John`。

请注意，组件名首字母必须大写，否则 React 会报错。例如 `HelloMessage` 可以作为组件名，但 `helloMessage` 不行。另外，React 组件的顶层只能有一个根节点。

```javascript
// 错误
class HelloMessage extends React.Component {
  render() {
    return <h1>
      Hello {this.props.name}
    </h1><p>
      some text
    </p>;
  }
}

// 正确
class HelloMessage extends React.Component {
  render() {
    return <div>
      <h1>Hello {this.props.name}</h1>
      <p>some text</p>
    </div>;
  }
}
```

## Demo05: this.props.children

[demo](http://ruanyf.github.io/react-demos/demo05/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo05/index.html)

React 使用 `this.props.children` 访问组件的子节点。

```javascript
// 组件把外部传入的 children 包装成列表
class NotesList extends React.Component {
  render() {
    return (
      <ol>
      {
        // React.Children.map 适合统一遍历 children
        React.Children.map(this.props.children, function (child) {
          return <li>{child}</li>;
        })
      }
      </ol>
    );
  }
}

ReactDOM.render(
  // 这里传入两个子节点，组件内部会从 this.props.children 取到它们
  <NotesList>
    <span>hello</span>
    <span>world</span>
  </NotesList>,
  document.getElementById('example')
);
```

`this.props.children` 一共有三种可能：

- 没有子节点时，值是 `undefined`
- 只有一个子节点时，值是一个对象
- 有多个子节点时，值是一个数组

React 提供了工具对象 [`React.Children`](https://facebook.github.io/react/docs/top-level-api.html#react.children) 来处理 `this.props.children` 这个不透明的数据结构。你可以用 `React.Children.map` 遍历它，而不用担心它到底是 `undefined`、`object` 还是 `array`。

## Demo06: PropTypes

[demo](http://ruanyf.github.io/react-demos/demo06/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo06/index.html)

React 组件可以接收很多属性，这些属性叫做 `props`，而且类型可以是任意的。

有时候你需要校验这些属性，避免用户传入不符合预期的数据。React 为此提供了 `PropTypes`。

```javascript
// 用 static propTypes 声明 title 必须是字符串且必填
class MyTitle extends React.Component {
  static propTypes = {
    title: PropTypes.string.isRequired,
  }
  render() {
    // 组件直接使用 props.title
    return <h1> {this.props.title} </h1>;
  }
}
```

上面的组件 `MyTitle` 接收一个 `title` 属性。`PropTypes` 会告诉 React：这个属性是必填的，而且必须是字符串。

现在我们传入一个数字：

```javascript
// 故意传入一个数字，方便看到校验警告
var data = 123;

// 这会触发 PropTypes 的类型检查
ReactDOM.render(
  <MyTitle title={data} />,
  document.getElementById('example')
);
```

这样就无法通过校验，控制台会出现错误提示：

```bash
Warning: Failed propType: Invalid prop `title` of type `number` supplied to `MyTitle`, expected `string`.
```

更多 `PropTypes` 的用法，可以查看 [官方文档](https://reactjs.org/docs/typechecking-with-proptypes.html)。

如果你想给属性提供默认值，可以使用 `defaultProps`。

```javascript
// 如果父组件没传 title，就使用默认值
class MyTitle extends React.Component {
  constructor(props) {
    super(props)
  }
  static defaultProps = {
    title: 'Hello World',
  }
  render() {
    // 这里读取到的是默认值或父组件传入的值
    return <h1> {this.props.title} </h1>;
  }
}

// 直接渲染，不传 title 也能正常显示
ReactDOM.render(
  <MyTitle />,
  document.getElementById('example')
);
```

从 React v15.5 开始，`React.PropTypes` 已经移动到单独的包里了。

## Demo07: 查找 DOM 节点

[demo](http://ruanyf.github.io/react-demos/demo07/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo07/index.html)

有时你需要在组件里直接引用某个 DOM 节点。React 提供了 `ref` 属性，可以把 DOM 节点挂到 `React.createRef()` 创建出来的实例上。

```js
// createRef 会返回一个 ref 对象
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    // 把输入框节点挂到 this.myTextInput 上
    this.myTextInput = React.createRef();
    this.handleClick = this.handleClick.bind(this)
  }
  handleClick() {
    // current 指向真实 DOM 节点
    this.myTextInput.current.focus();
  }
  render() {
    return (
      <div>
        {/* ref 绑定到 input 上 */}
        <input type="text" ref={this.myTextInput} />
        <input type="button" value="Focus the text input" onClick={this.handleClick} />
      </div>
    );
  }
}

ReactDOM.render(
  <MyComponent />,
  document.getElementById('example')
);
```

请注意，这种操作必须在组件已经挂载到 DOM 之后才能做，否则你拿到的会是 `null`。

## Demo08: this.state

[demo](http://ruanyf.github.io/react-demos/demo08/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo08/index.html)

React 把组件看作状态机：`this.state` 用来保存状态，`this.setState()` 用来更新状态并触发重新渲染。

```js
// state 保存组件内部状态
class LikeButton extends React.Component {
  constructor(props) {
    super(props)
    // 初始状态是未点赞
    this.state = {
    	liked: false
    }
    this.handleClick = this.handleClick.bind(this)
  }
  handleClick(event) {
    // 取反后再 setState
    this.setState({ liked: !this.state.liked });
  }
  render() {
    // 根据状态决定显示文本
    var text = this.state.liked ? 'like' : 'haven\'t liked';
    return (
      <p onClick={this.handleClick}>
        You {text} this. Click to toggle.
      </p>
    );
  }
}

ReactDOM.render(
  <LikeButton />,
  document.getElementById('example')
);
```

你可以像 `onClick`、`onKeyDown`、`onCopy` 这样，直接在组件属性上注册事件处理函数。官方文档列出了所有支持的事件。

## Demo09: 表单

[demo](http://ruanyf.github.io/react-demos/demo09/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo09/index.html)

按照 React 的设计理念，`this.state` 描述的是组件自身的状态，它会随着用户交互而改变；`this.props` 描述的是组件的属性，它是稳定且不可变的。

因此，`<input>`、`<textarea>`、`<option>` 这类表单元素的 `value` 并不会直接跟着用户输入变化。如果你想在用户输入时读取或更新值，就应该使用 `onChange` 事件。

```js
// 受控组件：value 由 state 控制
class Input extends React.Component {
constructor(props) {
  super(props)
  this.state = {value: 'Hello!'}
  this.handleChange = this.handleChange.bind(this)
}
handleChange(event) {
  // 每次输入都同步到 state
  this.setState({value: event.target.value});
}
render() {
  var value = this.state.value;
  return (
    <div>
      {/* value + onChange 组成受控输入框 */}
      <input type="text" value={value} onChange={this.handleChange} />
      <p>{value}</p>
    </div>
  );
}
}

ReactDOM.render(<Input/>, document.getElementById('example'));
```

更多内容可以查看 [官方文档](http://facebook.github.io/react/docs/forms.html)。

## Demo10: 组件生命周期

[demo](http://ruanyf.github.io/react-demos/demo10/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo10/index.html)

组件的生命周期主要分成三段：[挂载](https://facebook.github.io/react/docs/working-with-the-browser.html#component-lifecycle)（插入 DOM）、更新（重新渲染）和卸载（从 DOM 中移除）。React 提供了一系列生命周期钩子。`will` 开头的方法会在某个动作发生之前调用，`did` 开头的方法会在某个动作发生之后调用。

```js
// 组件挂载后启动定时器，持续更新 opacity
class Hello extends React.Component {
  constructor(props) {
    super(props)
    this.state = {opacity: 1.0};
  }

  componentDidMount() {
    // 每 100ms 更新一次透明度
    this.timer = setInterval(function () {
      var opacity = this.state.opacity;
      opacity -= .05;
      if (opacity < 0.1) {
        opacity = 1.0;
      }
      this.setState({
        opacity: opacity
      });
    }.bind(this), 100);
  }

  render() {
    // 把 state 映射到 style
    return (
      <div style={{opacity: this.state.opacity}}>
        Hello {this.props.name}
      </div>
    );
  }
}

ReactDOM.render(
  <Hello name="world"/>,
  document.getElementById('example')
);
```

下面是完整的生命周期方法列表：

- **componentWillMount()**：首次渲染前调用，适合做消息监听之类的准备工作。这里不能安全地使用 `this.setState`。
- **componentDidMount()**：首次渲染后调用。可以在这里访问 DOM。
- **componentWillUpdate(object nextProps, object nextState)**：组件更新并准备写入 DOM 之前调用。
- **componentDidUpdate(object prevProps, object prevState)**：组件更新完成并写入 DOM 后调用。首次渲染不会触发它。
- **componentWillUnmount()**：组件从 DOM 中卸载前调用，适合做清理工作。
- **componentWillReceiveProps(object nextProps)**：组件接收到新 `props` 时调用。你可以根据新 `props` 更新状态。
- **shouldComponentUpdate(object nextProps, object nextState)**：收到新 `props` 或 `state` 时、渲染前调用。如果返回 `false`，表示这次不需要更新。

## Demo11: Ajax

[demo](http://ruanyf.github.io/react-demos/demo11/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo11/index.html)

如果你想从服务器或 API 获取组件数据，通常会在 `componentDidMount` 的事件处理里发起 Ajax 请求。等服务器返回后，再通过 `this.setState()` 保存数据并触发 UI 重新渲染。

```js
// 组件通过 Ajax 拉取数据，然后写回 state
class UserGist extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      username: '',
      lastGistUrl: ''
    };
  }

  componentDidMount() {
    // 请求返回后更新用户名和地址
    $.get(this.props.source, function(result) {
      var lastGist = result[0];
      this.setState({
        username: lastGist.owner.login,
        lastGistUrl: lastGist.html_url
      });
    }.bind(this));
  }

  render() {
    return (
      <div>
        {/* 数据回来前这里会先显示空字符串 */}
        {this.state.username}'s last gist is
        <a href={this.state.lastGistUrl}>here</a>.
      </div>
    );
  }
}

ReactDOM.render(
  <UserGist source="https://api.github.com/users/octocat/gists" />,
  document.getElementById('example')
);
```

## Demo12: 从 Promise 中显示数据

[demo](http://ruanyf.github.io/react-demos/demo12/) / [源码](https://github.com/ruanyf/react-demos/blob/master/demo12/index.html)

这个示例受 Nat Pryce 的文章 ["Higher Order React Components"](http://natpryce.com/articles/000814.html) 启发。

如果 React 组件的数据是异步拿到的，我们也可以直接把一个 Promise 对象作为组件属性传进去：

```javascript
// Promise 先作为属性传进来，组件自己决定怎么展示 loading / error / success
ReactDOM.render(
  <RepoList promise={$.getJSON('https://api.github.com/search/repositories?q=javascript&sort=stars')} />,
  document.getElementById('example')
);
```

上面的代码会从 Github API 拉取数据，`RepoList` 组件拿到的是一个 Promise 作为属性。

在 Promise 还没完成时，组件会显示加载提示；Promise 成功后，组件会显示仓库列表；如果 Promise 被拒绝，组件会显示错误信息。

```javascript
// 组件内部用三个状态表示加载过程
class RepoList extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      loading: true,
      error: null,
      data: null
    };
  }

  componentDidMount() {
    // Promise 结束后更新 loading、data 或 error
    this.props.promise.then(
      value => this.setState({loading: false, data: value}),
      error => this.setState({loading: false, error: error}));
  }

  render() {
    // 先判断是否还在加载
    if (this.state.loading) {
      return <span>Loading...</span>;
    }
    else if (this.state.error !== null) {
      return <span>Error: {this.state.error.message}</span>;
    }
    else {
      // 成功后把仓库数组映射成列表项
      var repos = this.state.data.items;
      var repoList = repos.map(function (repo, index) {
        return (
          <li key={index}><a href={repo.html_url}>{repo.name}</a> ({repo.stargazers_count} stars) <br/> {repo.description}</li>
        );
      });
      return (
        <main>
          <h1>Github 上最受欢迎的 JavaScript 项目</h1>
          <ol>{repoList}</ol>
        </main>
      );
    }
  }
}
```

## Demo13: 服务端渲染

[源码](https://github.com/ruanyf/react-demos/tree/master/demo13/src)

这个示例复制自 [github.com/mhart/react-server-example](https://github.com/mhart/react-server-example)，我用 JSX 语法把它重写了一遍。

```bash
# 进入 demo13 目录安装依赖
$ npm install

# 把 src 子目录里的所有 jsx 文件转成 js 文件
$ npm run build

# 启动 HTTP 服务器
$ node server.js
```

启动后访问：

```text
http://localhost:3000
```

如果你想边改边看，建议先改 `src/app.js`，然后重新执行 `npm run build`，再刷新浏览器查看变化。

## 补充

### 预编译 JSX

上面的示例为了便于理解，没有提前编译 JSX。在生产环境里，应该先把 JSX 文件预编译后再上线。

先安装命令行工具 [Babel](https://babeljs.io/docs/usage/cli/)。

```bash
$ npm install -g babel
```

然后把 `.jsx` 文件预编译成 `.js` 文件。比如把整个 `src` 目录编译后输出到 `build` 目录，可以使用 `--out-dir` 或 `-d` 参数。

```bash
$ babel src --out-dir build
```

接着把编译好的 JS 文件放进 HTML 里：

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Hello React!</title>
    <script src="build/react.js"></script>
    <script src="build/react-dom.js"></script>
    <!-- 不需要 Browser.js 了 -->
  </head>
  <body>
    <div id="example"></div>
    <script src="build/helloworld.js"></script>
  </body>
</html>
```

## 相关链接

- [React 官方网站](http://facebook.github.io/react)
- [React 官方示例](https://github.com/facebook/react/tree/master/examples)
- [React (Virtual) DOM 术语表](http://facebook.github.io/react/docs/glossary.html)，Sebastian Markbåge
- [React 快速入门指南](http://www.jackcallister.com/2015/01/05/the-react-quick-start-guide.html)，Jack Callister
- [学习 React.js：入门与概念](https://scotch.io/tutorials/learning-react-getting-started-and-concepts)，Ken Wheeler
- [React 入门](http://ryanclark.me/getting-started-with-react)，Ryan Clark
- [React JS 教程与常见坑指南](https://zapier.com/engineering/react-js-tutorial-guide-gotchas/)，Justin Deal
- [React Primer](https://github.com/BinaryMuse/react-primer)，Binary Muse
- [jQuery 和 React.js 的思维差异](http://blog.zigomir.com/react.js/jquery/2015/01/11/jquery-versus-react-thinking.html)，zigomir

## 许可证

BSD 许可证
