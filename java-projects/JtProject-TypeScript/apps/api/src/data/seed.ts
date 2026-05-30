import type { Category, Product, User } from '../../../../packages/shared/src/index'

// 这份 seed 数据来自原始 JtProject 的 data.sql。
// 纯 TypeScript 版先使用内存数据仓库，便于把学习重点放在 API、类型和前端调用流程上。
//
// 读这个文件时可以把它理解成“用 TypeScript 写出来的 data.sql”：
// - SQL 里的 CATEGORY 表 -> categories 数组
// - SQL 里的 CUSTOMER 表 -> users 数组
// - SQL 里的 PRODUCT 表 -> products 数组
//
// 这里导出的数组会在 Store 里被 structuredClone 复制一份。
// 这样运行时修改商品或购物车，不会直接污染原始 seed 常量。

export const categories: Category[] = [
  { id: 1, name: 'Fruits' },
  { id: 2, name: 'Vegetables' },
  { id: 3, name: 'Meat' },
  { id: 4, name: 'Fish' },
  { id: 5, name: 'Dairy' },
  { id: 6, name: 'Bakery' },
  { id: 7, name: 'Drinks' },
  { id: 8, name: 'Sweets' },
  { id: 9, name: 'Other' }
]

export const users: User[] = [
  // 管理员账号，对应原始项目默认 admin / 123。
  {
    id: 1,
    address: '123, Albany Street',
    email: 'admin@nyan.cat',
    password: '123',
    role: 'ROLE_ADMIN',
    username: 'admin'
  },
  // 普通用户账号，对应原始项目默认 lisa / 765。
  {
    id: 2,
    address: '765, 5th Avenue',
    email: 'lisa@gmail.com',
    password: '765',
    role: 'ROLE_NORMAL',
    username: 'lisa'
  }
]

export const products: Product[] = [
  // 原始项目里的 Apple 商品。
  {
    id: 1,
    description: 'Fresh and juicy',
    image: 'https://freepngimg.com/save/9557-apple-fruit-transparent/744x744',
    name: 'Apple',
    price: 3,
    quantity: 40,
    weight: 76,
    categoryId: 1,
    categoryName: 'Fruits'
  },
  // 原始项目里的 Cracked Eggs 商品。
  {
    id: 2,
    description: 'Woops! There goes the eggs...',
    image: 'https://www.nicepng.com/png/full/813-8132637_poiata-bunicii-cracked-egg.png',
    name: 'Cracked Eggs',
    price: 1,
    quantity: 90,
    weight: 43,
    categoryId: 9,
    categoryName: 'Other'
  }
]
