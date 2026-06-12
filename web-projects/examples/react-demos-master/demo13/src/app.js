import React from 'react';

// 服务端渲染示例中的主组件，负责展示列表和处理新增操作
// 这个组件在服务端和浏览器端都会被用到，所以写法要尽量通用。
export default class App extends React.Component{

  constructor(props) {
    super(props);
    // render 和事件处理里都会用到 this，所以先绑定好
    this.render = this.render.bind(this);
    // 初始数据来自服务端传入的 props
    this.state = {
      items: this.props.items,
      disabled: true
    };
  }

  componentDidMount() {
    // 组件挂载后把按钮解除禁用
    // 这说明首屏 HTML 虽然已经渲染出来，但浏览器接管后才能真正交互。
    this.setState({
      disabled: false
    })
  }

  handleClick() {
    // 点击后在列表末尾追加一个新条目
    this.setState({
      items: this.state.items.concat('Item ' + this.state.items.length)
    })
  }

  render() {
    return (
      <div>
        {/* disabled 控制按钮是否可点，items 控制列表内容 */}
        {/* 这些 UI 状态在服务端渲染时就会生成初始 HTML。 */}
        <button onClick={this.handleClick.bind(this)} disabled={this.state.disabled}>Add Item</button>
        <ul>
        {
          this.state.items.map(function(item, index) {
            return <li key={index}>{item}</li>
          })
        }
        </ul>
      </div>
    )
  }
};
