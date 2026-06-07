import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';

// 浏览器端读取服务端注入的初始数据，再把 App 挂载到页面上
ReactDOM.render(<App items={window.APP_PROPS.items} />, document.getElementById('content'));
