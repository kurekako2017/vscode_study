# NestJS 学习指南

## 1. 这份学习指南适用的范围

本项目中，NestJS 不是替代 Express，而是作为“企业级框架对照学习”的第二套后端实现保留在仓库中。

核心原则：

- Express 继续保留为原始业务入口
- NestJS 作为学习版后端，用于对照理解企业项目结构
- React 前端不强制绑定某一个后端，使用 `VITE_API_BASE_URL` 在运行时切换
- 当前阶段重点不是扩展业务，而是学习 NestJS 的组织方式、依赖注入、DTO、校验与统一异常处理

实际项目入口：

- Express: `apps/api/src/server.ts`
- NestJS: `apps/api-nestjs/src/main.ts`
- 共享类型: `packages/shared/src/index.ts`
- 前端切换入口: `apps/web/src/api.ts`

---

## 2. 为什么这个项目会同时存在 Express 和 NestJS

Express 适合学习以下概念：

- `app.get()` / `app.post()` / `app.use()`
- middleware
- request / response 直接操作
- 路由与认证逻辑的手工组织

NestJS 适合学习以下概念：

- `@Controller()`
- `@Get()` / `@Post()` / `@Put()` / `@Delete()`
- `@Injectable()` Service
- `@Module()` 模块组织
- `constructor` 依赖注入
- DTO + `ValidationPipe`
- 全局异常过滤器

这两套实现本质上都是同一个业务契约，只是组织方式不同；在本项目里，最重要的学习价值在于“同一接口，两个框架如何表达”。

---

## 3. 项目里的真实代码结构

### 3.1 根目录结构

```text
JtProject-TypeScript/
├── apps/
│   ├── api/                  # 原始 Express 后端
│   ├── api-nestjs/          # NestJS 学习后端
│   └── web/                 # React + Vite 前端
├── packages/
│   └── shared/              # 共享类型与接口契约
├── package.json
├── README.md
└── docs/
```

### 3.2 NestJS 应用结构

```text
apps/api-nestjs/src/
├── main.ts
├── app.module.ts
├── common/
│   └── filters/
│       └── http-exception.filter.ts
├── product/
│   ├── product.controller.ts
│   ├── product.service.ts
│   ├── product.module.ts
│   └── dto/
│       ├── create-product.dto.ts
│       └── update-product.dto.ts
├── user/
│   ├── user.controller.ts
│   ├── user.service.ts
│   ├── user.module.ts
│   └── dto/
│       ├── login.dto.ts
│       └── register.dto.ts
├── cart/
│   ├── cart.controller.ts
│   ├── cart.service.ts
│   └── cart.module.ts
├── category/
│   ├── category.controller.ts
│   ├── category.service.ts
│   └── category.module.ts
└── ...
```

---

## 4. 启动方式

### 4.1 安装依赖

```bash
cd java-projects/JtProject-TypeScript
npm install
```

### 4.2 启动 Express

```bash
npm run start:api
```

默认端口：

- Express: `http://localhost:8090/api`

### 4.3 启动 NestJS

```bash
npm --workspace apps/api-nestjs run start:dev
```

默认端口：

- NestJS: `http://localhost:3002/api`

### 4.4 启动前端

```bash
npm --workspace apps/web run dev -- --host 0.0.0.0
```

默认端口：

- React: `http://localhost:5175`

---

## 5. main.ts：NestJS 应用启动入口

实际入口在：`apps/api-nestjs/src/main.ts`。

关键代码逻辑：

```ts
const app = await NestFactory.create(AppModule)
app.use(cookieParser())
app.setGlobalPrefix('api')
app.useGlobalFilters(new HttpExceptionFilter())
app.useGlobalPipes(new ValidationPipe({ ... }))
app.enableCors({
  origin: ['http://localhost:5175', 'http://127.0.0.1:5175'],
  credentials: true
})
await app.listen(port)
```

这里体现了几个 NestJS 常见特征：

1. `NestFactory.create(AppModule)`：创建应用实例
2. `app.use()`：注册 Express 中间件
3. `app.setGlobalPrefix('api')`：所有路由前缀自动加 `/api`
4. `app.useGlobalPipes(...)`：对 DTO 做校验转换
5. `app.useGlobalFilters(...)`：统一异常返回格式
6. `app.enableCors(...)`：为前端跨域与 cookie 场景服务

注意：因为项目中使用 `app.setGlobalPrefix('api')`，所以最终 URL 不是 `/products`，而是 `/api/products`。

---

## 6. AppModule：NestJS 入口模块

核心文件：`apps/api-nestjs/src/app.module.ts`

```ts
@Module({
    imports: [ProductModule, UserModule, CartModule, CategoryModule]
})
export class AppModule { }
```

这是 NestJS 的模块入口，类似“总装配单”，把各个业务模块拉进来。

- `ProductModule`：商品模块
- `UserModule`：认证/会话/管理员模块
- `CartModule`：购物车模块
- `CategoryModule`：分类模块

这体现了 NestJS 中最典型的组织方式：

- Controller：处理 HTTP
- Service：处理业务逻辑
- Module：汇总依赖

---

## 7. Controller 与 Express 的对应关系

### 7.1 商品控制器

文件：`apps/api-nestjs/src/product/product.controller.ts`

```ts
@Controller('products')
export class ProductController {
    @Get()
    getAll(): ApiResult<Product[]> {
        return { success: true, message: 'Products loaded', data: this.productService.findAll() }
    }
}
```

在 Express 中，这个接口相当于：

```ts
app.get('/api/products', (...) => {
  response.json(ok('Products loaded', store.getProducts()))
})
```

这里的对照是：

- `@Controller('products')` + `app.setGlobalPrefix('api')` => `/api/products`
- `@Get()` => `GET`
- 返回对象 => `{ success, message, data }`

### 7.2 统一返回契约

共享类型约定来自：`packages/shared/src/index.ts`

```ts
export type ApiResult<T> = {
  success: boolean
  message: string
  data: T
}
```

所以无论 Express 还是 NestJS，前端都能统一解析：

```json
{
  "success": true,
  "message": "Products loaded",
  "data": []
}
```

这也是前端能够“无感切换后端”的前提。

---

## 8. Service：业务逻辑集中地

文件：`apps/api-nestjs/src/product/product.service.ts`

```ts
@Injectable()
export class ProductService {
    private readonly categories = structuredClone(seedCategories)
    private products: Product[] = structuredClone(seedProducts)

    findAll() {
        return this.products
    }

    create(input: ProductInput) {
        const product = this.toProduct(input, this.nextId(this.products))
        this.products.push(product)
        return product
    }
}
```

本项目使用的是“内存数据层 + Service 层”，并没有引入数据库层。

这里的学习重点是：

- `ProductService` 负责商品业务逻辑
- `ProductController` 只负责接收请求和返回响应
- `Store` 在 Express 中承担数据层，在 NestJS 中被翻译成 `Service + private array`

这很像一个“从手工 Express 转到更结构化 NestJS”的过渡案例。

---

## 9. DTO：定义请求体结构并校验

### 9.1 创建 DTO

文件：`apps/api-nestjs/src/product/dto/create-product.dto.ts`

```ts
export class CreateProductDto {
    @IsString()
    @IsNotEmpty()
    @MinLength(2)
    name!: string

    @Transform(({ value }) => Number(value))
    @IsNumber()
    @IsPositive()
    price!: number

    @Transform(({ value }) => Number(value))
    @IsInt()
    @IsPositive()
    categoryId!: number
}
```

### 9.2 Update DTO

文件：`apps/api-nestjs/src/product/dto/update-product.dto.ts`

这里所有字段都使用 `@IsOptional()`，表示：

- PUT 更新时，允许只提交一部分字段
- 与 Express 里的“局部更新”语义接近

### 9.3 ValidationPipe 的作用

在 `main.ts` 中，注册了：

```ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
    transformOptions: { enableImplicitConversion: true }
  })
)
```

这表示：

- 自动把字符串转成数字
- 验证请求体字段是否合法
- 拒绝多余字段
- 把错误统一转换成异常

这与 Express 里手工写 `if` 校验相比，明显更规范、更标准化。

---

## 10. 全局异常过滤器

文件：`apps/api-nestjs/src/common/filters/http-exception.filter.ts`

```ts
@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
    catch(exception: unknown, host: ArgumentsHost) {
        const response = host.switchToHttp().getResponse<Response>()
        const status = exception instanceof HttpException ? exception.getStatus() : HttpStatus.INTERNAL_SERVER_ERROR

        response.status(status).json({
            success: false,
            message,
            data: null
        })
    }
}
```

这里的作用是：

- 把所有异常统一成 `ApiResult` 风格
- 让前端一套逻辑处理成功/失败
- 避免每个 Controller 手工 `response.status(...)`

相当于 Spring Boot 里的 `@ControllerAdvice` 思路，从结构上非常接近企业项目的统一错误处理。

---

## 11. 认证与 cookie 设计

### 11.1 用户登录

文件：`apps/api-nestjs/src/user/user.controller.ts`

```ts
@Post('login')
login(
    @Res({ passthrough: true }) response: Response,
    @Body() body: LoginDto
): ApiResult<SessionInfo> {
    const user = this.userService.checkLogin(body.username, body.password)
    if (!user || user.role !== 'ROLE_NORMAL') {
        throw new UnauthorizedException('Invalid user credentials')
    }

    response.cookie('jt_ts_session', user.username, this.userService.cookieOptions())
    return { success: true, message: 'User login successful', data: this.userService.sessionDataFor(user) }
}
```

### 11.2 管理员登录

管理员与普通用户分开使用不同 cookie：

- `jt_ts_session`：普通用户登录
- `jt_ts_admin`：管理员登录

这非常贴近原始 Express 的设计：

```ts
const sessionCookieName = 'jt_ts_session'
const adminCookieName = 'jt_ts_admin'
```

### 11.3 会话恢复

文件：`apps/api-nestjs/src/user/user.service.ts`

```ts
sessionData(request: Request): SessionInfo {
    const user = this.currentUser(request)
    const adminUsername = this.currentAdminUsername(request)
    return {
        authenticated: Boolean(user),
        username: user?.username ?? '',
        role: user?.role ?? '',
        adminLoggedIn: Boolean(adminUsername),
        adminUsername
    }
}
```

这里体现了服务端会话状态恢复的思路：

- 前端刷新或重新打开页面
- 请求 `/api/session`
- 服务端从 cookie 读取用户名
- 返回当前登录状态

---

## 12. 用户 / 购物车 / 分类模块的现实意义

NestJS 版本中，除了 Product，还补充了以下模块：

- `User`: 登录、注册、登出、会话状态、管理员登录
- `Cart`: 购物车列表、增加商品、删除商品
- `Category`: 分类列表

这些实现都与 Express 版本对齐，并共享同一套 `ApiResult` 格式和 cookie 设计。

示例：

- `GET /api/session`
- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/auth/logout`
- `GET /api/categories`
- `GET /api/cart`
- `POST /api/cart/items/:productId`
- `DELETE /api/cart/items/:productId`
- `POST /api/admin/login`
- `GET /api/admin/overview`

这种做法最大的价值，不是把业务“换成更高级的写法”，而是让你看到：

- 同样的功能，在 Express 和 NestJS 中分别怎么实现
- 哪些地方可以抽象成模块、服务和 DTO
- 哪些地方必须在 Controller 里保留权限校验和 cookie 处理

---

## 13. Express 与 NestJS 的映射关系

| 概念 | Express | NestJS | 说明 |
| --- | --- | --- | --- |
| 路由入口 | `app.get()` / `app.post()` | `@Controller()` + `@Get()` | 入口方式不同 |
| 处理函数 | handler function | controller method | 通过方法表达接口 |
| 业务逻辑 | store / function | `@Injectable()` Service | 逻辑收敛到 service |
| 模块组织 | 单文件 | `@Module()` | 更适合大项目 |
| DTO | 手工校验 | `class-validator` + `ValidationPipe` | 规范化校验 |
| 异常处理 | 手工 `response.status()` | `ExceptionFilter` | 统一错误结构 |
| 认证 | cookie + manual check | cookie + service guard | 同一思想 |

---

## 14. 当前项目里最值得学习的一个点：共享契约

共享类型文件：`packages/shared/src/index.ts`

这里定义了：

- `ApiResult<T>`
- `Product`
- `User`
- `SessionInfo`
- `AdminOverview`
- `LoginBody`
- `RegisterBody`
- `ProductInput`

这意味着：

- 前端页面知道后端返回结构是什么
- 后端接口返回字段和前端消费字段的“约定”在一个地方
- 修改类型时，TypeScript 能直接发现不一致之处

这也是现代 Web 项目里非常重要的“接口契约管理”思维。

---

## 15. 这套 NestJS 代码的真实定位

本项目中的 NestJS 不是标准的生产型完整架构，也不是要替代原生 Express 或数据库设计。

它更接近：

- 学习型中间层架构
- 框架对照模板
- 迁移练习入口
- 企业后端组织方式示例

真正的学习目标是：

1. 理解 NestJS 为什么要用 `Controller / Service / Module`
2. 理解为什么 `DTO` 和 `ValidationPipe` 能替代大量手工 if 校验
3. 理解为什么统一异常处理和统一返回结构如此重要
4. 理解为什么前端可以在同一个项目中切换 Express 和 NestJS，而不需要改大量页面逻辑

---

## 16. 实操建议：学习顺序

建议按下面顺序学习：

### 第一步：先看 Express

- `apps/api/src/server.ts`
- `apps/api/src/data/store.ts`

重点看：

- 路由注册
- cookie 认证
- 统一成功/失败返回
- 业务数据如何保存在内存中

### 第二步：再看 NestJS

- `apps/api-nestjs/src/main.ts`
- `apps/api-nestjs/src/app.module.ts`
- `apps/api-nestjs/src/product/product.controller.ts`
- `apps/api-nestjs/src/product/product.service.ts`
- `apps/api-nestjs/src/product/dto/create-product.dto.ts`

重点看：

- `@Controller()` 与 Express 路由的对应关系
- `@Injectable()` Service 的职责
- DTO 与 `ValidationPipe` 的作用
- 统一异常过滤器如何处理错误

### 第三步：对照 TypeScript 共享契约

- `packages/shared/src/index.ts`

重点看：

- `ApiResult<T>` 的统一设计
- `ProductInput` 与 `Product` 的区别
- 前端如何依赖共享类型减少接口误差

### 第四步：切换前端 API Base

在 `apps/web/src/api.ts` 中，前端默认指向 Express：

```ts
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8090/api'
```

通过环境变量切换到 NestJS：

```bash
VITE_API_BASE_URL=http://localhost:3002/api npm --workspace apps/web run dev -- --host 0.0.0.0
```

这样可以直接对比：

- 相同页面
- 相同业务逻辑
- 不同后端实现
- 前端行为几乎不变

这正是本项目最好的学习方式。

---

## 17. 常见坑点与避坑说明

### 17.1 路由前缀注意 `api`

NestJS 中通过：

```ts
app.setGlobalPrefix('api')
```

因此：

- `@Controller('products')` => `/api/products`
- 不是 `/products`

### 17.2 返回结构要统一

NestJS 中要与 Express 保持一致：

```ts
{ success: true, message: '...', data: ... }
```

如果只返回裸数据，前端会失去统一处理能力。

### 17.3 cookie 名称必须一致

现有代码使用：

- `jt_ts_session`
- `jt_ts_admin`

登录、会话恢复和权限校验都依赖这些 cookie 名称。只要其中一个不一致，认证就会失败。

### 17.4 DTO 的字段类型转换要注意

例如：

```ts
@Transform(({ value }) => Number(value))
@IsInt()
```

这类写法的意图是：

- 把前端字符串参数转换为数字
- 保持与 Express 中 `Number(request.params.id)` 类似的语义

### 17.5 数据层和业务层不能混在一起

在本学习项目中，Express 的 `Store` 是“数据访问层”，而 NestJS 的 `Service` 是“业务逻辑层”。

如果只看代码表面，可能会误以为两者完全相同；真正理解时，需要看：

- 数据在哪里存储
- 业务逻辑在哪里处理
- Controller 的职责是什么

---

## 18. 一句话总结

这个项目的 NestJS 学习版，本质上是：

“把原先手写、函数式、单文件的 Express 业务，重组成更接近企业项目的 `Controller + Service + Module + DTO + Filter` 结构，但仍然保留内存数据和共享 API 契约，不做复杂数据库重构。”

这让它同时具备两种价值：

- 对比学习：Express vs NestJS
- 渐进迁移：从脚手架式后端走向框架化后端

如果你想继续深入，可以把注意力放在下面几个文件：

- `apps/api-nestjs/src/main.ts`
- `apps/api-nestjs/src/app.module.ts`
- `apps/api-nestjs/src/product/product.controller.ts`
- `apps/api-nestjs/src/product/product.service.ts`
- `apps/api-nestjs/src/common/filters/http-exception.filter.ts`
- `packages/shared/src/index.ts`

这几处代码可以看作 NestJS 学习的“核心标本”。

---

## 19. 总结：适合什么人学

这个学习版特别适合以下人群：

- 已经接触过 Express / Node.js
- 想理解企业级后端框架组织方式
- 想对照 Spring Boot / NestJS / Express 的设计差异
- 想知道为什么前端、后端、公共类型要分层

如果你已经熟悉 Express，那么阅读 NestJS 版本时，最好的方式不是“从零重写”，而是“拿 Express 的业务和 NestJS 的结构逐项对照”。

这正是本项目最适合的学习路径。
