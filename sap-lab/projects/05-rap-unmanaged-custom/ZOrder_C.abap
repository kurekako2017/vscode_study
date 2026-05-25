*&---------------------------------------------------------------------*
*& ABAP 类: lhc_order
*& 说明: Order 业务对象的 Unmanaged 实现类
*& 功能: 手动实现 CRUD、Determination、Validation、Action
*& 特点: Unmanaged 模式需要完全手动实现所有操作
*&---------------------------------------------------------------------*

@EndUserText.label: 'Order BO Implementation'
CLASS lhc_order DEFINITION INHERITING FROM cl_abap_behavior_handler.

  PUBLIC SECTION.
    // 类构造方法
    CLASS-METHODS class_constructor.

  PRIVATE SECTION.
    
    // ===== CRUD 操作 - Unmanaged 模式需要手动实现 =====
    // CREATE: 创建新订单
    METHODS create FOR CREATE Order.
    
    // READ: 读取订单信息
    METHODS read FOR READ Order RESULT RESULT.
    
    // UPDATE: 修改订单
    METHODS update FOR UPDATE Order.
    
    // DELETE: 删除订单
    METHODS delete FOR DELETE Order.

    // ===== Determination 方法 =====
    // set_order_number: 自动生成订单号
    METHODS set_order_number FOR DETERMINATION Order~set_order_number
      IMPORTING keys FOR Order.

    // calculate_total: 计算订单总金额
    METHODS calculate_total FOR DETERMINATION Order~calculate_total
      IMPORTING keys FOR Order.

    // ===== Validation 方法 =====
    // validate_customer: 验证客户是否存在
    METHODS validate_customer FOR VALIDATION Order~validate_customer
      IMPORTING keys FOR Order.

    // ===== Action 方法 =====
    // approve: 批准订单
    METHODS approve FOR ACTION Order~approve
      IMPORTING keys FOR ACTION Order
      RESULT result.

ENDCLASS.

*&---------------------------------------------------------------------*
* 类实现部分
*&---------------------------------------------------------------------*
CLASS lhc_order IMPLEMENTATION.

  // ===== 类构造方法 =====
  CLASS-METHOD class_constructor.
    // 类初始化
  ENDMETHOD.

  // ===== CREATE 操作实现 =====
  // 功能: 创建新订单
  // 逻辑:
  "   1. 接收要插入的订单对象
  "   2. 生成唯一的订单号 (UUID)
  "   3. 将订单插入数据库
  METHOD create.
    " 自定义创建逻辑
    " 使用 UUID 工厂生成唯一的订单号
    INSERT zorders FROM @( VALUE #(
      order_number = cl_uuid_factory=>create_system_uuid( )->create_uuid_x16( )
      ( entity mapping from entry )  " 从请求实体映射字段
    ) ).
  ENDMETHOD.

  // ===== READ 操作实现 =====
  // 功能: 读取订单信息
  // 逻辑:
  "   1. 根据 keys 过滤条件
  "   2. 从数据库查询订单
  "   3. 返回结果集合
  METHOD read.
    " 自定义读取逻辑
    " 查询满足条件的订单记录
    SELECT * FROM zorders 
      INTO TABLE @result 
      WHERE order_id IN ( SELECT order_id FROM table( @keys ) ).
  ENDMETHOD.

  // ===== Determination: set_order_number =====
  // 功能: 自动为订单生成唯一订单号
  // 触发: 订单保存时 (create)
  // 逻辑:
  "   1. 接收要处理的订单 ID 列表
  "   2. 为每个订单生成 UUID 格式的订单号
  "   3. 更新订单表
  METHOD set_order_number.
    " 自动生成订单号
    MODIFY ENTITIES OF zorder IN LOCAL MODE
      ENTITY order
        UPDATE SET (
          " 生成 16 字节的 UUID 作为订单号
          order_number = cl_uuid_factory=>create_system_uuid( )->create_uuid_x16( )
        )
        WHERE order_id IN ( SELECT order_id FROM table( keys ) ).
  ENDMETHOD.

  // ===== Determination: calculate_total =====
  // 功能: 计算订单的总金额
  // 触发: 订单保存时 (create 和 update)
  // 逻辑:
  "   1. 读取订单的 ID
  "   2. 查询该订单的所有订单项
  "   3. 求和计算总金额
  "   4. 更新订单的总金额字段
  METHOD calculate_total.
    " 计算订单总额
    " 第1步: 读取订单信息
    READ ENTITIES OF zorder IN LOCAL MODE
      ENTITY order
        FIELDS ( order_id )                // 只读订单 ID
        WITH CORRESPONDING #( keys )       // 映射输入的 keys
      RESULT DATA(lt_orders).

    " 第2步: 循环处理每个订单
    LOOP AT lt_orders INTO DATA(ls_order).
      " 查询该订单所有项的金额总和
      SELECT SUM( amount ) AS total_amount
        FROM zorder_items
        WHERE order_id = @ls_order-order_id
        INTO @DATA(ls_total).

      " 更新订单的总金额字段
      MODIFY ENTITY zorder IN LOCAL MODE
        UPDATE SET (
          total_amount = ls_total-total_amount  " 设置计算的总金额
        )
        WHERE order_id = @ls_order-order_id.
    ENDLOOP.
  ENDMETHOD.

  // ===== Validation: validate_customer =====
  // 功能: 验证订单的客户是否存在
  // 触发: 订单保存时 (create 和 update)
  // 逻辑:
  "   1. 读取订单的客户 ID
  "   2. 检查该客户是否存在于客户表
  "   3. 如果不存在，添加错误消息
  METHOD validate_customer.
    " 读取订单的客户 ID 字段
    READ ENTITIES OF zorder IN LOCAL MODE
      ENTITY order
        FIELDS ( customer_id )             // 只读客户 ID
        WITH CORRESPONDING #( keys )       // 映射输入的 keys
      RESULT DATA(lt_orders).

    " 循环验证每个订单的客户
    LOOP AT lt_orders INTO DATA(ls_order).
      " 检查客户是否存在
      SELECT SINGLE customer_id FROM zcustomers
        WHERE customer_id = @ls_order-customer_id
        INTO @DATA(lv_customer_id).

      " 如果查询返回非 0 (即未找到该客户)
      IF sy-subrc <> 0.
        " 生成验证错误消息
        APPEND VALUE #(
          %key = ls_order-%key              " 标记出错的记录
          %msg = new_message(               " 创建错误消息
            id = 'ZCM_ORDER'                " 消息 ID
            number = '001'                  " 消息编号
            severity = if_abap_behv=>mk_severity_error  " 错误严重级别
            v1 = 'Customer not found'       " 错误描述
          )
        ) TO reported-order.               " 添加到验证报告
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  // ===== Action: approve =====
  // 功能: 批准订单的自定义操作
  // 逻辑:
  "   1. 接收要批准的订单 ID
  "   2. 将订单状态更改为 'APPROVED'
  "   3. 返回更新后的订单
  METHOD approve.
    " 批准订单: 更新订单状态为已批准
    MODIFY ENTITIES OF zorder IN LOCAL MODE
      ENTITY order
        UPDATE SET ( order_status = 'APPROVED' )  " 状态改为已批准
        WHERE order_id IN ( SELECT order_id FROM table( keys ) ).
  ENDMETHOD.

ENDCLASS.
