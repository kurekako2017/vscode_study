*&---------------------------------------------------------------------*
*& ABAP 类: lhc_product
*& 说明: Product 业务对象的行为实现类
*& 功能: 实现 Determination 和 Validation 的业务逻辑
*& 继承: cl_abap_behavior_handler (RAP 行为处理基类)
*&---------------------------------------------------------------------*

@EndUserText.label: 'Product BO Implementation'
CLASS lhc_product DEFINITION INHERITING FROM cl_abap_behavior_handler.

  PUBLIC SECTION.
    " 类构造方法：在类首次加载时执行
    CLASS-METHODS class_constructor.

  PRIVATE SECTION.
    " ===== Determination 方法 =====
    " set_defaults: 设置默认值
    " 在创建产品时自动设置创建时间和创建人
    METHODS set_defaults FOR DETERMINATION Product~set_defaults
      IMPORTING keys FOR Product.

    " ===== Validation 方法 =====
    " check_price_positive: 检查价格是否为正数
    " 验证产品价格必须大于 0
    METHODS check_price_positive FOR VALIDATION Product~check_price_positive
      IMPORTING keys FOR Product.

ENDCLASS.

*&---------------------------------------------------------------------*
* 类实现部分
*&---------------------------------------------------------------------*
CLASS lhc_product IMPLEMENTATION.

  " ===== 类构造方法 =====
  " 说明: 首次使用该类时自动调用
  CLASS-METHOD class_constructor.
    " 此处可以做类级别的初始化
  ENDMETHOD.

  " ===== Determination 实现: set_defaults =====
  " 功能: 在创建产品时自动设置审计字段
  " 逻辑:
  "   1. 接收要创建的产品 ID 列表 (keys)
  "   2. 更新这些产品的创建时间 (sy-datum 当前日期)
  "   3. 更新创建人 (sy-uname 当前用户)
  METHOD set_defaults.
    " MODIFY ENTITIES: 修改实体
    " OF zproduct: 操作 zproduct 实体
    " IN LOCAL MODE: 本地模式（不涉及事务）
    MODIFY ENTITIES OF zproduct IN LOCAL MODE
      ENTITY product                     " 操作产品实体
        UPDATE SET (                     " 更新设置
          created_at = sy-datum,         " 设置创建日期为系统当前日期
          created_by = sy-uname          " 设置创建人为系统当前用户
        )
        WHERE product_id IN ( SELECT product_id FROM table( keys ) ).
  ENDMETHOD.

  " ===== Validation 实现: check_price_positive =====
  " 功能: 验证产品价格必须为正数
  " 逻辑:
  "   1. 读取要验证的产品的价格字段
  "   2. 循环检查每个产品的价格
  "   3. 如果价格 < 0，生成错误消息
  "   4. 将错误消息加入到验证报告
  METHOD check_price_positive.
    " READ ENTITIES: 读取实体
    " OF zproduct: 从 zproduct 实体读取
    " IN LOCAL MODE: 本地模式
    READ ENTITIES OF zproduct IN LOCAL MODE
      ENTITY product                     " 读取产品实体
        FIELDS ( price )                 " 只读取价格字段
        WITH CORRESPONDING #( keys )     " 映射 keys 参数
      RESULT DATA(lt_product).           " 结果保存到 lt_product
    
    " ===== 验证逻辑 =====
    " 循环遍历所有读取的产品
    LOOP AT lt_product INTO DATA(ls_product)
      WHERE price < 0.  " 条件: 价格小于 0
      
      " 添加错误消息到验证报告
      APPEND VALUE #(
        %key = ls_product-%key           " 标记该行的键值
        %msg = new_message(              " 创建新消息
          id = 'ZCM_PRODUCT'             " 消息 ID
          number = '001'                 " 消息编号
          severity = if_abap_behv=>mk_severity_error  " 错误级别
          v1 = 'Price must be positive'  " 错误文本
        )
      ) TO reported-product.             " 添加到 reported 表
      
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
