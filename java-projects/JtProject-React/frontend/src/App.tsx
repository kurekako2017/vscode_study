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
  const navigate = useNavigate()
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
      setSession(await loginUserRequest(userLogin))
      await refreshCart()
      setMessage('User login successful.')
      navigate('/products')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleRegister(event: FormEvent) {
    event.preventDefault()
    try {
      setSession(await registerUserRequest(registerForm))
      setRegisterForm({ username: '', email: '', password: '', address: '' })
      await refreshCart()
      setMessage('Registration successful.')
      navigate('/products')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleUserLogout() {
    try {
      const nextSession = await logoutUserRequest()
      setSession((current) => ({ ...current, ...nextSession }))
      setCart([])
      setMessage('User logout successful.')
      navigate('/login')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function addToCart(productId: number) {
    try {
      setCart(await addToCartRequest(productId))
      setMessage('Product added to cart.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function removeFromCart(productId: number) {
    try {
      setCart(await removeFromCartRequest(productId))
      setMessage('Product removed from cart.')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleAdminLogin(event: FormEvent) {
    event.preventDefault()
    try {
      const nextSession = await loginAdminRequest(adminLogin)
      setSession((current) => ({ ...current, ...nextSession }))
      await refreshAdmin()
      setMessage('Admin login successful.')
      navigate('/admin/dashboard')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function handleAdminLogout() {
    try {
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
      setCategories(await saveCategoryRequest(categoryForm))
      setCategoryForm(emptyCategoryForm())
      setMessage('Category saved.')
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function deleteCategory(id: number) {
    try {
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
      setProducts(await saveProductRequest(productForm))
      setProductForm(emptyProductForm(categories))
      setMessage('Product saved.')
      await refreshAdmin()
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  async function deleteProduct(id: number) {
    try {
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
      const result = await saveProfileRequest(profileForm)
      setProfileForm({
        username: result.username,
        email: result.email,
        password: result.password,
        address: result.address ?? ''
      })
      setMessage('Admin profile updated.')
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
      {/* 根据登录态切换不同页面，未授权访问会回退到登录页。 */}
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
      <AppShell />
    </BrowserRouter>
  )
}
