'use strict';

// 这是 demo13/src/browser.js 编译后的浏览器入口
var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDom = require('react-dom');

var _reactDom2 = _interopRequireDefault(_reactDom);

var _app = require('./app');

var _app2 = _interopRequireDefault(_app);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// 把服务端注入的初始 props 带给客户端渲染
_reactDom2.default.render(_react2.default.createElement(_app2.default, { items: window.APP_PROPS.items }), document.getElementById('content'));
