import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';

// 浏览器端读取服务端注入的初始数据，再把 App 挂载到页面上
// 这一步的关键是“复用服务端已经生成的 HTML”，而不是重新空白渲染一遍。
ReactDOM.render(<App items={window.APP_PROPS.items} />, document.getElementById('content'));
