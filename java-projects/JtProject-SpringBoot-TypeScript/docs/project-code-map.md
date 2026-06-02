# 项目源码导读

## 后端入口

- `src/main/java/com/jtspringproject/JtSpringProject/controller/ApiController.java`：前端调用的 REST API 入口
- `src/main/java/com/jtspringproject/JtSpringProject/services/`：业务服务接口
- `src/main/java/com/jtspringproject/JtSpringProject/services/impl/`：业务服务实现
- `src/main/java/com/jtspringproject/JtSpringProject/dao/`：数据访问接口
- `src/main/java/com/jtspringproject/JtSpringProject/dao/impl/`：数据访问实现
- `src/main/resources/application.properties`：端口、H2 数据库、日志配置

## 前端入口

- `frontend/index.html`：浏览器入口
- `frontend/src/main.ts`：状态、事件、渲染
- `frontend/src/api.ts`：通用 API 请求封装
- `frontend/src/services/appService.ts`：业务请求封装
- `frontend/src/types.ts`：前端类型定义
- `frontend/src/styles.css`：页面样式

## 推荐定位方式

看一个功能时按这个顺序找：

```text
main.ts 的事件或 render 函数
  -> appService.ts 的业务函数
  -> api.ts 的请求封装
  -> ApiController.java 的接口方法
  -> ServiceImpl
  -> DaoImpl
```

例如“加入购物车”：

```text
main.ts: add-cart
  -> addToCartRequest()
  -> POST /cart/items/{productId}
  -> ApiController.addCartItem()
  -> CartServiceImpl.java
  -> CartProductDaoImpl.java
```
