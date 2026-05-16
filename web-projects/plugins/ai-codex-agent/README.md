# AI Codex Agent

示例 WordPress 插件，用于演示如何在后台调用 OpenAI（ChatGPT/Codex）生成内容并通过 REST 接口提供服务。

安装与使用

1. 将本插件目录 `ai-codex-agent` 上传到服务器的 `wp-content/plugins/` 下。
2. 在 `wp-config.php` 中配置 OpenAI Key（推荐）：

```php
define('OPENAI_API_KEY', getenv('OPENAI_API_KEY'));
```

3. 在服务器上通过 WP-CLI 激活：

```bash
cd /path/to/wordpress
wp plugin activate ai-codex-agent
```

4. 在 WordPress 后台左侧菜单找到 `AI Codex`，在页面内输入 prompt 并生成内容。

REST API

- POST `/wp-json/ai-codex/v1/generate` （需要已登录并具备 `edit_posts` 权限）
- 请求体示例：

```json
{ "prompt": "请生成一段关于 Docker Compose 的 200 字中文简介。" }
```

安全与生产注意

- 不要将 API Key 提交到代码仓库，使用服务器环境变量或 Secret 管理。
- 在生产环境中建议先在 staging 测试，并为生成内容设置自动草稿与审核流程。
- 使用缓存（transient）与速率限制以控制成本。

许可证

示例代码仅供学习与参考，请按照你所在组织的合规策略使用与修改。
