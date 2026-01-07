# 日本企業サイト 完全開発ガイド 🇯🇵

> **目標**: 最低コストで迅速に開発・オンライン化  
> **既存リソース**: onamae.com RSプラン WordPress サーバー  
> **必須機能**: ニュース配信、問い合わせフォーム、メール送信

---

## 📊 方案比較表

| 方案 | 開発時間 | コスト | 難易度 | おすすめ度 |
|------|----------|--------|--------|------------|
| **方案1: WordPress単体** | 2-3日 | ¥0 | ⭐ | ⭐⭐⭐⭐⭐ |
| **方案2: Bootstrap Studio + WordPress** | 3-5日 | $60 | ⭐⭐ | ⭐⭐⭐⭐ |
| **方案3: VSCode + WordPress連携** | 4-7日 | ¥0 | ⭐⭐⭐ | ⭐⭐⭐ |
| **方案4: Elementor Pro (推奨)** | 1-2日 | $59/年 | ⭐ | ⭐⭐⭐⭐⭐ |

---

## 🏆 方案1: WordPress単体方案【最推奨】

### ✅ メリット
- **完全無料** (既存サーバー利用)
- **最速実装** (2-3日で完成)
- **日本語対応完璧** (テーマ多数)
- **プラグインで全機能実現**

### 📦 必要なもの
1. **テーマ**: Lightning (無料・日本製)
2. **フォームプラグイン**: Contact Form 7 (無料)
3. **ニュース機能**: WordPress標準機能
4. **メール送信**: WP Mail SMTP (無料)

### 🚀 実装手順

#### Step 1: WordPressセットアップ (30分)

```bash
# onamae.com RSプランにログイン
# WordPress自動インストール機能を使用
# 推奨設定:
# - サイト名: 会社名
# - ユーザー名: admin以外
# - パスワード: 強力なもの
```

#### Step 2: テーマインストール (15分)

```
WordPress管理画面 → 外観 → テーマ → 新規追加
検索: "Lightning"
インストール → 有効化

推奨日本企業向けテーマ:
1. Lightning (無料) - 日本企業に最適
2. Xeory Extension (無料) - SEO最適化済み
3. Cocoon (無料) - 多機能
4. Business Press (無料) - ビジネス向け
```

#### Step 3: 必須プラグインインストール (30分)

```
プラグイン → 新規追加

【必須プラグイン】
1. Contact Form 7 - 問い合わせフォーム
2. WP Mail SMTP - メール送信設定
3. VK All in One Expansion Unit - Lightningの拡張機能
4. SiteGuard WP Plugin - セキュリティ
5. EWWW Image Optimizer - 画像最適化

【オプション】
6. Yoast SEO - SEO対策
7. UpdraftPlus - バックアップ
8. WP Super Cache - キャッシュ
```

#### Step 4: 問い合わせフォーム設定 (20分)

```
Contact Form 7 → 新規追加

【日本企業標準フォーム】
<label> お名前 (必須)
[text* your-name] </label>

<label> 会社名
[text your-company] </label>

<label> メールアドレス (必須)
[email* your-email] </label>

<label> 電話番号
[tel your-phone] </label>

<label> お問い合わせ内容 (必須)
[textarea* your-message] </label>

[submit "送信する"]

【メール設定】
送信先: info@yourcompany.co.jp
送信元: wordpress@yourcompany.co.jp
題名: [お問い合わせ] [your-name]様より
```

#### Step 5: メール送信設定 (30分)

```
WP Mail SMTP → 設定

【onamae.comメールサーバー設定】
送信方法: Other SMTP
SMTP Host: mail.onamae.com
SMTPポート: 465
暗号化: SSL
認証: ON
SMTPユーザー名: info@yourcompany.co.jp
SMTPパスワード: [メールパスワード]

【テスト送信】
設定 → Eメールテスト → テストメール送信
```

#### Step 6: ニュース機能設定 (30分)

```
# WordPressの投稿機能を「ニュース」として利用

設定 → 投稿設定
カテゴリー追加:
- お知らせ
- プレスリリース
- イベント情報
- 製品情報

固定ページ作成:
1. ニュース一覧ページ
2. トップページに最新ニュース3件表示

【ショートコード例】
トップページに挿入:
[display-posts posts_per_page="3" include_excerpt="true"]
```

#### Step 7: ページ作成 (2-3時間)

```
【日本企業標準ページ構成】
1. トップページ (HOME)
2. 会社概要 (Company)
3. 事業内容 (Business)
4. 製品・サービス (Products/Services)
5. ニュース (News)
6. 採用情報 (Recruit)
7. お問い合わせ (Contact)
8. プライバシーポリシー (Privacy)

各ページ作成:
固定ページ → 新規追加
Lightningのページビルダーで作成
```

### 💰 コスト内訳

```
初期費用: ¥0
月額費用: ¥0 (既存サーバー利用)
年間費用: ¥0

※onamae.com RSプラン料金は既存契約に含まれる
```

### 📱 レスポンシブ対応

```
Lightningテーマは自動対応
確認方法:
- スマホ表示: F12 → デバイスツールバー
- タブレット表示: サイズ変更で確認
```

---

## 🎨 方案2: Bootstrap Studio + WordPress

### 📋 概要
- **Bootstrap Studio**: 静的HTMLデザイン作成
- **WordPress**: コンテンツ管理・フォーム・ニュース機能

### 役割分担

```
【Bootstrap Studio】60%
- トップページデザイン
- 企業情報ページ
- 製品紹介ページ
- レスポンシブレイアウト
- カスタムアニメーション

【WordPress】40%
- ニュース記事管理
- 問い合わせフォーム
- メール送信機能
- 管理画面での更新
```

### 🚀 実装手順

#### Phase 1: Bootstrap Studioでデザイン (2日)

```bash
# 1. Bootstrap Studioインストール
# 価格: $60 (買い切り)
# ダウンロード: https://bootstrapstudio.io/

# 2. 日本企業テンプレート選択
File → New from Template
推奨テンプレート:
- Corporate Template
- Business Template
- Professional Template
```

#### Phase 2: ページ作成

```html
<!-- トップページ構成例 -->
1. ヘッダーナビゲーション
   - 会社ロゴ
   - メニュー (会社概要/事業内容/ニュース/採用/問い合わせ)
   - 言語切替 (日本語/English)

2. メインビジュアル
   - スライドショー (3-5枚)
   - キャッチコピー
   - CTAボタン

3. 事業紹介セクション
   - 3カラムレイアウト
   - アイコン + テキスト

4. 最新ニュース (WordPress連携部分)
   - 3件表示
   - 「もっと見る」リンク

5. 会社概要
   - 簡易情報
   - アクセスマップ

6. フッター
   - 会社情報
   - SNSリンク
   - プライバシーポリシー
```

#### Phase 3: WordPressテーマ化 (1日)

```bash
# 1. Bootstrap Studio → Export
File → Export → Custom Code

# 2. ファイル構成変換
static-site/
├── index.html
├── css/
├── js/
└── images/

↓ 変換 ↓

wordpress-theme/
├── style.css
├── index.php
├── header.php
├── footer.php
├── functions.php
├── page-templates/
├── css/
├── js/
└── images/
```

#### Phase 4: WordPress統合

```php
// functions.php - 基本設定
<?php
function custom_theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    
    register_nav_menus(array(
        'primary' => 'メインメニュー',
        'footer' => 'フッターメニュー'
    ));
}
add_action('after_setup_theme', 'custom_theme_setup');

// スタイル読み込み
function custom_scripts() {
    wp_enqueue_style('bootstrap', get_template_directory_uri() . '/css/bootstrap.min.css');
    wp_enqueue_style('main-style', get_stylesheet_uri());
    wp_enqueue_script('bootstrap-js', get_template_directory_uri() . '/js/bootstrap.bundle.min.js', array('jquery'), null, true);
}
add_action('wp_enqueue_scripts', 'custom_scripts');
?>
```

```php
// index.php - ニュース一覧表示
<?php get_header(); ?>

<div class="container mt-5">
    <h1>ニュース</h1>
    
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article class="mb-4">
            <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p class="text-muted"><?php the_date(); ?></p>
            <?php the_excerpt(); ?>
        </article>
    <?php endwhile; endif; ?>
</div>

<?php get_footer(); ?>
```

### 💰 コスト内訳

```
Bootstrap Studio: $60 (買い切り)
WordPress: ¥0
プラグイン: ¥0
合計初期費用: $60 (約¥9,000)
月額費用: ¥0
```

---

## 💻 方案3: VSCode + WordPress連携

### 📋 概要
VSCodeでローカル開発 → WordPressサーバーに同期

### 役割分担

```
【VSCode】開発環境
- HTMLテンプレート作成
- CSS/JavaScriptカスタマイズ
- Git版本管理
- FTP/SFTPでファイル同期

【WordPress】本番環境
- コンテンツ管理
- プラグイン機能
- データベース管理
```

### 🚀 実装手順

#### Step 1: VSCode環境構築 (30分)

```bash
# 1. VSCodeインストール済み確認
code --version

# 2. 必要な拡張機能インストール
- PHP Intelephense
- WordPress Snippets
- SFTP/FTP Sync
- Live Server
- Prettier - Code formatter
```

#### Step 2: ローカル開発環境

```bash
# プロジェクト構造
mkdir japan-corporate-site
cd japan-corporate-site

japan-corporate-site/
├── wp-content/
│   └── themes/
│       └── corporate-theme/
│           ├── style.css
│           ├── index.php
│           ├── header.php
│           ├── footer.php
│           ├── functions.php
│           ├── page-templates/
│           │   ├── front-page.php
│           │   ├── page-about.php
│           │   └── page-contact.php
│           ├── css/
│           │   └── custom.css
│           ├── js/
│           │   └── custom.js
│           └── images/
└── .vscode/
    └── sftp.json
```

#### Step 3: SFTP設定

```json
// .vscode/sftp.json
{
    "name": "onamae.com WordPress",
    "host": "your-server.onamae.com",
    "protocol": "sftp",
    "port": 22,
    "username": "your-username",
    "password": "your-password",
    "remotePath": "/home/your-username/public_html/wp-content/themes/corporate-theme",
    "uploadOnSave": true,
    "ignore": [
        ".vscode",
        ".git",
        "node_modules"
    ]
}
```

#### Step 4: テーマ開発

```css
/* style.css - WordPressテーマヘッダー */
/*
Theme Name: Japan Corporate Theme
Theme URI: https://yourcompany.co.jp
Description: 日本企業向けカスタムテーマ
Author: Your Name
Version: 1.0
License: GNU General Public License v2 or later
Text Domain: japan-corporate
*/

/* カスタムスタイル */
:root {
    --primary-color: #003366;
    --secondary-color: #0066cc;
    --text-color: #333333;
}

body {
    font-family: 'Noto Sans JP', sans-serif;
    color: var(--text-color);
}

.hero-section {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 100px 0;
}
```

```php
// front-page.php - トップページテンプレート
<?php
/*
Template Name: Front Page
*/
get_header();
?>

<section class="hero-section">
    <div class="container">
        <h1>あなたのビジネスを<br>次のステージへ</h1>
        <p class="lead">革新的なソリューションで企業の成長を支援</p>
        <a href="#contact" class="btn btn-light btn-lg">お問い合わせ</a>
    </div>
</section>

<section class="news-section py-5">
    <div class="container">
        <h2 class="text-center mb-4">最新ニュース</h2>
        <div class="row">
            <?php
            $news_query = new WP_Query(array(
                'post_type' => 'post',
                'posts_per_page' => 3
            ));
            
            if ($news_query->have_posts()) :
                while ($news_query->have_posts()) : $news_query->the_post();
            ?>
                <div class="col-md-4">
                    <div class="card">
                        <?php if (has_post_thumbnail()) : ?>
                            <?php the_post_thumbnail('medium', array('class' => 'card-img-top')); ?>
                        <?php endif; ?>
                        <div class="card-body">
                            <p class="text-muted"><?php the_date(); ?></p>
                            <h5 class="card-title"><?php the_title(); ?></h5>
                            <p class="card-text"><?php the_excerpt(); ?></p>
                            <a href="<?php the_permalink(); ?>" class="btn btn-primary">詳しく見る</a>
                        </div>
                    </div>
                </div>
            <?php
                endwhile;
                wp_reset_postdata();
            endif;
            ?>
        </div>
    </div>
</section>

<?php get_footer(); ?>
```

#### Step 5: 同期とデプロイ

```bash
# VSCodeコマンドパレット (Ctrl+Shift+P)
SFTP: Sync Local -> Remote

# または右クリック
右クリック → Upload Folder
```

### 💰 コスト内訳

```
VSCode: ¥0 (無料)
プラグイン: ¥0 (無料)
開発時間: 4-7日
月額費用: ¥0
```

---

## ⚡ 方案4: Elementor Pro【超高速開発】

### ✅ なぜ最速か？

```
1. ドラッグ&ドロップで完成
2. 日本語テンプレート豊富
3. フォーム機能内蔵
4. レスポンシブ自動対応
5. コード知識不要
```

### 🚀 実装手順 (1-2日で完成)

#### Step 1: Elementor Pro購入 (10分)

```
価格: $59/年 (約¥9,000)
公式サイト: https://elementor.com/pricing/
プラン: Essential ($59/年・1サイト)
```

#### Step 2: インストール (15分)

```
WordPress管理画面
プラグイン → 新規追加 → "Elementor" 検索
1. Elementor (無料版) - インストール
2. Elementor Pro - ライセンスキー入力
```

#### Step 3: テンプレート選択 (30分)

```
Elementor → テンプレート → ライブラリ

日本企業向けテンプレート:
1. Corporate Business
2. Professional Services
3. Consulting Firm
4. Technology Company

選択 → Import → カスタマイズ開始
```

#### Step 4: ページ作成 (3-4時間)

```
【超高速作成手順】
1. テンプレート挿入
2. テキストをクリックして会社情報に変更
3. 画像をドラッグ&ドロップで置き換え
4. カラースキーム変更 (ブランドカラー)
5. 公開ボタンクリック

完了!
```

#### Step 5: フォーム設定 (30分)

```
Elementor Proフォームウィジェット:
1. フォームウィジェットをドラッグ
2. フィールド追加:
   - 名前
   - 会社名
   - メールアドレス
   - 電話番号
   - 問い合わせ内容
3. Actions設定:
   - Email: info@yourcompany.co.jp
   - Email2: 自動返信メール
4. SMTP設定: WP Mail SMTP連携
```

### 💰 コスト内訳

```
Elementor Pro: $59/年
初期費用: ¥9,000
月額費用: ¥0
更新費: ¥9,000/年
```

---

## 📧 無料メール・ニュース機能実装

### 方法1: Contact Form 7 + WP Mail SMTP (完全無料)

```
【問い合わせフォーム】
プラグイン: Contact Form 7
設定時間: 20分
機能: フォーム送信、自動返信

【メール送信】
プラグイン: WP Mail SMTP
設定時間: 30分
対応: onamae.comメールサーバー

【ニュース配信】
機能: WordPress標準投稿機能
RSS配信: 自動生成
カテゴリ: お知らせ/プレスリリース/イベント
```

### 方法2: Mailchimp連携 (無料枠あり)

```
無料プラン: 月2,000通まで
プラグイン: MC4WP (無料)

設定手順:
1. Mailchimp アカウント作成
2. API キー取得
3. MC4WP インストール
4. フォーム作成
5. メール配信設定

【メリット】
- プロフェッショナルなメールデザイン
- 開封率・クリック率分析
- 自動配信設定
```

### 方法3: Sendinblue (無料: 300通/日)

```
プラグイン: Sendinblue (無料)

機能:
✅ トランザクションメール (無制限)
✅ マーケティングメール (300通/日)
✅ SMS送信
✅ チャット機能

設定:
1. Sendinblue登録
2. プラグインインストール
3. APIキー連携
4. 送信者設定
```

---

## 🚀 デプロイ設定

### onamae.com RSプラン設定

```bash
【FTP/SFTP情報】
ホスト: ftp.your-domain.com
ポート: 21 (FTP) / 22 (SFTP)
ユーザー名: [契約時のユーザー名]
パスワード: [設定したパスワード]
ルートディレクトリ: /public_html/

【WordPress URL設定】
設定 → 一般設定
WordPress アドレス: https://yourcompany.co.jp
サイトアドレス: https://yourcompany.co.jp

【SSL証明書】
onamae.com管理画面 → SSL設定
Let's Encrypt (無料) を有効化

【.htaccess設定】
# HTTPS強制リダイレクト
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
```

### バックアップ設定

```
プラグイン: UpdraftPlus (無料)

自動バックアップ設定:
- スケジュール: 毎日
- 保存先: Google Drive / Dropbox (無料)
- 保持期間: 30日分

手動バックアップ:
管理画面 → UpdraftPlus → 今すぐバックアップ
```

---

## 📊 方案選択フローチャート

```
コーディング経験あり？
├─ YES → 技術的チャレンジしたい？
│   ├─ YES → 【方案3】VSCode + WordPress
│   └─ NO → 【方案1】WordPress単体
│
└─ NO → 予算ある？($60)
    ├─ YES → デザイン重視？
    │   ├─ YES → 【方案4】Elementor Pro (最速)
    │   └─ NO → 【方案2】Bootstrap Studio
    │
    └─ NO → 【方案1】WordPress単体 (完全無料)
```

---

## 🎯 推奨方案: 段階的アプローチ

### Phase 1: まず動くものを作る (1-2日)

```
【方案1】WordPress単体で開始
↓
基本機能実装:
- Lightning テーマ
- Contact Form 7
- WP Mail SMTP
- 基本ページ作成

コスト: ¥0
時間: 2日
```

### Phase 2: デザイン改善 (必要に応じて)

```
オプション1: Elementor Pro 追加
コスト: $59/年
効果: プロフェッショナルなデザイン

オプション2: Bootstrap Studio
コスト: $60 (買い切り)
効果: 完全カスタムデザイン
```

### Phase 3: 機能拡張 (運用開始後)

```
- 多言語対応 (WPML: $39/年)
- 予約システム (Amelia: 無料版あり)
- ECサイト機能 (WooCommerce: 無料)
- 会員システム (Ultimate Member: 無料)
```

---

## 📋 実装チェックリスト

### 立ち上げ前 (1週間以内)

- [ ] WordPressインストール
- [ ] テーマ選択・インストール
- [ ] 必須プラグインインストール
- [ ] 問い合わせフォーム作成
- [ ] メール送信テスト成功
- [ ] 基本ページ作成 (7ページ)
- [ ] レスポンシブ確認
- [ ] SSL証明書設定
- [ ] Google Analytics設定
- [ ] Google Search Console登録

### ローンチ時

- [ ] 全ページ動作確認
- [ ] フォーム送信テスト
- [ ] メール受信確認
- [ ] スマホ表示確認
- [ ] 読み込み速度チェック
- [ ] SEO基本設定完了
- [ ] プライバシーポリシー掲載
- [ ] サイトマップ生成

### ローンチ後 (1ヶ月)

- [ ] バックアップ自動化
- [ ] アクセス解析確認
- [ ] ニュース記事3件投稿
- [ ] SNS連携設定
- [ ] お客様からの問い合わせ対応テスト

---

## 💡 成功のポイント

### 1. まずは完璧を目指さない

```
✅ 60%の完成度で公開
✅ フィードバック収集
✅ 段階的改善

❌ 100%完璧になるまで非公開
```

### 2. 既存リソースを最大活用

```
✅ onamae.com サーバー活用
✅ WordPress標準機能使用
✅ 無料プラグイン優先
✅ 無料テーマから開始

💰 初期コスト: ¥0
```

### 3. 将来の拡張性を考慮

```
✅ プラグインで機能追加可能
✅ テーマ変更容易
✅ 多言語対応準備
✅ EC機能追加可能

🚀 ビジネス成長に対応
```

---

## 📚 参考リソース

### WordPress公式

- [WordPress.org](https://ja.wordpress.org/)
- [テーマディレクトリ](https://ja.wordpress.org/themes/)
- [プラグインディレクトリ](https://ja.wordpress.org/plugins/)

### 学習リソース

- [WordPress Codex 日本語版](https://wpdocs.osdn.jp/)
- [ドットインストール WordPress入門](https://dotinstall.com/lessons/basic_wordpress)
- [Udemy WordPress講座](https://www.udemy.com/topic/wordpress/)

### コミュニティ

- [WordBench](https://wordbench.org/) - 日本のWordPressコミュニティ
- [WordPress フォーラム](https://ja.wordpress.org/support/forums/)

---

## 🆘 トラブルシューティング

### よくある問題と解決方法

```
【問題1】メールが送信されない
→ WP Mail SMTP設定確認
→ SMTPポート 465/587 試す
→ SSL/TLS設定確認

【問題2】画像がアップロードできない
→ php.ini upload_max_filesize 確認
→ メディア設定確認
→ サーバーディスク容量確認

【問題3】ページが遅い
→ 画像最適化 (EWWW Image Optimizer)
→ キャッシュプラグイン導入
→ 不要プラグイン削除

【問題4】フォームスパム
→ reCAPTCHA 追加
→ Akismet 設定
→ SiteGuard WP Plugin 有効化
```

---

## 🎉 まとめ: 最速・最安ロードマップ

### Week 1: 立ち上げ

```
Day 1-2: WordPress単体セットアップ
- テーマインストール (Lightning)
- プラグイン設定
- 基本ページ作成

Day 3-4: コンテンツ作成
- 会社情報入力
- 画像準備・アップロード
- ニュース記事作成

Day 5: テスト
- フォームテスト
- メール送信テスト
- レスポンシブ確認

Day 6-7: 公開準備
- SSL設定
- 最終確認
- 🚀 ローンチ!
```

### 総コスト

```
必須コスト: ¥0
オプション (Elementor Pro): ¥9,000/年
推奨初期投資: ¥0〜¥9,000

月額ランニングコスト: ¥0
(onamae.comサーバー代は既存)
```

---

**質問やサポートが必要な場合は、具体的な実装フェーズをお知らせください!** 🚀
