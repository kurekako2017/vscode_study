# gk-fuji.co.jp 跳转到 gk-fuji.jp 教程

## 适用场景

本文适用于以下场景：

- 服务器是 `onamae.com` 的 RSプラン 共享主机
- `gk-fuji.jp` 已经是正式网站，WordPress 正常运行
- `gk-fuji.co.jp` 只是注册完成，并且已经指向同一台服务器
- 域名商是 `onamae.com`（お名前.com）
- 目标是把 `gk-fuji.co.jp` 统一跳转到 `gk-fuji.jp`
- 未来还要考虑 `gk-fuji.jp` 可能废止，最终改由 `gk-fuji.co.jp` 作为主域名

## 先确认你要哪种结果

这个问题有两种完全不同的目标：

1. 输入 `gk-fuji.co.jp` 后，地址栏变成 `gk-fuji.jp`（域名跳转）
2. 输入 `gk-fuji.co.jp` 后，地址栏仍然显示 `gk-fuji.co.jp`（主域名切换）

如果你想要“地址栏保持 `.co.jp`”，就不能继续使用“`.co.jp` 跳转到 `.jp`”的方案，而是要把 `.co.jp` 设为 WordPress 主域名。

## 先给结论

如果你要的是“`.co.jp` 输入后直接显示网站，并且地址栏保持 `.co.jp`”，最适合的做法是：

1. 取消 `gk-fuji.co.jp -> gk-fuji.jp` 的域名转发
2. 把 `gk-fuji.co.jp` 绑定到当前 WordPress 同一目录
3. 把 WordPress 主域名改为 `https://gk-fuji.co.jp`
4. 再把 `gk-fuji.jp` 反向 `301` 到 `https://gk-fuji.co.jp`

如果你要的是“`.co.jp` 自动跳到 `.jp`”，才使用方案二：

1. 直接在 `onamae.com` 后台给 `gk-fuji.co.jp` 配置域名转发
2. 让 `gk-fuji.co.jp` 以 `301` 永久跳转到 `https://gk-fuji.jp`
3. `gk-fuji.jp` 继续作为 WordPress 的唯一主域名
4. `gk-fuji.co.jp` 不需要自己创建 WordPress 网站目录
5. 所有内链、站点地图、搜索引擎收录都以 `gk-fuji.jp` 为准

这样做的好处是：

- 不需要改服务器文件
- 不需要创建 `gk-fuji.co.jp` 的网站目录
- 配置最简单
- 适合现在只有域名、还没给这个域名单独建站的情况

---

## 方案对比

| 方案 | 适合度 | 优点 | 缺点 |
|------|--------|------|------|
| 新方案：`.co.jp` 作为主域名，`.jp` 反向跳转 | 最推荐（你的当前目标） | 地址栏始终显示 `.co.jp`，品牌统一 | 需要一次 WordPress 主域名切换 |
| 注册商转发（`.co.jp -> .jp`） | 仅适合“我要跳到 `.jp`” | 配置简单，不用改站点 | 地址栏会显示 `.jp`，不符合你当前目标 |
| 服务器层 301 跳转（`.co.jp -> .jp`） | 备选 | 控制力强，适合精细配置 | 仍然会显示 `.jp` |
| WordPress 插件跳转 | 可用但不优先 | 后台可操作 | 依赖 WordPress 正常加载，性能和控制力一般 |

如果你现在的目标是“地址栏显示 `.co.jp`”，直接走新方案，不要再把 `.co.jp` 转发到 `.jp`。

---

## 新方案：`.co.jp` 直接显示网站（推荐）

### 适用目标

- 输入 `https://gk-fuji.co.jp/` 后，地址栏保持 `.co.jp`
- 网站内容和当前 `gk-fuji.jp` 一样（同一套 WordPress）
- `gk-fuji.jp` 后续作为旧域名，只做反向跳转

### 实施步骤

1. 在 onamae.com 里关闭 `gk-fuji.co.jp -> gk-fuji.jp` 的转发设置
2. 在 RSプラン 里确认 `gk-fuji.co.jp` 和 `gk-fuji.jp` 都绑定到同一套 WordPress 目录
3. 确认 `https://gk-fuji.co.jp` 证书正常（避免 HTTPS 警告）
4. 进入 WordPress 后台，将“WordPress 地址”和“站点地址”都改成 `https://gk-fuji.co.jp`
5. 用搜索替换工具把内容中的绝对链接由 `.jp` 替换为 `.co.jp`
6. 给 `gk-fuji.jp` 加反向 301 规则，统一跳到 `.co.jp`
7. 清缓存（WordPress 缓存/CDN/浏览器）
8. 验证首页、内页、图片、脚本、样式都正常

### `gk-fuji.jp -> gk-fuji.co.jp` 反向 301 示例

```apache
RewriteEngine On

RewriteCond %{HTTP_HOST} ^(www\.)?gk-fuji\.jp$ [NC]
RewriteRule ^(.*)$ https://gk-fuji.co.jp/$1 [R=301,L]
```

### 验证标准

- 访问 `https://gk-fuji.co.jp/`：页面正常，地址栏保持 `.co.jp`
- 访问 `https://gk-fuji.jp/`：自动 `301` 到 `.co.jp`
- 任意内页与参数链接也保持正确跳转
- 搜索引擎提交的 sitemap 使用 `.co.jp`

---

## 方案一：在服务器上做 301 跳转

这是最推荐的方案。因为 `gk-fuji.co.jp` 已经解析到同一台服务器，所以只要在 RSプラン 里用 `.htaccess` 识别这个域名并返回 301 即可。

RSプラン 这类共享主机通常更适合用 Apache + `.htaccess` 来做跳转，而不是直接改 nginx 主配置。

### 0. RSプラン 里的实际配置位置

在 onamae.com 的 RSプラン 中，通常做法不是去改整台服务器的全局配置，而是：

1. 登录 onamae.com 后台
2. 打开 RSプラン 对应的服务器管理页面
3. 找到 `gk-fuji.co.jp` 对应的网站目录
4. 在 `gk-fuji.co.jp` 对应的站点根目录下编辑或新增 `.htaccess`
5. 让 `gk-fuji.co.jp` 命中跳转规则后直接返回 `301`

如果 `gk-fuji.jp` 是 WordPress，`.htaccess` 一般就在 WordPress 安装目录里，也就是 `wp-config.php`、`wp-content`、`wp-includes` 同级的那个目录。`gk-fuji.co.jp` 这边则要看它在 RSプラン 中是否已经分配了自己的站点目录；如果没有，就先在控制面板里把这个域名绑定到一个目录，再往那个目录里放 `.htaccess`。

如果你采用的是方案二，也就是 `onamae.com` 域名转发，那么 `gk-fuji.co.jp` 不需要独立站点目录，也不需要自己放 `.htaccess`。这种情况下，转发规则直接在注册商后台完成。

### 0.2 推荐的实际操作路径

如果你要自己动手，推荐按这个顺序做。下面写的是更接近 RSプラン 实际操作的版本：

1. 登录 onamae.com
2. 进入 RSプラン 的服务器管理页面
3. 确认 `gk-fuji.jp` 已经是 WordPress 正式站点
4. 确认 `gk-fuji.co.jp` 已经绑定到同一台服务器，且可以访问或至少有对应的站点目录
5. 如果后台有“文件管理”入口，先打开文件管理；如果没有，直接准备 FTP 信息
6. 找到 `gk-fuji.co.jp` 对应的目录，或者 WordPress 当前使用的根目录
7. 检查目录里是否已经有 `.htaccess`
8. 如果没有，就新建一个名为 `.htaccess` 的纯文本文件
9. 如果已经有，就先备份原文件内容，再编辑
10. 在 WordPress 原有规则前后加入跳转规则
11. 保存后刷新站点，确认 `gk-fuji.co.jp` 会直接跳转到 `gk-fuji.jp`
12. 再用带路径和参数的 URL 做一次测试，确认没有丢路径

如果你不确定 WordPress 原有的 `.htaccess` 内容，不要直接删除旧内容，只在前面或后面追加跳转规则。先备份，再改文件，这是 RSプラン 上最稳的做法。

### 0.1 如果找不到站点根目录

如果你在后台看不到明确的目录信息，可以按这几个判断：

- 站点访问后能打开 WordPress 首页，说明你已经进入了正确的网站目录
- 目录里存在 WordPress 核心文件，说明这里就是可编辑的站点根目录
- 后台提供文件管理或 FTP 信息时，优先通过 FTP 进入该目录再改 `.htaccess`

如果 RSプラン 后台界面限制较多，最稳妥的方式通常是用 FTP 连接后直接修改 `.htaccess`。

### 0.3 怎么验证跳转是否正确

你可以用浏览器或命令行检查结果：

- 在浏览器地址栏输入 `http://gk-fuji.co.jp`
- 看是否自动变成 `https://gk-fuji.jp`
- 检查地址栏是否保留路径，例如 `/about/`
- 检查浏览器开发者工具里的状态码是否为 `301`

如果你有命令行环境，也可以用 `curl -I https://gk-fuji.co.jp` 看返回头里是否出现 `301 Moved Permanently` 和 `Location: https://gk-fuji.jp/...`

### 1. Apache / .htaccess 写法

如果站点是 Apache 或兼容 `.htaccess` 的环境，可以在 `gk-fuji.co.jp` 对应站点的根目录里加入：

```apache
RewriteEngine On

RewriteCond %{HTTP_HOST} ^(www\.)?gk-fuji\.co\.jp$ [NC]
RewriteRule ^(.*)$ https://gk-fuji.jp/$1 [R=301,L]
```

说明：

- 会把 `http://gk-fuji.co.jp/xxx` 跳转到 `https://gk-fuji.jp/xxx`
- 会把 `www.gk-fuji.co.jp` 也一并处理
- `301` 表示永久跳转，适合正式迁移

### 2. nginx 写法

如果是 nginx，建议单独给 `gk-fuji.co.jp` 建一个 server block：

```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name gk-fuji.co.jp www.gk-fuji.co.jp;

    return 301 https://gk-fuji.jp$request_uri;
}
```

如果你的网站启用了 HTTPS，`gk-fuji.co.jp` 也要有可用证书，否则用户在跳转前会先看到证书警告。

### 3. WordPress 场景下的注意点

如果 `gk-fuji.jp` 本身是 WordPress：

- WordPress 的 `Site Address (URL)` 和 `WordPress Address (URL)` 继续保持 `https://gk-fuji.jp`
- `gk-fuji.co.jp` 不要作为 WordPress 主站地址
- 跳转必须发生在 WordPress 之前，否则会多一次 PHP 处理

也就是说，`gk-fuji.co.jp` 最好在 Web 服务器层直接返回 301，不要让 WordPress 页面先加载出来再跳。

---

## 方案二：使用 onamae.com 的域名转发

如果你希望采用最省事的方式，这就是主方案。`gk-fuji.co.jp` 只是注册域名，没有单独建站时，直接在 onamae.com 后台做转发最合适。

> 重要：你截图里的 `WWW転送設定`（wwwあり / wwwなし / 転送しない）只用于同一域名内的 `www` 归一化，不是“跳到另一个域名”的 URL 转发。
> 这个弹窗里没有目标地址输入框是正常现象。

### 配置思路

1. 登录 `onamae.com` 后台
2. 找到 `gk-fuji.co.jp`
3. 查找“URL 转发 / URL転送 / 转送先URL”类型的功能入口（不是 `WWW転送設定`）
4. 目标地址填写：`https://gk-fuji.jp`
5. 选择永久转发，优先使用 `301`
6. 保存后测试跳转是否生效

### 如果没有“目标地址”输入框

如果你只能看到 `WWW転送設定` 这个弹窗，说明当前入口仅支持 `www` 与非 `www` 的同域名跳转，不支持 `gk-fuji.co.jp -> gk-fuji.jp`。

此时有两个可行方案：

1. 在 onamae.com 里继续找真正的 `URL転送` 功能入口（如果你的套餐或域名管理页面提供）
2. 如果没有该功能，就改用方案一（服务器侧 301），在 RSプラン 的 `.htaccess` 上做域名跳转

也就是说：

- `WWW転送設定` 能做：`www.gk-fuji.co.jp -> gk-fuji.co.jp`
- `WWW転送設定` 不能做：`gk-fuji.co.jp -> gk-fuji.jp`

### 需要确认的点

- 是否支持保留原始路径，例如：`/company/` 是否能跳到 `https://gk-fuji.jp/company/`
- 是否支持查询参数，例如 `?utm_source=...`
- 是否支持 HTTPS
- 是否返回真正的 `301`，而不是框架跳转或 `302`

### 这个方案的风险

- 有些注册商转发对路径和参数的支持不完整
- 证书和 HTTPS 支持要在后台确认
- 如果你未来需要更复杂规则，可能还要换成服务器层跳转

所以这适合当前“只做域名跳转”的场景；如果以后要做更复杂的规则，再升级方案。

---

## 方案三：用 WordPress 插件做跳转

如果你只想在 WordPress 后台操作，可以用跳转插件做 301。

### 适合情况

- 你能登录 WordPress 后台
- 服务器权限有限
- 想先快速上线

### 缺点

- 访问请求要先进入 WordPress，再决定跳转
- 性能和稳定性不如服务器层
- 如果 WordPress 出问题，跳转也会失效

### 建议

WordPress 插件跳转只适合补救，不建议作为正式长期方案。

---

## 推荐实施步骤

### 阶段 1：先把跳转做好

1. 确认 `gk-fuji.co.jp` 和 `gk-fuji.jp` 都已解析到同一台服务器
2. 给两个域名都准备好 HTTPS 证书
3. 让 `gk-fuji.co.jp` 返回 `301` 到 `https://gk-fuji.jp`
4. 确认 `www.gk-fuji.co.jp` 也一起跳转
5. 测试首页、内页、带参数链接是否都能正确保留

### 阶段 2：统一 WordPress 主域名

1. 检查 WordPress 的站点地址是否为 `https://gk-fuji.jp`
2. 更新站内绝对链接
3. 更新菜单、页脚、图标、开放图数据里的域名
4. 重新生成 sitemap
5. 到搜索引擎后台提交新站点地图

### 阶段 3：观察和验证

- 用浏览器访问 `http://gk-fuji.co.jp`
- 用浏览器访问 `https://gk-fuji.co.jp`
- 用浏览器访问 `https://gk-fuji.co.jp/some-page?x=1`
- 确认都跳到 `gk-fuji.jp`，且路径和参数没有丢失

---

## SEO 和收录建议

如果 `gk-fuji.co.jp` 只是别名域名，那么建议它一直只做跳转，不要同时承载独立内容。

要点如下：

- 只保留一个主域名，避免重复内容
- 所有 canonical 统一指向 `gk-fuji.jp`
- sitemap 只提交 `gk-fuji.jp`
- 外部宣传、名片、SNS 链接都尽量写主域名
- 不要使用 `302`，正式迁移尽量用 `301`

如果未来要切换主域名，搜索引擎会更容易理解站点迁移关系。

---

## 未来如果要废止 gk-fuji.jp，怎么做

这是你现在就应该提前规划的部分。

### 推荐的未来目标

未来如果决定废止 `gk-fuji.jp`，通常应当让：

- `gk-fuji.co.jp` 变成新主域名
- `gk-fuji.jp` 继续保留一段时间，专门做 `301` 跳转到 `gk-fuji.co.jp`

也就是说，域名角色反过来：

- 现在：`gk-fuji.co.jp` → `gk-fuji.jp`
- 未来：`gk-fuji.jp` → `gk-fuji.co.jp`

### 迁移步骤

1. 先把 `gk-fuji.co.jp` 完整切成主站
2. 确认 WordPress 站点地址切到 `https://gk-fuji.co.jp`
3. 全站内链、图片、规范链接统一到 `.co.jp`
4. `gk-fuji.jp` 仅做 301 跳转
5. 保持跳转至少 6 到 12 个月
6. 等搜索引擎、外部链接、邮件签名、印刷物都更新完，再考虑是否续费 `gk-fuji.jp`

### 废止前不要做的事

- 不要立刻注销旧域名
- 不要立刻删除旧域名 DNS
- 不要立刻关闭旧域名 SSL
- 不要把旧域名直接改成 404

原因很简单：

- 外部旧链接还会继续访问
- 搜索引擎需要时间重新识别
- 用户收藏夹和历史邮件里的链接仍然存在

### 废止时的最稳做法

如果你最终真的要废止 `gk-fuji.jp`，建议顺序是：

1. 先把站点完全迁移到 `gk-fuji.co.jp`
2. 确认 301 跳转稳定运行
3. 观察一段时间的访问日志和搜索收录
4. 再决定是否停用 `gk-fuji.jp`

通常在企业网站场景里，旧域名最好继续保留很长时间，只做跳转，不要过早放弃。

---

## 最终推荐方案

如果按稳定性和后续可维护性排序，建议这样做：

1. 现在：`gk-fuji.co.jp` 通过服务器层 `301` 跳转到 `gk-fuji.jp`
2. `gk-fuji.jp` 继续作为 WordPress 正式站点
3. 未来若要废止 `.jp`：先把主站切到 `.co.jp`，再让 `.jp` 做 `301`
4. 两次切换都尽量保留旧域名至少 6 到 12 个月

这样最不容易出 SEO 问题，也最方便以后再做域名策略调整。
