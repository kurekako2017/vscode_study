import type { Category, Product, ProductInput, User } from '../../../../packages/shared/src/index'
import { categories as seedCategories, products as seedProducts, users as seedUsers } from './seed'

// Store 是一个很小的内存数据层。
// 它在纯 TypeScript 版里扮演原始项目 DAO + 数据库的角色，接口层不直接操作数组细节。
//
// 为什么要有 Store，而不是在 server.ts 里直接操作数组？
// 1. server.ts 专心处理 HTTP 请求和响应。
// 2. Store 专心处理数据查询、增删改查和购物车状态。
// 3. 以后如果要把内存数据换成 SQLite/PostgreSQL，只需要优先改 Store 这一层。
export class Store {
  // private 表示这些数组只能在 Store 内部直接修改。
  // 外部必须通过 getProducts/addCartItem 等方法访问，边界更清楚。
  private categories: Category[] = structuredClone(seedCategories)
  private users: User[] = structuredClone(seedUsers)
  private products: Product[] = structuredClone(seedProducts)

  // carts 用 Map 表示“用户 id -> 商品 id 列表”。
  // 这相当于原始项目里的 CART + CART_PRODUCT 两张表的简化内存版。
  private carts = new Map<number, number[]>()

  // 返回分类数组。
  // 学习版直接返回引用；真实项目通常会返回副本或 DTO，避免外部直接改内部数据。
  getCategories() {
    return this.categories
  }

  // 返回用户数组，供后台统计 customerCount 使用。
  getUsers() {
    return this.users
  }

  // 返回商品数组，供 GET /api/products 和后台商品列表使用。
  getProducts() {
    return this.products
  }

  // 根据用户名查用户。
  // 登录、注册查重、cookie 恢复会话都会用到它。
  findUserByUsername(username: string) {
    return this.users.find((user) => user.username === username)
  }

  // 校验用户名和密码。
  // 原始项目是 UserService.checkLogin，这里把逻辑放进 Store。
  checkLogin(username: string, password: string) {
    return this.users.find((user) => user.username === username && user.password === password)
  }

  // 注册普通用户。
  // Omit<User, 'id' | 'role'> 表示调用方不能传 id 和 role，这两个字段由后端决定。
  registerUser(input: Omit<User, 'id' | 'role'>) {
    const user: User = {
      ...input,
      id: this.nextId(this.users),
      role: 'ROLE_NORMAL'
    }
    this.users.push(user)
    return user
  }

  // 根据用户 id 取购物车商品。
  // carts 里保存的是 productId，所以这里要把 id 转回完整 Product 对象给前端渲染。
  getCartProducts(userId: number) {
    const productIds = this.carts.get(userId) ?? []
    return productIds.flatMap((id) => this.products.find((product) => product.id === id) ?? [])
  }

  // 添加购物车商品。
  // 这里允许重复添加同一个商品，因此 cart 是 productId 数组，而不是 Set。
  addCartItem(userId: number, productId: number) {
    const current = this.carts.get(userId) ?? []
    this.carts.set(userId, [...current, productId])
    return this.getCartProducts(userId)
  }

  // 删除购物车里的一个商品。
  // 如果同一个商品加了多次，这里只删除第一个匹配项，模拟“一次移除一件”。
  removeCartItem(userId: number, productId: number) {
    const current = this.carts.get(userId) ?? []
    const index = current.indexOf(productId)
    if (index >= 0) {
      current.splice(index, 1)
    }
    this.carts.set(userId, current)
    return this.getCartProducts(userId)
  }

  // 创建商品。
  // 前端提交的是 ProductInput，Store 会补上 id 和 categoryName，变成完整 Product。
  createProduct(input: ProductInput) {
    const product = this.toProduct(input, this.nextId(this.products))
    this.products.push(product)
    return product
  }

  // 更新商品。
  // 找不到 id 时返回 null，让 server.ts 决定返回 404。
  updateProduct(id: number, input: ProductInput) {
    const index = this.products.findIndex((product) => product.id === id)
    if (index < 0) {
      return null
    }
    const product = this.toProduct(input, id)
    this.products[index] = product
    return product
  }

  // 删除商品后返回新的商品列表，方便接口直接把最新列表给前端。
  deleteProduct(id: number) {
    this.products = this.products.filter((product) => product.id !== id)
    return this.products
  }

  // 把表单输入转换成完整 Product。
  // 这是一个集中转换点：categoryId -> categoryName 的逻辑都在这里。
  private toProduct(input: ProductInput, id: number): Product {
    const category = this.categories.find((item) => item.id === input.categoryId)
    return {
      id,
      ...input,
      categoryName: category?.name ?? 'Uncategorized'
    }
  }

  // 简单生成下一个 id。
  // 内存学习版可以这样做；真实并发系统通常交给数据库自增或 UUID。
  private nextId(items: Array<{ id: number }>) {
    return Math.max(0, ...items.map((item) => item.id)) + 1
  }
}
