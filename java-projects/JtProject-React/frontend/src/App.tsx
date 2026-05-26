// 文件说明：
// 这是应用的壳组件，负责路由分发、全局状态（通过自定义 hook）以及
// 各种表单提交的集中处理（登录、注册、购物车、后台管理等）。
// 学习点：
// - 使用 `useNavigate` 做路由跳转
// - 把网络请求封装到服务层（services/appService）并在这里分发结果
// - 将回调和表单状态（来自 `useAppState`）传给子组件，保持视图组件尽量“瘦”
// 对应旧版 JSP：index.jsp（主页）、products.jsp / uproduct.jsp（商品列表）、cart.jsp（购物车）、
// adminlogin.jsp / adminHome.jsp（后台登录/首页）、userLogin.jsp / register.jsp（用户登录/注册）、
// categories.jsp、productsAdd.jsp、productsUpdate.jsp、displayCustomers.jsp、updateProfile.jsp（后台管理相关页面）
// 下面是常规的 React/路由导入
import { FormEvent } from 'react'
import { BrowserRouter, Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { AppLayout } from './layouts/AppLayout'
import { AdminDashboardView } from './views/AdminDashboardView'
import { AdminLoginView } from './views/AdminLoginView'
import { CartView } from './views/CartView'
import { ProductsView } from './views/ProductsView'
import { UserLoginView } from './views/UserLoginView'
import { useAppState } from './hooks/useAppState'
import {
  addToCartRequest,
  deleteCategoryRequest,
  deleteProductRequest,
  emptyCategoryForm,
  emptyProductForm,
  loginAdminRequest,
  loginUserRequest,
  logoutAdminRequest,
  logoutUserRequest,
  registerUserRequest,
  removeFromCartRequest,
  saveCategoryRequest,
  saveProductRequest,
  saveProfileRequest,
  type ProductForm
} from './services/appService'

function AppShell() {
  // useNavigate 是 React Router 提供的 hook，用来在代码中执行页面跳转（替代传统 location.href）
  // 例如： navigate('/products') 会把路由切换到 /products
  const navigate = useNavigate()

  // useAppState 是自定义的 Hook，集中管理应用级状态并返回当前状态与更新方法
  // 下面把 Hook 返回的对象解构成独立变量，按功能分组说明：
  // - message / setMessage: 用于显示全局提示（操作成功/失败信息）
  // - session / setSession: 当前会话信息（authenticated, username, role, adminLoggedIn 等）
  // - products / setProducts: 商品列表数据（用于商品页与后台管理）
  // - categories / setCategories: 商品分类列表
  // - cart / setCart: 当前用户的购物车项数组
  // - customers / setCustomers: 后台查看的用户列表
  // - overview / setOverview: 管理后台的统计概览（商品数/分类数/客户数等）
  // - userLogin / setUserLogin: 登录表单的受控状态（普通用户）
  // - registerForm / setRegisterForm: 注册表单的受控状态
  // - adminLogin / setAdminLogin: 管理员登录表单的受控状态
  // - categoryForm / setCategoryForm: 后台分类编辑表单状态
  // - productForm / setProductForm: 后台商品编辑表单状态
  // - profileForm / setProfileForm: 管理员个人资料表单状态
  // - refreshCart: 辅助函数，重新从后端加载购物车（用于登录后同步）
  // - refreshAdmin: 辅助函数，重新加载后台所需的数据集合（概览/客户/商品/分类）
  // 学习点：Hook 的返回值通常包含 "值" 与 "setter"，这是 React 状态管理的常见模式
  const {
    message,
    setMessage,
    session,
    setSession,
    products,
    setProducts,
    categories,
    setCategories,
    cart,
    setCart,
    customers,
    setCustomers,
    overview,
    setOverview,
    userLogin,
    setUserLogin,
    registerForm,
    setRegisterForm,
    adminLogin,
    setAdminLogin,
    categoryForm,
    setCategoryForm,
    productForm,
    setProductForm,
    profileForm,
    setProfileForm,
    refreshCart,
    refreshAdmin
  } = useAppState()

  // 登录、注册、购物车和后台管理都通过这层壳组件串联，
  // 这里负责把表单提交和路由跳转集中起来。
  async function handleUserLogin(event: FormEvent) {
    event.preventDefault()
    try {
      // 调用登录接口并把返回的会话对象写入全局状态
      setSession(await loginUserRequest(userLogin))
      // 登录后刷新当前用户的购物车数据（异步）
      await refreshCart()
      // 给用户一个简短的提示信息
      setMessage('User login successful.')
      // 登录成功后跳转到商品列表页
      navigate('/products')
    } catch (error) {
      // 捕获并展示错误信息（如认证失败）
      setMessage((error as Error).message)
    }
  }

  async function handleRegister(event: FormEvent) {
    event.preventDefault()
    try {
      // 调用注册接口并把返回的会话写入状态（自动登录）
      setSession(await registerUserRequest(registerForm))
      // 重置注册表单为初始空值，避免残留输入
      setRegisterForm({ username: '', email: '', password: '', address: '' })
      // 注册成功后刷新购物车（如果后台在注册时也有初始化）
      await refreshCart()
      setMessage('Registration successful.')
      // 注册后跳转到商品页
      navigate('/products')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleUserLogout() {
    try {
      // 调用登出接口，后端通常会清除会话或 token
      const nextSession = await logoutUserRequest()
      // 合并返回的会话信息（可能包含 authenticated=false）
      setSession((current) => ({ ...current, ...nextSession }))
      // 清空本地购物车状态
      setCart([])
      setMessage('User logout successful.')
      // 跳回登录页
      navigate('/login')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function addToCart(productId: number) {
    try {
      // 请求后端把商品加入购物车，并把最新的购物车数组写回状态
      setCart(await addToCartRequest(productId))
      // 给出成功提示
      setMessage('Product added to cart.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function removeFromCart(productId: number) {
    try {
      // 请求后端移除购物车项，后端返回更新后的购物车
      setCart(await removeFromCartRequest(productId))
      setMessage('Product removed from cart.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleAdminLogin(event: FormEvent) {
    event.preventDefault()
    try {
      // 调用管理员登录接口并合并会话信息（可能包含 admin 标志）
      const nextSession = await loginAdminRequest(adminLogin)
      setSession((current) => ({ ...current, ...nextSession }))
      // 登录后加载管理员所需的概览/客户/商品等数据
      await refreshAdmin()
      setMessage('Admin login successful.')
      // 管理员登录成功跳转到后台概览页
      navigate('/admin/dashboard')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleAdminLogout() {
    try {
      // 管理员登出，更新会话并清理后台状态
      const nextSession = await logoutAdminRequest()
      setSession((current) => ({ ...current, ...nextSession }))
      setOverview(null)
      setCustomers([])
      setMessage('Admin logout successful.')
      navigate('/admin/login')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  // 商品、分类和个人资料的保存/删除逻辑都在这里分发，
  // 组件层只需要把表单状态和回调传进来。
  async function submitCategory(event: FormEvent) {
    event.preventDefault()
    try {
      // 保存或更新分类，后端返回最新的分类列表
      setCategories(await saveCategoryRequest(categoryForm))
      // 重置分类表单为初始值
      setCategoryForm(emptyCategoryForm())
      setMessage('Category saved.')
      // 刷新后台数据以同步概览/商品等
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function deleteCategory(id: number) {
    try {
      // 请求后端删除分类，后端返回更新后的分类数组
      setCategories(await deleteCategoryRequest(id))
      setMessage('Category deleted.')
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function submitProduct(event: FormEvent) {
    event.preventDefault()
    try {
      // 保存或更新商品信息，后端返回新的商品列表
      setProducts(await saveProductRequest(productForm))
      // 重置商品表单（并根据当前分类列表选择默认分类）
      setProductForm(emptyProductForm(categories))
      setMessage('Product saved.')
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function deleteProduct(id: number) {
    try {
      // 删除商品并更新本地商品列表
      setProducts(await deleteProductRequest(id))
      setMessage('Product deleted.')
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function submitProfile(event: FormEvent) {
    event.preventDefault()
    try {
      // 提交管理员资料修改到后端，并用后端返回的结果更新表单（确保一致性）
      const result = await saveProfileRequest(profileForm)
      setProfileForm({
        username: result.username,
        email: result.email,
        password: result.password,
        address: result.address ?? ''
      })
      setMessage('Admin profile updated.')
      // 更新后台数据以反映资料变更
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  return (
    <AppLayout
      authenticated={session.authenticated}
      adminLoggedIn={session.adminLoggedIn}
      onUserLogout={handleUserLogout}
      onAdminLogout={handleAdminLogout}
    >
      {/* 根据登录态切换不同页面，未授权访问会回退到登录页。
          路由配置里每个 Route 的 element 接收父组件传入的回调和状态，
          保持子组件只负责展示与用户交互，不直接做网络请求。 */}
      <Routes>
        <Route
          path="/login"
          element={
            <UserLoginView
              message={message}
              userLogin={userLogin}
              registerForm={registerForm}
              setUserLogin={setUserLogin}
              setRegisterForm={setRegisterForm}
              onLogin={handleUserLogin}
              onRegister={handleRegister}
            />
          }
        />
        <Route
          path="/products"
          element={<ProductsView session={session} products={products} message={message} onAddToCart={addToCart} />}
        />
        <Route
          path="/cart"
          element={session.authenticated ? <CartView session={session} cart={cart} message={message} onRemoveFromCart={removeFromCart} /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/admin/login"
          element={<AdminLoginView message={message} adminLogin={adminLogin} setAdminLogin={setAdminLogin} onLogin={handleAdminLogin} />}
        />
        <Route
          path="/admin/dashboard"
          element={
            session.adminLoggedIn ? (
              <AdminDashboardView
                message={message}
                overview={overview}
                categories={categories}
                products={products}
                customers={customers}
                profileForm={profileForm}
                categoryForm={categoryForm}
                productForm={productForm}
                setCategoryForm={setCategoryForm}
                setProductForm={setProductForm}
                setProfileForm={setProfileForm}
                onSubmitCategory={submitCategory}
                onDeleteCategory={deleteCategory}
                onSubmitProduct={submitProduct}
                onDeleteProduct={deleteProduct}
                onSubmitProfile={submitProfile}
              />
            ) : (
              <Navigate to="/admin/login" replace />
            )
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AppLayout>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      {/* BrowserRouter: 把整个 React 应用包裹为一个路由上下文，使 useNavigate、Routes、Link 等路由功能可用 */}
      <AppShell />
    </BrowserRouter>
  )
}
