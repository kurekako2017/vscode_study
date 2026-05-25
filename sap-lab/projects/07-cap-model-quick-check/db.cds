*&---------------------------------------------------------------------*
*& CAP 数据库模型: db.cds
*& 说明: 定义核心业务实体和数据结构
*& 特点: 使用 CAP 提供的通用功能（cuid、managed）
*& 关系: 产品、价格、客户、订单、订单项的完整数据模型
*&---------------------------------------------------------------------*

// 定义命名空间
namespace sap.catalog;

// 导入 CAP 通用功能
using { 
  cuid,       // 自动生成唯一 ID 的类型
  managed     // 提供创建人、创建时间、修改人、修改时间等字段
} from '@sap/cds/common';

// =====================================================
// 产品实体 (Products)
// =====================================================
entity Products : cuid, managed {
  product_name        : String(255) not null;    // 产品名称 (必填)
  description         : String(1000);             // 产品描述
  category            : String(100) not null;    // 产品分类 (必填)
  price               : Decimal(15, 2) not null; // 价格 (必填)
  currency            : String(3) default 'USD'; // 货币代码 (默认美元)
  stock_quantity      : Integer default 0;       // 库存数量 (默认 0)
  is_active           : Boolean default true;    // 是否激活 (默认激活)
  
  // 一对多关系: 一个产品可以有多个价格记录
  compositions composition [0..*] of Prices on prices.product
}

// =====================================================
// 价格实体 (Prices)
// =====================================================
entity Prices : cuid, managed {
  product             : Association to Products; // 关联到产品
  currency            : String(3);               // 货币代码
  amount              : Decimal(15, 2) not null; // 金额 (必填)
  discount_percent    : Decimal(5, 2) default 0; // 折扣百分比
  effective_from      : Date;                    // 生效日期
  effective_to        : Date;                    // 失效日期
}

// =====================================================
// 客户实体 (Customers)
// =====================================================
entity Customers : cuid, managed {
  customer_name       : String(255) not null;    // 客户名称 (必填)
  email               : String(255);              // 电子邮件
  phone               : String(20);               // 电话号码
  address             : String(500);              // 地址
  city                : String(100);              // 城市
  country             : String(100);              // 国家
  
  // 一对多关系: 一个客户可以有多个订单
  orders              : composition [0..*] of Orders on orders.customer
}

// =====================================================
// 订单实体 (Orders)
// =====================================================
entity Orders : cuid, managed {
  customer            : Association to Customers; // 关联到客户
  order_number        : String(20) unique not null; // 订单号 (唯一，必填)
  order_date          : Date not null;            // 订单日期 (必填)
  total_amount        : Decimal(15, 2);           // 订单总金额
  status              : String(20) default 'PENDING'; // 订单状态 (默认待处理)
  
  // 一对多关系: 一个订单可以有多个订单项
  items               : composition [0..*] of OrderItems on items.order
}

// =====================================================
// 订单项实体 (OrderItems)
// =====================================================
entity OrderItems : cuid, managed {
  order               : Association to Orders;   // 关联到订单
  product             : Association to Products; // 关联到产品
  quantity            : Integer not null;        // 数量 (必填)
  unit_price          : Decimal(15, 2) not null; // 单价 (必填)
  line_amount         : Decimal(15, 2) not null; // 行金额 (必填)
}
