'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

// 这是 demo13/src/app.js 编译后的产物，保留给直接运行时使用
var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var App = function (_React$Component) {
  _inherits(App, _React$Component);

  function App(props) {
    _classCallCheck(this, App);

    var _this = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

    // 绑定 this，保证点击事件和生命周期里都能访问组件实例
    _this.render = _this.render.bind(_this);
    // 初始列表数据来自 props
    _this.state = {
      items: _this.props.items,
      disabled: true
    };
    return _this;
  }

  _createClass(App, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      // 组件挂载后解除按钮禁用
      this.setState({
        disabled: false
      });
    }
  }, {
    key: 'handleClick',
    value: function handleClick() {
      // 点击按钮后在列表末尾追加一个条目
      this.setState({
        items: this.state.items.concat('Item ' + this.state.items.length)
      });
    }
  }, {
    key: 'render',
    value: function render() {
      return _react2.default.createElement(
        'div',
        null,
        _react2.default.createElement(
          'button',
          { onClick: this.handleClick.bind(this), disabled: this.state.disabled },
          'Add Item'
        ),
        _react2.default.createElement(
          'ul',
          null,
          this.state.items.map(function (item, index) {
            return _react2.default.createElement(
              'li',
              { key: index },
              item
            );
          })
        )
      );
    }
  }]);

  return App;
}(_react2.default.Component);

exports.default = App;
;
