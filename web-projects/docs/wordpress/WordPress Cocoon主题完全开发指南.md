# WordPress Cocoon主题完全开发指南

> **目标**: 使用免费Cocoon主题快速搭建日本企业网站  
> **开发时间**: 1-2天  
> **成本**: ¥0（完全免费）  
> **特点**: 日本制作、SEO优化、高速、响应式

---

## 📋 目录

1. [Cocoon主题介绍](#cocoon主题介绍)
2. [快速安装配置](#快速安装配置)
3. [企业网站页面模板](#企业网站页面模板)
4. [功能模块配置](#功能模块配置)
5. [自定义设计](#自定义设计)
6. [实战案例](#实战案例)

---

## 🎯 Cocoon主题介绍

### 为什么选择Cocoon？

```
✅ 完全免费（日本制作）
✅ 日语完美支持
✅ SEO内置优化
✅ 高速加载（PageSpeed Score 90+）
✅ 响应式设计
✅ 不需要编程知识
✅ 更新频繁（安全可靠）
✅ 大量自定义选项
```

### Cocoon vs 其他主题对比

| 特性 | Cocoon | Lightning | Elementor Pro |
|------|---------|-----------|---------------|
| **价格** | 免费 | 免费 | $59/年 |
| **日语优化** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **SEO功能** | 内置 | 需要插件 | 需要插件 |
| **速度** | 最快 | 快 | 中 |
| **自定义性** | 高 | 中 | 最高 |
| **学习曲线** | 易 | 易 | 中 |

---

## 🚀 快速安装配置（30分钟）

### Step 1: 安装Cocoon主题（5分钟）

```bash
# 方法1: WordPress管理画面安装
外观 → 主题 → 新规追加
搜索: "Cocoon"
インストール → 有効化

# 方法2: 官方网站下载（推荐）
访问: https://wp-cocoon.com/
下载: Cocoon主题 + Cocoon Child主题（子主题）

WordPress管理画面:
外观 → 主题 → 新规追加 → テーマのアップロード
上传 cocoon-master.zip → インストール
上传 cocoon-child-master.zip → インストール → 有効化
```

**重要**: 必须启用**子主题**（Cocoon Child），不要直接启用父主题！

### Step 2: 基本设置（10分钟）

#### 2-1: Cocoon设置 - 全体设置

```
Cocoon设定 → 全体

【サイトキーカラー】
キーカラー: #0066cc (企业主色)
サイトキーカラーの透過度: 0.9

【サイトフォント】
サイト全体のフォント: 游ゴシック体
font-size: 16px

【サイト幅の調整】
サイト幅: 1200px
モバイル: 100%

保存
```

#### 2-2: Cocoon设置 - ヘッダー

```
Cocoon设定 → ヘッダー

【ヘッダーレイアウト】
選択: センターロゴ（中央Logo配置）

【ヘッダー背景色】
背景色: #ffffff（白色）

【ヘッダーロゴ】
ロゴ画像: [上传公司Logo]
ロゴサイズ: 高さ60px

【ヘッダーメニュー】
メニュー配置: グローバルナビ表示
メニュー背景色: #003366（深蓝色）
メニュー文字色: #ffffff（白色）

保存
```

#### 2-3: Cocoon设置 - 固定页面设置

```
Cocoon设定 → 投稿 → 固定ページ設定

【関連記事の表示】
固定ページに関連記事を表示する: OFF（企业网站不需要）

【パンくずリストの表示】
固定ページにパンくずリストを表示する: ON

【更新日の表示】
固定ページに更新日を表示する: OFF

保存
```

### Step 3: 推荐插件安装（10分钟）

```
必须插件:
1. Contact Form 7 - 联系表单
2. WP Mail SMTP - 邮件发送
3. SiteGuard WP Plugin - 安全防护

推荐插件:
4. EWWW Image Optimizer - 图片优化
5. UpdraftPlus - 自动备份
6. Google XML Sitemaps - 站点地图
```

### Step 4: 菜单设置（5分钟）

```
外观 → メニュー → 新规作成

菜单名: グローバルナビ

添加页面:
□ ホーム（首页）
□ 会社概要（公司简介）
□ 事業内容（业务内容）
□ ニュース（新闻）
□ 採用情報（招聘信息）
□ お問い合わせ（联系我们）

菜单位置: ヘッダーメニュー
保存
```

---

## 📄 企业网站页面模板

### 模板1: 首页（トップページ）

#### 使用方法
```
固定ページ → 新规追加
标题: ホーム
页面模板: 选择"トップページ（Cocoon）"
```

#### 完整HTML代码（可直接复制使用）

```html
<!-- メインビジュアル -->
<div class="hero-section" style="background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; padding: 100px 20px; text-align: center;">
    <h1 style="font-size: 48px; margin-bottom: 20px; font-weight: bold;">
        お客様のビジネスを<br>次のステージへ
    </h1>
    <p style="font-size: 20px; margin-bottom: 40px;">
        革新的なソリューションで企業の成長を支援します
    </p>
    <a href="/contact" class="btn-primary" style="display: inline-block; background: white; color: #003366; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 18px;">
        お問い合わせはこちら →
    </a>
</div>

<!-- 会社の強み（3カラム） -->
<section style="padding: 80px 20px; background: #f8f9fa;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 50px; color: #003366;">
            私たちの強み
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <!-- 強み1 -->
            <div style="background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="width: 80px; height: 80px; background: #0066cc; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 40px; color: white;">💡</span>
                </div>
                <h3 style="font-size: 24px; margin-bottom: 15px; color: #003366;">革新的な技術</h3>
                <p style="color: #666; line-height: 1.8;">
                    最新のテクノロジーを活用し、お客様のビジネス課題を解決します。
                </p>
            </div>
            
            <!-- 強み2 -->
            <div style="background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="width: 80px; height: 80px; background: #0066cc; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 40px; color: white;">🤝</span>
                </div>
                <h3 style="font-size: 24px; margin-bottom: 15px; color: #003366;">信頼の実績</h3>
                <p style="color: #666; line-height: 1.8;">
                    創業以来、多くの企業様にご支持いただいております。
                </p>
            </div>
            
            <!-- 強み3 -->
            <div style="background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                <div style="width: 80px; height: 80px; background: #0066cc; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 40px; color: white;">⚡</span>
                </div>
                <h3 style="font-size: 24px; margin-bottom: 15px; color: #003366;">スピード対応</h3>
                <p style="color: #666; line-height: 1.8;">
                    お客様のご要望に迅速かつ柔軟に対応いたします。
                </p>
            </div>
        </div>
    </div>
</section>

<!-- 最新ニュース -->
<section style="padding: 80px 20px; background: white;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 50px; color: #003366;">
            最新ニュース
        </h2>
        
        <!-- Cocoonショートコード: 最新記事3件表示 -->
        [new_list count="3" type="border_partition" children="0"]
        
        <div style="text-align: center; margin-top: 40px;">
            <a href="/news" style="display: inline-block; color: #0066cc; font-weight: bold; text-decoration: none; border-bottom: 2px solid #0066cc; padding-bottom: 5px;">
                ニュース一覧を見る →
            </a>
        </div>
    </div>
</section>

<!-- 会社概要（簡易版） -->
<section style="padding: 80px 20px; background: #f8f9fa;">
    <div class="container" style="max-width: 1200px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 50px; color: #003366;">
            会社概要
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center;">
            <div>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #ddd;">
                        <th style="padding: 15px; text-align: left; width: 30%; background: #f0f0f0;">会社名</th>
                        <td style="padding: 15px;">株式会社サンプル</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <th style="padding: 15px; text-align: left; background: #f0f0f0;">設立</th>
                        <td style="padding: 15px;">2020年4月1日</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <th style="padding: 15px; text-align: left; background: #f0f0f0;">所在地</th>
                        <td style="padding: 15px;">東京都渋谷区〇〇</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #ddd;">
                        <th style="padding: 15px; text-align: left; background: #f0f0f0;">代表者</th>
                        <td style="padding: 15px;">代表取締役 山田太郎</td>
                    </tr>
                </table>
                
                <div style="margin-top: 30px;">
                    <a href="/about" style="display: inline-block; background: #0066cc; color: white; padding: 15px 30px; border-radius: 5px; text-decoration: none; font-weight: bold;">
                        詳しく見る →
                    </a>
                </div>
            </div>
            
            <div>
                <img src="https://via.placeholder.com/600x400/0066cc/ffffff?text=Company+Image" alt="会社画像" style="width: 100%; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            </div>
        </div>
    </div>
</section>

<!-- CTA（お問い合わせ誘導） -->
<section style="padding: 80px 20px; background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; text-align: center;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
        <h2 style="font-size: 36px; margin-bottom: 20px;">
            お気軽にお問い合わせください
        </h2>
        <p style="font-size: 18px; margin-bottom: 40px; line-height: 1.8;">
            ご相談・お見積もりは無料です。<br>
            専門スタッフが丁寧に対応いたします。
        </p>
        
        <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <a href="/contact" style="display: inline-block; background: white; color: #003366; padding: 15px 40px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 18px;">
                📧 お問い合わせフォーム
            </a>
            <a href="tel:03-1234-5678" style="display: inline-block; background: transparent; color: white; padding: 15px 40px; border: 2px solid white; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 18px;">
                📞 03-1234-5678
            </a>
        </div>
    </div>
</section>

<!-- 自定义CSS（添加到カスタマイズ → 追加CSS） -->
<style>
/* レスポンシブ対応 */
@media (max-width: 768px) {
    .hero-section h1 {
        font-size: 32px !important;
    }
    .hero-section p {
        font-size: 16px !important;
    }
    section h2 {
        font-size: 28px !important;
    }
    div[style*="grid-template-columns"] {
        grid-template-columns: 1fr !important;
    }
}

/* ボタンホバー効果 */
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
</style>
```

---

### 模板2: 公司简介页面（会社概要）

```html
<!-- ページヘッダー -->
<div style="background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; padding: 60px 20px; text-align: center;">
    <h1 style="font-size: 42px; margin-bottom: 10px;">会社概要</h1>
    <p style="font-size: 18px;">Company Profile</p>
</div>

<!-- 代表挨拶 -->
<section style="padding: 80px 20px; background: white;">
    <div class="container" style="max-width: 1000px; margin: 0 auto;">
        <h2 style="font-size: 32px; margin-bottom: 40px; color: #003366; border-left: 5px solid #0066cc; padding-left: 20px;">
            代表挨拶
        </h2>
        
        <div style="display: grid; grid-template-columns: 200px 1fr; gap: 40px; align-items: start;">
            <div>
                <img src="https://via.placeholder.com/200x250/0066cc/ffffff?text=CEO" alt="代表取締役" style="width: 100%; border-radius: 10px;">
                <p style="text-align: center; margin-top: 10px; font-weight: bold;">代表取締役<br>山田太郎</p>
            </div>
            
            <div>
                <p style="line-height: 2; color: #333; margin-bottom: 20px;">
                    この度は、弊社のウェブサイトをご覧いただき、誠にありがとうございます。
                </p>
                <p style="line-height: 2; color: #333; margin-bottom: 20px;">
                    当社は20XX年の創業以来、お客様のビジネス成長を支援することを使命とし、
                    革新的なソリューションを提供してまいりました。
                </p>
                <p style="line-height: 2; color: #333; margin-bottom: 20px;">
                    これからも、お客様の期待を超えるサービスを提供し続けることで、
                    社会に貢献してまいります。
                </p>
                <p style="line-height: 2; color: #333;">
                    今後とも、変わらぬご支援を賜りますよう、よろしくお願い申し上げます。
                </p>
            </div>
        </div>
    </div>
</section>

<!-- 会社情報 -->
<section style="padding: 80px 20px; background: #f8f9fa;">
    <div class="container" style="max-width: 1000px; margin: 0 auto;">
        <h2 style="font-size: 32px; margin-bottom: 40px; color: #003366; border-left: 5px solid #0066cc; padding-left: 20px;">
            会社情報
        </h2>
        
        <table style="width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; width: 25%; background: #f0f0f0; font-weight: bold;">会社名</th>
                <td style="padding: 20px;">株式会社サンプル</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">英文社名</th>
                <td style="padding: 20px;">Sample Corporation</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">設立</th>
                <td style="padding: 20px;">2020年4月1日</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">資本金</th>
                <td style="padding: 20px;">1,000万円</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">代表者</th>
                <td style="padding: 20px;">代表取締役社長 山田太郎</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">従業員数</th>
                <td style="padding: 20px;">50名（2025年12月現在）</td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">事業内容</th>
                <td style="padding: 20px;">
                    ・ITコンサルティング<br>
                    ・システム開発<br>
                    ・Webサイト制作<br>
                    ・クラウドソリューション
                </td>
            </tr>
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">本社所在地</th>
                <td style="padding: 20px;">
                    〒150-0001<br>
                    東京都渋谷区神宮前1-2-3 サンプルビル5F<br>
                    TEL: 03-1234-5678<br>
                    FAX: 03-1234-5679
                </td>
            </tr>
            <tr>
                <th style="padding: 20px; text-align: left; background: #f0f0f0; font-weight: bold;">取引銀行</th>
                <td style="padding: 20px;">
                    三菱UFJ銀行 渋谷支店<br>
                    みずほ銀行 原宿支店
                </td>
            </tr>
        </table>
    </div>
</section>

<!-- アクセスマップ -->
<section style="padding: 80px 20px; background: white;">
    <div class="container" style="max-width: 1000px; margin: 0 auto;">
        <h2 style="font-size: 32px; margin-bottom: 40px; color: #003366; border-left: 5px solid #0066cc; padding-left: 20px;">
            アクセス
        </h2>
        
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 20px; margin-bottom: 15px; color: #003366;">🚇 電車でお越しの場合</h3>
            <ul style="line-height: 2; color: #666; padding-left: 20px;">
                <li>JR山手線「原宿駅」徒歩5分</li>
                <li>東京メトロ千代田線・副都心線「明治神宮前駅」徒歩3分</li>
            </ul>
        </div>
        
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 20px; margin-bottom: 15px; color: #003366;">🚗 お車でお越しの場合</h3>
            <p style="line-height: 2; color: #666;">
                ※駐車場はございません。お近くのコインパーキングをご利用ください。
            </p>
        </div>
        
        <!-- Google Map埋め込み -->
        <div style="border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3241.0273588794387!2d139.7024!3d35.6702!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzXCsDQwJzEyLjciTiAxMznCsDQyJzA4LjYiRQ!5e0!3m2!1sja!2sjp!4v1234567890" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        </div>
    </div>
</section>

<!-- 沿革 -->
<section style="padding: 80px 20px; background: #f8f9fa;">
    <div class="container" style="max-width: 1000px; margin: 0 auto;">
        <h2 style="font-size: 32px; margin-bottom: 40px; color: #003366; border-left: 5px solid #0066cc; padding-left: 20px;">
            沿革
        </h2>
        
        <div style="position: relative; padding-left: 40px;">
            <!-- タイムライン線 -->
            <div style="position: absolute; left: 10px; top: 10px; bottom: 10px; width: 2px; background: #0066cc;"></div>
            
            <!-- 2020年 -->
            <div style="position: relative; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="position: absolute; left: -34px; top: 20px; width: 12px; height: 12px; background: #0066cc; border-radius: 50%; border: 3px solid white;"></div>
                <h3 style="font-size: 18px; color: #0066cc; margin-bottom: 10px; font-weight: bold;">2020年4月</h3>
                <p style="color: #666; line-height: 1.8;">株式会社サンプル設立</p>
            </div>
            
            <!-- 2021年 -->
            <div style="position: relative; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="position: absolute; left: -34px; top: 20px; width: 12px; height: 12px; background: #0066cc; border-radius: 50%; border: 3px solid white;"></div>
                <h3 style="font-size: 18px; color: #0066cc; margin-bottom: 10px; font-weight: bold;">2021年7月</h3>
                <p style="color: #666; line-height: 1.8;">東京本社を渋谷区に移転</p>
            </div>
            
            <!-- 2022年 -->
            <div style="position: relative; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="position: absolute; left: -34px; top: 20px; width: 12px; height: 12px; background: #0066cc; border-radius: 50%; border: 3px solid white;"></div>
                <h3 style="font-size: 18px; color: #0066cc; margin-bottom: 10px; font-weight: bold;">2022年3月</h3>
                <p style="color: #666; line-height: 1.8;">資本金1,000万円に増資</p>
            </div>
            
            <!-- 2023年 -->
            <div style="position: relative; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="position: absolute; left: -34px; top: 20px; width: 12px; height: 12px; background: #0066cc; border-radius: 50%; border: 3px solid white;"></div>
                <h3 style="font-size: 18px; color: #0066cc; margin-bottom: 10px; font-weight: bold;">2023年10月</h3>
                <p style="color: #666; line-height: 1.8;">大阪支社開設</p>
            </div>
            
            <!-- 2024年 -->
            <div style="position: relative; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="position: absolute; left: -34px; top: 20px; width: 12px; height: 12px; background: #0066cc; border-radius: 50%; border: 3px solid white;"></div>
                <h3 style="font-size: 18px; color: #0066cc; margin-bottom: 10px; font-weight: bold;">2024年6月</h3>
                <p style="color: #666; line-height: 1.8;">従業員数50名突破</p>
            </div>
        </div>
    </div>
</section>
```

---

### 模板3: 联系表单页面（お問い合わせ）

```html
<!-- ページヘッダー -->
<div style="background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: white; padding: 60px 20px; text-align: center;">
    <h1 style="font-size: 42px; margin-bottom: 10px;">お問い合わせ</h1>
    <p style="font-size: 18px;">Contact Us</p>
</div>

<!-- お問い合わせフォーム -->
<section style="padding: 80px 20px; background: white;">
    <div class="container" style="max-width: 800px; margin: 0 auto;">
        <div style="background: #f0f8ff; border-left: 5px solid #0066cc; padding: 20px; margin-bottom: 40px; border-radius: 5px;">
            <p style="margin: 0; line-height: 1.8; color: #333;">
                📧 お問い合わせ内容を確認後、2営業日以内に担当者よりご連絡いたします。<br>
                お急ぎの場合は、お電話（03-1234-5678）にてお問い合わせください。
            </p>
        </div>
        
        <!-- Contact Form 7のショートコード -->
        [contact-form-7 id="123" title="お問い合わせフォーム"]
        
        <!-- フォームがない場合のHTML例 -->
        <div style="background: #f8f9fa; padding: 40px; border-radius: 10px;">
            <form>
                <div style="margin-bottom: 25px;">
                    <label style="display: block; font-weight: bold; margin-bottom: 8px; color: #333;">
                        お名前 <span style="color: red; font-size: 12px;">必須</span>
                    </label>
                    <input type="text" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;">
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; font-weight: bold; margin-bottom: 8px; color: #333;">
                        会社名
                    </label>
                    <input type="text" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;">
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; font-weight: bold; margin-bottom: 8px; color: #333;">
                        メールアドレス <span style="color: red; font-size: 12px;">必須</span>
                    </label>
                    <input type="email" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;">
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; font-weight: bold; margin-bottom: 8px; color: #333;">
                        電話番号
                    </label>
                    <input type="tel" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;">
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: block; font-weight: bold; margin-bottom: 8px; color: #333;">
                        お問い合わせ内容 <span style="color: red; font-size: 12px;">必須</span>
                    </label>
                    <textarea required rows="6" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical;"></textarea>
                </div>
                
                <div style="margin-bottom: 25px;">
                    <label style="display: flex; align-items: start; cursor: pointer;">
                        <input type="checkbox" required style="margin-top: 5px; margin-right: 10px;">
                        <span style="color: #666; line-height: 1.6;">
                            <a href="/privacy-policy" target="_blank" style="color: #0066cc; text-decoration: underline;">プライバシーポリシー</a>に同意する
                        </span>
                    </label>
                </div>
                
                <div style="text-align: center;">
                    <button type="submit" style="background: #0066cc; color: white; padding: 15px 60px; border: none; border-radius: 30px; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(0,102,204,0.3);">
                        送信する
                    </button>
                </div>
            </form>
        </div>
    </div>
</section>

<!-- その他のお問い合わせ方法 -->
<section style="padding: 80px 20px; background: #f8f9fa;">
    <div class="container" style="max-width: 1000px; margin: 0 auto;">
        <h2 style="text-align: center; font-size: 32px; margin-bottom: 50px; color: #003366;">
            その他のお問い合わせ方法
        </h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            <!-- 電話 -->
            <div style="background: white; padding: 40px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 50px; margin-bottom: 20px;">📞</div>
                <h3 style="font-size: 20px; margin-bottom: 15px; color: #003366;">お電話でのお問い合わせ</h3>
                <p style="font-size: 24px; font-weight: bold; color: #0066cc; margin-bottom: 10px;">03-1234-5678</p>
                <p style="color: #666; font-size: 14px;">受付時間: 平日 9:00-18:00</p>
            </div>
            
            <!-- メール -->
            <div style="background: white; padding: 40px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 50px; margin-bottom: 20px;">✉️</div>
                <h3 style="font-size: 20px; margin-bottom: 15px; color: #003366;">メールでのお問い合わせ</h3>
                <p style="font-size: 18px; color: #0066cc; margin-bottom: 10px;">info@sample.co.jp</p>
                <p style="color: #666; font-size: 14px;">24時間受付</p>
            </div>
            
            <!-- FAX -->
            <div style="background: white; padding: 40px; border-radius: 10px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 50px; margin-bottom: 20px;">📠</div>
                <h3 style="font-size: 20px; margin-bottom: 15px; color: #003366;">FAXでのお問い合わせ</h3>
                <p style="font-size: 24px; font-weight: bold; color: #0066cc; margin-bottom: 10px;">03-1234-5679</p>
                <p style="color: #666; font-size: 14px;">24時間受付</p>
            </div>
        </div>
    </div>
</section>
```

---

## ⚙️ 功能模块配置

### 模块1: 使用Cocoon短代码显示最新文章

```
<!-- 最新记事3件（ボーダー区切り） -->
[new_list count="3" type="border_partition"]

<!-- 最新记事5件（カード型） -->
[new_list count="5" type="default"]

<!-- 特定カテゴリーの記事表示 -->
[new_list count="4" type="default" cats="123,456"]
※ 123,456はカテゴリーID

<!-- サムネイル画像付き -->
[new_list count="3" type="default" thumbnail="1"]
```

### 模块2: Cocoon按钮（CTA按钮）

```html
<!-- デフォルトボタン -->
[btn class="simple"]お問い合わせはこちら[/btn]

<!-- 大きいボタン -->
[btn class="big rich_pink"]
今すぐ申し込む
[/btn]

<!-- リンク付きボタン -->
[btn href="/contact" class="big rich_blue"]
無料相談する
[/btn]

<!-- アイコン付きボタン -->
[btn href="/download" class="simple" icon="icon-download"]
カタログダウンロード
[/btn]
```

### 模块3: 吹き出し（对话气泡）

```
<!-- 左側に表示 -->
[speech_bubble type="ln-flat" subtype="L1" icon="1.jpg" name="山田"]
ご質問がございましたら、お気軽にお問い合わせください。
[/speech_bubble]

<!-- 右側に表示 -->
[speech_bubble type="ln-flat" subtype="R1" icon="2.jpg" name="お客様"]
詳しい資料をいただけますか？
[/speech_bubble]
```

### 模块4: タブ（标签页）

```
[tabs]
[tab title="サービスA"]
サービスAの詳細説明がここに入ります。
[/tab]
[tab title="サービスB"]
サービスBの詳細説明がここに入ります。
[/tab]
[tab title="サービスC"]
サービスCの詳細説明がここに入ります。
[/tab]
[/tabs]
```

### 模块5: アコーディオン（手风琴）

```
[accordion title="Q: 料金はいくらですか？"]
A: 基本プランは月額10,000円からとなります。詳しくはお問い合わせください。
[/accordion]

[accordion title="Q: 無料トライアルはありますか？"]
A: はい、14日間の無料トライアルをご用意しております。
[/accordion]

[accordion title="Q: サポート体制は？"]
A: 平日9:00-18:00の間、電話・メールでサポートいたします。
[/accordion]
```

---

## 🎨 自定义设计

### 配色方案设定

```
Cocoon设定 → 全体 → サイトキーカラー

【ビジネス系】
キーカラー: #003366（ネイビーブルー）
サブカラー: #0066cc（ブルー）

【IT系】
キーカラー: #2196F3（スカイブルー）
サブカラー: #00BCD4（シアン）

【製造業】
キーカラー: #1976D2（ダークブルー）
サブカラー: #FFA726（オレンジ）

【コンサル】
キーカラー: #37474F（グレーブルー）
サブカラー: #00897B（ティール）
```

### 自定义CSS追加

```css
/* Cocoon设定 → カスタマイズ → 追加CSS */

/* ヘッダーのカスタマイズ */
.header {
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* メインビジュアルの高さ調整 */
.hero-section {
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ボタンのホバーエフェクト */
.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,102,204,0.4);
    transition: all 0.3s ease;
}

/* カードのホバーエフェクト */
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

/* フォントの調整 */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
}

/* スマホ対応 */
@media (max-width: 768px) {
    .hero-section {
        min-height: 300px;
        padding: 40px 20px;
    }
    
    h1 {
        font-size: 28px !important;
    }
    
    h2 {
        font-size: 24px !important;
    }
}

/* セクション間の余白統一 */
section {
    padding: 80px 20px;
}

@media (max-width: 768px) {
    section {
        padding: 40px 15px;
    }
}

/* テーブルのレスポンシブ対応 */
@media (max-width: 768px) {
    table {
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}
```

---

## 🚀 实战案例

### 案例1: IT咨询公司完整配置

#### サイト構成
```
1. トップページ（首页模板使用）
2. 会社概要（公司简介模板使用）
3. サービス案内
   ├─ システムコンサルティング
   ├─ クラウド導入支援
   └─ DX推進支援
4. 導入事例（事例一覧）
5. ニュース（ブログ機能）
6. 採用情報
7. お問い合わせ（联系表单模板使用）
```

#### Cocoon设定
```
【全体設定】
キーカラー: #2196F3
フォント: Noto Sans JP

【ヘッダー】
レイアウト: センターロゴ
背景色: #ffffff
メニュー背景: #2196F3

【フッター】
背景色: #263238
文字色: #ffffff
3カラムレイアウト

【SEO設定】
フロントページタイトル: ITコンサルティング | 株式会社〇〇
フロントページの説明: システム導入からDX推進まで、貴社のIT化を全面支援します
```

#### 使用的插件
```
✅ Contact Form 7（お問い合わせ）
✅ WP Mail SMTP（メール送信）
✅ Table of Contents Plus（目次自動生成）
✅ EWWW Image Optimizer（画像最適化）
✅ Google XML Sitemaps（サイトマップ）
```

#### 制作時間
```
Day 1: テーマ設定・基本ページ作成（6時間）
Day 2: コンテンツ入力・画像準備（4時間）
合計: 10時間（1-2日で完成）
```

---

### 案例2: 制造业公司配置

#### 特色功能
```
✅ 製品カタログページ（20製品）
✅ 技術紹介ページ
✅ 工場見学申込フォーム
✅ PDF資料ダウンロード
✅ 多言語対応（日本語・英語）
```

#### Cocoon设定
```
【全体設定】
キーカラー: #1976D2
サブカラー: #FFA726

【ヘッダー】
レイアウト: トップメニュー（小）
ロゴサイズ: 高さ50px

【投稿設定】
投稿日・更新日: 表示
カテゴリー: 表示
タグ: 非表示
```

#### 追加插件
```
✅ Download Monitor（資料ダウンロード管理）
✅ WPML（多言語対応）※有料
✅ WP Forms（高度なフォーム）
```

---

## 📊 性能优化技巧

### 1. 画像最適化

```
Cocoon设定 → 画像

【LazyLoad設定】
画像の遅延読み込み: ON
iframeの遅延読み込み: ON

【推奨画像サイズ】
ヘッダー画像: 1920x600px
サムネイル: 640x360px
記事内画像: 最大幅800px

【画像形式】
写真: WebP形式（推奨）
ロゴ・イラスト: SVG形式
```

### 2. キャッシュ設定

```
プラグイン: WP Super Cache または W3 Total Cache

設定:
✅ ページキャッシュ: ON
✅ ブラウザキャッシュ: ON
✅ Gzip圧縮: ON
```

### 3. 不要機能の無効化

```
Cocoon设定 → パフォーマンス

無効化推奨:
✅ 絵文字スクリプト: 無効
✅ jQuery Migrate: 無効
✅ ブログカード外部リクエスト: 無効（企业网站不需要）
```

---

## 🔧 トラブルシューティング

### 問題1: ページが正しく表示されない

```
【解決方法】
1. Cocoon Child（子テーマ）を有効化しているか確認
2. キャッシュクリア
   → Cocoon设定 → キャッシュ削除
   → ブラウザキャッシュクリア (Ctrl+Shift+Delete)
3. プラグインの競合確認
   → プラグインを一時的に全て無効化して確認
```

### 問題2: スマホ表示が崩れる

```
【確認ポイント】
1. Cocoon设定 → モバイル → レスポンシブ: ON
2. カスタムCSSの@mediaクエリ確認
3. テーブルの幅指定を%で設定
4. 画像のmax-width: 100%設定
```

### 問題3: ショートコードが表示されない

```
【原因】
- プラグインとの競合
- テーマのバージョンが古い

【解決方法】
1. Cocoonを最新版にアップデート
2. プラグインを一つずつ無効化して特定
3. [raw][/raw]タグで囲む
```

---

## 📚 学習リソース

### Cocoon公式サイト
```
🌐 https://wp-cocoon.com/
- テーマダウンロード
- 設定マニュアル
- カスタマイズ方法
- フォーラム（質問可能）
```

### 推奨YouTube教程
```
検索キーワード:
- "Cocoon 使い方"
- "Cocoon カスタマイズ"
- "Cocoon 企業サイト"
- "Cocoon 設定方法"
```

---

## ✅ 完成チェックリスト

### 公開前チェック

```
□ Cocoon Child（子テーマ）有効化
□ サイトタイトル・キャッチフレーズ設定
□ ファビコン設定
□ ロゴ画像アップロード
□ メニュー作成・設定
□ 全ページ作成完了
□ お問い合わせフォーム動作確認
□ メール送信テスト成功
□ スマホ表示確認
□ タブレット表示確認
□ 全リンク動作確認
□ 画像最適化完了
□ SEO設定完了
□ プライバシーポリシー掲載
□ SSL証明書設定（HTTPS）
□ Google Analytics設置
□ Google Search Console登録
```

---

## 🎉 まとめ

### Cocoon使用の最大メリット

```
💰 完全無料
⚡ 高速表示
📱 レスポンシブ完璧
🔍 SEO最適化済み
🇯🇵 日本語完全対応
🎨 カスタマイズ豊富
📚 ドキュメント充実
👥 コミュニティ活発

→ 企業サイト制作に最適！
```

### 開発時間・コスト

```
開発時間: 1-2日
初期費用: ¥0
月額費用: ¥0
年間費用: ¥0

外注費用（¥300,000-800,000）と比較
→ 100%削減！
```

---

**次のステップ: 実際にCocoonをインストールして、このガイドの模板を使って企業サイトを作ってみましょう！** 🚀
