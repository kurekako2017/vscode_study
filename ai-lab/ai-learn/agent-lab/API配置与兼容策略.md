# API 配置与兼容策略

这份说明是给 `agent-lab` 里所有示例准备的统一入口。

当前结论很简单：

- 如果继续用 **OpenAI 官方接口**，很多示例只需要设置 `OPENAI_API_KEY`
- 如果要切换到 **DeepSeek / OpenRouter / 其他 OpenAI 兼容服务**，仅改环境变量还不够，代码最好也做一次统一抽象
- 如果希望“同一套代码，多家 API 都能跑”，建议后续统一到一套配置层，再由代码读取这些配置

## 现在的代码现状

`agent-lab` 里目前的大多数示例，都是直接读取：

```bash
OPENAI_API_KEY
```

然后创建 OpenAI client。也就是说，它们的默认形态是“OpenAI 官方接口优先”。

这套方式的优点是：

- 简单
- 直观
- 学习门槛低

缺点是：

- 不适合频繁切换供应商
- 代码里容易写死 provider 逻辑
- 后期如果改成 DeepSeek / OpenRouter，需要逐个例子处理

## 什么时候只改环境变量就够了

只改环境变量，通常适用于下面这种情况：

1. 你仍然在调用 OpenAI 官方接口
2. 代码里已经支持从环境变量读取 API Key
3. 代码没有写死 provider 专属的 `base_url`

这种情况下，通常只需要设置：

```bash
export OPENAI_API_KEY="your-api-key"
```

就能跑。

## 什么时候需要改代码

如果你要切到这些服务，通常需要改代码或做统一封装：

- DeepSeek
- OpenRouter
- 其他 OpenAI 兼容服务

原因是这些服务不只要 Key，往往还需要：

- `base_url`
- `model`
- 有时还要 provider-specific 的兼容设置

如果代码里没有统一读取这些配置，那就会出现：

- 某些 demo 能跑
- 某些 demo 不能跑
- 每个 demo 的启动方式不一致

这会让学习体验变差。

## 推荐的统一方向

为了以后维护方便，建议后续把配置统一成这一套逻辑：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`
- `LLM_PROVIDER`

然后在代码里提供一个统一的 client 构建函数，优先读取这套变量，再兼容旧的 `OPENAI_API_KEY`。

这样以后切换服务时，通常只改 `.env`，业务代码不用跟着改。

## 推荐策略

### 方案 A：保持现状

适合：

- 想先把教程跑通
- 暂时只用 OpenAI 官方接口

特点：

- 不改代码
- 直接设置 `OPENAI_API_KEY`
- 最省事

### 方案 B：逐个 demo 改

适合：

- 只想先改少数重点示例

特点：

- 改动小
- 但后续维护成本会慢慢变高

### 方案 C：统一抽象配置层

适合：

- 想让 `agent-lab` 变成长期可维护的学习仓库
- 想在 DeepSeek / OpenRouter / OpenAI 间自由切换

特点：

- 前期要做一次统一整理
- 后面所有 demo 都能复用
- 最适合“同一套代码、多种 API”目标

## 建议的执行顺序

1. 先把当前 demo 继续按 `OPENAI_API_KEY` 跑通
2. 再挑最常用的几个 demo 做统一配置层
3. 最后把剩余 demo 逐步迁移到统一模式

## 这份文档的用途

以后如果你再问：

- 这个 demo 为什么只能读 `OPENAI_API_KEY`
- 怎么切到 DeepSeek
- 怎么让同一套代码兼容 OpenRouter
- 哪些地方需要改代码，哪些地方只要改环境变量

就先看这份文档，再决定下一步怎么统一改造。
