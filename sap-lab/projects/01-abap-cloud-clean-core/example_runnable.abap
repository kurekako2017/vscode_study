*&---------------------------------------------------------------------*
*& Report ZEXAMPLE_CLEAN_CORE_RUNNABLE
*&---------------------------------------------------------------------*
*& 程序名称: ZEXAMPLE_CLEAN_CORE_RUNNABLE
*& 程序说明: ABAP Cloud 示例程序 - 遵循 Clean Core 原则 (可执行版本)
*&          该程序演示如何使用面向对象的方式组织代码，
*&          将业务逻辑分离到单独的服务类中
*& 创建人: 系统
*& 创建日期: 2025-12-31
*& 注意: 这是一个简化版本，模拟数据库操作
*&---------------------------------------------------------------------*

REPORT zexample_clean_core_runnable.

*----------------------------------------------------------------------*
* 产品数据结构定义
* 说明: 定义产品的数据结构
*----------------------------------------------------------------------*
TYPES: BEGIN OF ty_product,
         product_id    TYPE i,           " 产品编号
         product_name  TYPE string,      " 产品名称
         description   TYPE string,      " 产品描述
         price         TYPE p DECIMALS 2, " 产品价格
       END OF ty_product.

*----------------------------------------------------------------------*
* 全局数据定义区域
* 说明: 定义全局变量和数据结构，用于存储产品信息
*----------------------------------------------------------------------*
DATA: gt_products TYPE TABLE OF ty_product,     " 产品列表 (内表)
      gs_product  TYPE ty_product.              " 单个产品 (结构)

*----------------------------------------------------------------------*
* 业务逻辑类定义 - lcl_product_service
* 说明: 这是一个本地类(lcl)，包含所有产品相关的业务逻辑
*       遵循 Clean Core 原则：
*       1. 关注点分离 - 将业务逻辑与报表逻辑分开
*       2. 单一职责 - 每个方法只负责一个业务功能
*       3. 易于测试 - 可以独立测试业务逻辑
*       4. 易于维护 - 代码组织清晰，易于理解和修改
*----------------------------------------------------------------------*
CLASS lcl_product_service DEFINITION.
  " =====================================================
  " 公开部分 - 定义该类对外暴露的接口
  " =====================================================
  PUBLIC SECTION.
    
    "-----------------------------------------------------
    " 方法1: get_products - 获取产品列表
    " 说明: 从模拟数据库查询所有产品信息
    " 返回值: rt_products - 产品列表内表
    "-----------------------------------------------------
    METHODS get_products
      RETURNING VALUE(rt_products) TYPE TABLE OF ty_product.
    
    "-----------------------------------------------------
    " 方法2: create_product - 创建新产品
    " 说明: 将新产品信息添加到内表
    " 参数: is_product - 要创建的产品对象
    " 返回值: rv_success - 是否创建成功 (true/false)
    "-----------------------------------------------------
    METHODS create_product
      IMPORTING is_product TYPE ty_product
      RETURNING VALUE(rv_success) TYPE abap_bool.
    
    "-----------------------------------------------------
    " 方法3: get_product_count - 获取产品总数
    " 说明: 返回当前系统中产品的总数
    " 返回值: 产品数量
    "-----------------------------------------------------
    METHODS get_product_count
      RETURNING VALUE(rv_count) TYPE i.

ENDCLASS.

*----------------------------------------------------------------------*
* 业务逻辑类实现 - lcl_product_service
* 说明: 实现上面定义的所有业务逻辑方法
*----------------------------------------------------------------------*
CLASS lcl_product_service IMPLEMENTATION.

  "-------------------------------------------------------
  " 方法实现: get_products
  " 功能: 获取所有产品 (从全局内表)
  " 逻辑流程:
  "   1. 将全局产品列表复制到返回参数
  "   2. 返回产品列表
  "-------------------------------------------------------
  METHOD get_products.
    " 将全局产品列表赋值给返回参数
    rt_products = gt_products.
  ENDMETHOD.

  "-------------------------------------------------------
  " 方法实现: create_product
  " 功能: 创建新产品
  " 逻辑流程:
  "   1. 接收产品参数
  "   2. 验证产品数据有效性
  "   3. 将产品添加到内表
  "   4. 返回成功标记
  "-------------------------------------------------------
  METHOD create_product.
    " 创建产品业务逻辑
    
    " ===== 数据有效性检查 =====
    " 检查产品 ID 是否有效
    IF is_product-product_id <= 0.
      WRITE: / 'ERROR: 产品 ID 必须大于 0'.
      rv_success = abap_false.
      RETURN.
    ENDIF.
    
    " 检查产品名称是否为空
    IF is_product-product_name IS INITIAL.
      WRITE: / 'ERROR: 产品名称不能为空'.
      rv_success = abap_false.
      RETURN.
    ENDIF.
    
    " 检查产品价格是否有效
    IF is_product-price <= 0.
      WRITE: / 'ERROR: 产品价格必须大于 0'.
      rv_success = abap_false.
      RETURN.
    ENDIF.
    
    " ===== 添加产品 =====
    " 将产品对象添加到内表中
    APPEND is_product TO gt_products.
    
    " ===== 返回成功 =====
    rv_success = abap_true.
  ENDMETHOD.

  "-------------------------------------------------------
  " 方法实现: get_product_count
  " 功能: 获取产品总数
  " 逻辑流程:
  "   1. 使用 lines() 函数获取内表行数
  "   2. 返回产品数量
  "-------------------------------------------------------
  METHOD get_product_count.
    " 获取内表中产品的总数
    rv_count = lines( gt_products ).
  ENDMETHOD.

ENDCLASS.

*----------------------------------------------------------------------*
* 主程序入口点
* 说明: START-OF-SELECTION 是报表程序的主入口
*       此部分代码在用户点击"执行"(F8)后执行
*----------------------------------------------------------------------*
START-OF-SELECTION.
  
  "-----------------------------------------------------
  " 标题输出
  "-----------------------------------------------------
  WRITE: / '==============================================='.
  WRITE: / 'ABAP Cloud Clean Core 示例程序 - 执行结果'.
  WRITE: / '==============================================='.
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 第1步: 创建服务对象实例
  "-----------------------------------------------------
  WRITE: / '[第1步] 创建服务对象实例...'.
  DATA(lo_service) = NEW lcl_product_service( ).
  WRITE: / '✓ 服务对象创建成功'.
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 第2步: 添加示例产品
  "-----------------------------------------------------
  WRITE: / '[第2步] 添加示例产品...'.
  
  " 添加产品 1
  gs_product-product_id = 1.
  gs_product-product_name = 'ABAP 教科书'.
  gs_product-description = 'ABAP 开发完全指南'.
  gs_product-price = '89.99'.
  
  IF lo_service->create_product( gs_product ) = abap_true.
    WRITE: / '✓ 产品 1 添加成功: ' && gs_product-product_name.
  ENDIF.
  
  " 添加产品 2
  gs_product-product_id = 2.
  gs_product-product_name = 'SAP 云开发'.
  gs_product-description = '使用 RAP 进行 SAP 云开发'.
  gs_product-price = '129.99'.
  
  IF lo_service->create_product( gs_product ) = abap_true.
    WRITE: / '✓ 产品 2 添加成功: ' && gs_product-product_name.
  ENDIF.
  
  " 添加产品 3
  gs_product-product_id = 3.
  gs_product-product_name = 'CDS 视图深度讲解'.
  gs_product-description = 'Core Data Services 完整教程'.
  gs_product-price = '99.99'.
  
  IF lo_service->create_product( gs_product ) = abap_true.
    WRITE: / '✓ 产品 3 添加成功: ' && gs_product-product_name.
  ENDIF.
  
  " 尝试添加无效产品 (测试验证)
  WRITE: / ''.
  WRITE: / '尝试添加无效产品 (ID 为负数):'.
  gs_product-product_id = -1.
  gs_product-product_name = '无效产品'.
  gs_product-price = '50.00'.
  
  IF lo_service->create_product( gs_product ) <> abap_true.
    WRITE: / '✓ 系统正确拒绝了无效数据'.
  ENDIF.
  
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 第3步: 获取产品列表
  "-----------------------------------------------------
  WRITE: / '[第3步] 获取产品列表...'.
  DATA(lt_products) = lo_service->get_products( ).
  WRITE: / '✓ 产品列表获取成功'.
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 第4步: 输出统计信息
  "-----------------------------------------------------
  WRITE: / '[第4步] 统计结果:'.
  DATA(lv_count) = lo_service->get_product_count( ).
  WRITE: / '总产品数:', lv_count.
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 第5步: 详细信息
  "-----------------------------------------------------
  WRITE: / '[第5步] 产品详细列表:'.
  WRITE: / '-----------------------------------------------'.
  WRITE: / '| 编号 | 产品名称 | 价格 |'.
  WRITE: / '-----------------------------------------------'.
  
  IF lv_count > 0.
    LOOP AT lt_products INTO gs_product.
      WRITE: / '| ' && gs_product-product_id && ' | ' 
              && gs_product-product_name && ' | ¥' 
              && gs_product-price && ' |'.
    ENDLOOP.
  ELSE.
    WRITE: / '(无产品信息)'.
  ENDIF.
  
  WRITE: / '-----------------------------------------------'.
  WRITE: / ''.
  
  "-----------------------------------------------------
  " 程序完成
  "-----------------------------------------------------
  WRITE: / '[完成] 程序执行成功！'.
  WRITE: / '==============================================='.
