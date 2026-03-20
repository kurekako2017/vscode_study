# Java 基础教程

## 1. Java 程序是如何运行的

编写 `.java` 文件后，Java 编译器会把它编译成 `.class` 字节码文件，然后由 JVM 执行。

流程:

1. 编写源代码
2. 使用 `javac` 编译
3. 使用 `java` 运行

示例:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
```

## 2. Java 基础语法

### 变量与数据类型

常见类型:

- `int`
- `long`
- `double`
- `boolean`
- `char`
- `String`

### 流程控制

- `if / else`
- `switch`
- `for`
- `while`
- `do-while`

### 方法

重点:

- 参数
- 返回值
- 方法重载

## 3. 面向对象

### 类与对象

类是模板，对象是实例。

### 封装

通过 `private` 隐藏内部数据，通过 getter/setter 提供访问。

### 继承

子类复用父类能力。

### 多态

父类引用指向子类对象，运行时表现不同。

### 接口

用于定义统一行为规范。

## 4. 常用基础类

- `String`
- `StringBuilder`
- `Math`
- `LocalDate`
- `LocalDateTime`
- `BigDecimal`

企业开发中尤其要重视:

- 金额运算使用 `BigDecimal`
- 日期时间使用 `java.time`

## 5. 集合框架

### List

- 有序
- 可重复
- 常见实现: `ArrayList`, `LinkedList`

### Set

- 不可重复
- 常见实现: `HashSet`

### Map

- 键值对
- 常见实现: `HashMap`

学习重点:

- 遍历
- 增删改查
- 泛型
- 选择合适的数据结构

## 6. 异常处理

### 异常分类

- 检查型异常
- 运行时异常

### 关键字

- `try`
- `catch`
- `finally`
- `throw`
- `throws`

企业项目要求:

- 不要吞异常
- 记录关键日志
- 给出有意义的错误信息

## 7. IO 和文件处理

常见场景:

- 读取配置文件
- 导入 CSV
- 输出日志
- 生成报表

## 8. 多线程基础

需要了解:

- `Thread`
- `Runnable`
- 线程安全
- `synchronized`
- 线程池

即使在初级阶段，也要建立正确认识:

- Web 应用天然是多线程环境
- 不要在共享对象里随意保存请求级数据

## 9. 学习输出建议

完成本章后，你至少应能独立实现:

- 控制台 CRUD 程序
- 文件读写程序
- 使用集合保存数据
- 使用异常处理输入错误
- 用类和对象对业务建模
