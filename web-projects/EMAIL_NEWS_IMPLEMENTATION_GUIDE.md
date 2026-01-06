# 邮件服务器部署与功能实现完整指南

## 📋 目录

1. [邮件服务器部署方案](#1-邮件服务器部署方案)
2. [邮件发送功能实现](#2-邮件发送功能实现)
3. [新闻/表单提交功能](#3-新闻表单提交功能)
4. [完整项目示例](#4-完整项目示例)
5. [生产环境部署](#5-生产环境部署)

---

## 1. 邮件服务器部署方案

### 1.1 方案对比

| 方案 | 优点 | 缺点 | 适用场景 | 成本 |
|------|------|------|----------|------|
| **第三方邮件服务** | 简单、稳定、高送达率 | 需付费、有发送限制 | 推荐方案 | ¥0-500/月 |
| **云服务商SMTP** | 专业、可靠 | 需配置 | 中大型企业 | ¥200-1000/月 |
| **自建邮件服务器** | 完全控制 | 复杂、易进垃圾箱 | 技术团队 | 服务器成本 |

---

## 2. 邮件发送功能实现

### 2.1 方案一：使用 Nodemailer (Node.js)

#### 安装依赖
```bash
npm install nodemailer express body-parser dotenv
```

#### 项目结构
```
email-service/
├── .env                    # 环境配置
├── package.json
├── server.js              # 服务器主文件
├── config/
│   └── emailConfig.js     # 邮件配置
├── routes/
│   ├── contactRoute.js    # 联系表单路由
│   └── newsRoute.js       # 新闻提交路由
├── controllers/
│   ├── emailController.js # 邮件控制器
│   └── newsController.js  # 新闻控制器
├── templates/
│   ├── contactEmail.html  # 联系邮件模板
│   └── newsAlert.html     # 新闻通知模板
└── public/
    ├── contact.html       # 联系表单页面
    └── news-submit.html   # 新闻提交页面
```

#### .env 配置文件
```env
# 邮件服务配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# 接收邮件地址
ADMIN_EMAIL=admin@company.com
NOTIFICATION_EMAIL=notifications@company.com

# 服务器配置
PORT=3000
NODE_ENV=production

# 数据库配置（新闻存储）
DB_HOST=localhost
DB_USER=root
DB_PASS=password
DB_NAME=company_website
```

#### config/emailConfig.js
```javascript
const nodemailer = require('nodemailer');
require('dotenv').config();

// 创建邮件传输器
const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    },
    tls: {
        rejectUnauthorized: false
    }
});

// 验证邮件配置
transporter.verify(function(error, success) {
    if (error) {
        console.error('邮件服务器连接失败:', error);
    } else {
        console.log('✅ 邮件服务器已就绪');
    }
});

module.exports = transporter;
```

#### controllers/emailController.js
```javascript
const transporter = require('../config/emailConfig');
const fs = require('fs');
const path = require('path');

// 发送联系表单邮件
exports.sendContactEmail = async (req, res) => {
    try {
        const { name, email, phone, subject, message } = req.body;

        // 数据验证
        if (!name || !email || !message) {
            return res.status(400).json({
                success: false,
                message: '请填写所有必填字段'
            });
        }

        // 邮件验证
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({
                success: false,
                message: '邮箱格式不正确'
            });
        }

        // 读取邮件模板
        const templatePath = path.join(__dirname, '../templates/contactEmail.html');
        let htmlTemplate = fs.readFileSync(templatePath, 'utf8');

        // 替换模板变量
        htmlTemplate = htmlTemplate
            .replace('{{name}}', name)
            .replace('{{email}}', email)
            .replace('{{phone}}', phone || '未提供')
            .replace('{{subject}}', subject || '无主题')
            .replace('{{message}}', message)
            .replace('{{date}}', new Date().toLocaleString('zh-CN'));

        // 发送给管理员
        const mailOptions = {
            from: `"${name}" <${process.env.SMTP_USER}>`,
            to: process.env.ADMIN_EMAIL,
            replyTo: email,
            subject: `【网站留言】${subject || '新消息'}`,
            html: htmlTemplate,
            text: `
姓名: ${name}
邮箱: ${email}
电话: ${phone || '未提供'}
主题: ${subject || '无'}
留言内容:
${message}
            `
        };

        await transporter.sendMail(mailOptions);

        // 发送自动回复给用户
        const autoReplyOptions = {
            from: `"公司客服" <${process.env.SMTP_USER}>`,
            to: email,
            subject: '感谢您的留言 - 我们已收到',
            html: `
                <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                        <h2 style="color: #333;">感谢您的留言，${name}！</h2>
                        <p>我们已经收到您的消息，我们的团队会在 24 小时内回复您。</p>
                        <div style="background-color: #f9f9f9; padding: 15px; margin: 20px 0; border-left: 4px solid #007bff;">
                            <h3>您的留言内容：</h3>
                            <p><strong>主题：</strong>${subject || '无'}</p>
                            <p><strong>内容：</strong>${message}</p>
                        </div>
                        <p style="color: #666; font-size: 14px;">如有紧急事项，请直接致电：400-123-4567</p>
                        <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
                        <p style="color: #999; font-size: 12px;">本邮件由系统自动发送，请勿直接回复。</p>
                    </div>
                </div>
            `
        };

        await transporter.sendMail(autoReplyOptions);

        res.status(200).json({
            success: true,
            message: '消息已发送，我们会尽快回复您！'
        });

    } catch (error) {
        console.error('发送邮件失败:', error);
        res.status(500).json({
            success: false,
            message: '发送失败，请稍后重试',
            error: process.env.NODE_ENV === 'development' ? error.message : undefined
        });
    }
};

// 发送测试邮件
exports.sendTestEmail = async (req, res) => {
    try {
        const mailOptions = {
            from: process.env.SMTP_USER,
            to: process.env.ADMIN_EMAIL,
            subject: '测试邮件 - 邮件服务正常',
            html: `
                <h2>邮件服务测试</h2>
                <p>这是一封测试邮件，如果您收到此邮件，说明邮件服务配置正确。</p>
                <p>发送时间: ${new Date().toLocaleString('zh-CN')}</p>
            `
        };

        await transporter.sendMail(mailOptions);

        res.status(200).json({
            success: true,
            message: '测试邮件已发送'
        });
    } catch (error) {
        console.error('测试邮件发送失败:', error);
        res.status(500).json({
            success: false,
            message: '测试邮件发送失败',
            error: error.message
        });
    }
};
```

#### templates/contactEmail.html
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网站留言</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <!-- 头部 -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px;">新的网站留言</h1>
                        </td>
                    </tr>
                    
                    <!-- 内容 -->
                    <tr>
                        <td style="padding: 30px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="padding-bottom: 20px;">
                                        <h2 style="color: #333; margin: 0 0 10px 0;">留言详情</h2>
                                        <p style="color: #666; margin: 0; font-size: 14px;">接收时间: {{date}}</p>
                                    </td>
                                </tr>
                                
                                <!-- 发件人信息 -->
                                <tr>
                                    <td style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td width="100" style="padding: 5px 0; color: #666; font-weight: bold;">姓名：</td>
                                                <td style="padding: 5px 0; color: #333;">{{name}}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 5px 0; color: #666; font-weight: bold;">邮箱：</td>
                                                <td style="padding: 5px 0;">
                                                    <a href="mailto:{{email}}" style="color: #667eea; text-decoration: none;">{{email}}</a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 5px 0; color: #666; font-weight: bold;">电话：</td>
                                                <td style="padding: 5px 0; color: #333;">{{phone}}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 5px 0; color: #666; font-weight: bold;">主题：</td>
                                                <td style="padding: 5px 0; color: #333;">{{subject}}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- 留言内容 -->
                                <tr>
                                    <td style="padding: 20px 0;">
                                        <h3 style="color: #333; margin: 0 0 15px 0;">留言内容：</h3>
                                        <div style="background-color: #f9f9f9; padding: 20px; border-left: 4px solid #667eea; border-radius: 4px; color: #333; line-height: 1.6;">
                                            {{message}}
                                        </div>
                                    </td>
                                </tr>
                                
                                <!-- 快速回复按钮 -->
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <a href="mailto:{{email}}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 15px 40px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                                            快速回复
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- 页脚 -->
                    <tr>
                        <td style="background-color: #f4f4f4; padding: 20px; text-align: center;">
                            <p style="color: #999; margin: 0; font-size: 12px;">
                                本邮件由网站自动发送 | 
                                <a href="https://www.company.com" style="color: #667eea; text-decoration: none;">访问网站</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

#### routes/contactRoute.js
```javascript
const express = require('express');
const router = express.Router();
const emailController = require('../controllers/emailController');

// 联系表单提交
router.post('/contact', emailController.sendContactEmail);

// 测试邮件
router.get('/test-email', emailController.sendTestEmail);

module.exports = router;
```

#### server.js
```javascript
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const contactRoute = require('./routes/contactRoute');
const newsRoute = require('./routes/newsRoute');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// API 路由
app.use('/api', contactRoute);
app.use('/api', newsRoute);

// 根路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 健康检查
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date() });
});

// 错误处理
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        success: false,
        message: '服务器内部错误'
    });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`✅ 服务器运行在 http://localhost:${PORT}`);
    console.log(`📧 邮件服务已配置: ${process.env.SMTP_HOST}`);
});
```

#### public/contact.html（前端表单）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>联系我们</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }

        .required {
            color: #e74c3c;
        }

        input, textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        textarea {
            resize: vertical;
            min-height: 120px;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>联系我们</h1>
        <p class="subtitle">有任何问题？请填写表单，我们会尽快回复您。</p>

        <div id="message" class="message"></div>

        <form id="contactForm">
            <div class="form-group">
                <label>姓名 <span class="required">*</span></label>
                <input type="text" name="name" id="name" required placeholder="请输入您的姓名">
            </div>

            <div class="form-group">
                <label>邮箱 <span class="required">*</span></label>
                <input type="email" name="email" id="email" required placeholder="example@email.com">
            </div>

            <div class="form-group">
                <label>电话</label>
                <input type="tel" name="phone" id="phone" placeholder="您的联系电话">
            </div>

            <div class="form-group">
                <label>主题</label>
                <input type="text" name="subject" id="subject" placeholder="咨询主题">
            </div>

            <div class="form-group">
                <label>留言内容 <span class="required">*</span></label>
                <textarea name="message" id="message" required placeholder="请详细描述您的问题或需求..."></textarea>
            </div>

            <button type="submit" class="btn" id="submitBtn">
                <span id="btnText">发送消息</span>
            </button>
        </form>
    </div>

    <script>
        const form = document.getElementById('contactForm');
        const messageDiv = document.getElementById('message');
        const submitBtn = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // 禁用按钮
            submitBtn.disabled = true;
            btnText.innerHTML = '<span class="loading"></span> 发送中...';

            // 收集表单数据
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value
            };

            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (data.success) {
                    showMessage('success', '✅ ' + data.message);
                    form.reset();
                } else {
                    showMessage('error', '❌ ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', '❌ 发送失败，请检查网络连接后重试');
            } finally {
                // 恢复按钮
                submitBtn.disabled = false;
                btnText.textContent = '发送消息';
            }
        });

        function showMessage(type, text) {
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messageDiv.style.display = 'block';

            // 3秒后自动隐藏
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    </script>
</body>
</html>
```

---

## 3. 新闻/表单提交功能

### 3.1 数据库设计

#### MySQL 数据库表结构
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS company_website CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE company_website;

-- 新闻表
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100),
    category VARCHAR(50),
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    featured_image VARCHAR(500),
    views INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    INDEX idx_status (status),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 联系表单记录表
CREATE TABLE contact_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status ENUM('new', 'processing', 'replied', 'closed') DEFAULT 'new',
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 新闻分类表
CREATE TABLE news_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例分类
INSERT INTO news_categories (name, slug, description) VALUES
('公司新闻', 'company-news', '公司最新动态和新闻'),
('产品更新', 'product-updates', '产品功能更新和发布'),
('行业资讯', 'industry-news', '行业相关新闻和资讯');
```

### 3.2 新闻管理功能实现

#### controllers/newsController.js
```javascript
const mysql = require('mysql2/promise');
const transporter = require('../config/emailConfig');
require('dotenv').config();

// 创建数据库连接池
const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// 提交新闻
exports.submitNews = async (req, res) => {
    try {
        const { title, content, author, category, featured_image } = req.body;

        // 验证必填字段
        if (!title || !content) {
            return res.status(400).json({
                success: false,
                message: '标题和内容为必填项'
            });
        }

        // 插入数据库
        const [result] = await pool.execute(
            'INSERT INTO news (title, content, author, category, featured_image, status) VALUES (?, ?, ?, ?, ?, ?)',
            [title, content, author || '匿名', category || '未分类', featured_image || null, 'draft']
        );

        const newsId = result.insertId;

        // 发送邮件通知管理员
        const mailOptions = {
            from: process.env.SMTP_USER,
            to: process.env.NOTIFICATION_EMAIL,
            subject: '【新闻提交】有新的新闻待审核',
            html: `
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #333;">新闻提交通知</h2>
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>标题：</strong>${title}</p>
                        <p><strong>作者：</strong>${author || '匿名'}</p>
                        <p><strong>分类：</strong>${category || '未分类'}</p>
                        <p><strong>提交时间：</strong>${new Date().toLocaleString('zh-CN')}</p>
                        <hr>
                        <p><strong>内容预览：</strong></p>
                        <div style="border-left: 4px solid #007bff; padding-left: 15px;">
                            ${content.substring(0, 200)}${content.length > 200 ? '...' : ''}
                        </div>
                    </div>
                    <a href="http://localhost:3000/admin/news/${newsId}" 
                       style="display: inline-block; background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">
                        查看详情并审核
                    </a>
                </div>
            `
        };

        await transporter.sendMail(mailOptions);

        res.status(201).json({
            success: true,
            message: '新闻提交成功，等待审核',
            newsId: newsId
        });

    } catch (error) {
        console.error('新闻提交失败:', error);
        res.status(500).json({
            success: false,
            message: '提交失败，请稍后重试'
        });
    }
};

// 获取新闻列表
exports.getNewsList = async (req, res) => {
    try {
        const { page = 1, limit = 10, category, status = 'published' } = req.query;
        const offset = (page - 1) * limit;

        let query = 'SELECT * FROM news WHERE status = ?';
        let params = [status];

        if (category) {
            query += ' AND category = ?';
            params.push(category);
        }

        query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?';
        params.push(parseInt(limit), offset);

        const [rows] = await pool.execute(query, params);

        // 获取总数
        let countQuery = 'SELECT COUNT(*) as total FROM news WHERE status = ?';
        let countParams = [status];
        if (category) {
            countQuery += ' AND category = ?';
            countParams.push(category);
        }

        const [countResult] = await pool.execute(countQuery, countParams);
        const total = countResult[0].total;

        res.json({
            success: true,
            data: rows,
            pagination: {
                page: parseInt(page),
                limit: parseInt(limit),
                total: total,
                totalPages: Math.ceil(total / limit)
            }
        });

    } catch (error) {
        console.error('获取新闻列表失败:', error);
        res.status(500).json({
            success: false,
            message: '获取新闻列表失败'
        });
    }
};

// 获取单个新闻详情
exports.getNewsDetail = async (req, res) => {
    try {
        const { id } = req.params;

        const [rows] = await pool.execute(
            'SELECT * FROM news WHERE id = ?',
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                success: false,
                message: '新闻不存在'
            });
        }

        // 增加浏览次数
        await pool.execute(
            'UPDATE news SET views = views + 1 WHERE id = ?',
            [id]
        );

        res.json({
            success: true,
            data: rows[0]
        });

    } catch (error) {
        console.error('获取新闻详情失败:', error);
        res.status(500).json({
            success: false,
            message: '获取新闻详情失败'
        });
    }
};

// 发布新闻
exports.publishNews = async (req, res) => {
    try {
        const { id } = req.params;

        await pool.execute(
            'UPDATE news SET status = ?, published_at = NOW() WHERE id = ?',
            ['published', id]
        );

        res.json({
            success: true,
            message: '新闻已发布'
        });

    } catch (error) {
        console.error('发布新闻失败:', error);
        res.status(500).json({
            success: false,
            message: '发布新闻失败'
        });
    }
};

// 删除新闻
exports.deleteNews = async (req, res) => {
    try {
        const { id } = req.params;

        await pool.execute('DELETE FROM news WHERE id = ?', [id]);

        res.json({
            success: true,
            message: '新闻已删除'
        });

    } catch (error) {
        console.error('删除新闻失败:', error);
        res.status(500).json({
            success: false,
            message: '删除新闻失败'
        });
    }
};
```

#### routes/newsRoute.js
```javascript
const express = require('express');
const router = express.Router();
const newsController = require('../controllers/newsController');

// 公开路由
router.get('/news', newsController.getNewsList);
router.get('/news/:id', newsController.getNewsDetail);
router.post('/news/submit', newsController.submitNews);

// 管理员路由（需要添加认证中间件）
router.put('/admin/news/:id/publish', newsController.publishNews);
router.delete('/admin/news/:id', newsController.deleteNews);

module.exports = router;
```

#### public/news-submit.html
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>提交新闻</title>
    <link href="https://cdn.jsdelivr.net/npm/quill@2.0.0/dist/quill.snow.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 32px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }

        .required {
            color: #e74c3c;
        }

        input, select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        #editor {
            height: 300px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .message {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }

        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 提交新闻</h1>

        <div id="message" class="message"></div>

        <form id="newsForm">
            <div class="form-group">
                <label>新闻标题 <span class="required">*</span></label>
                <input type="text" id="title" required placeholder="请输入新闻标题">
            </div>

            <div class="form-group">
                <label>作者</label>
                <input type="text" id="author" placeholder="作者姓名（选填）">
            </div>

            <div class="form-group">
                <label>分类</label>
                <select id="category">
                    <option value="">选择分类</option>
                    <option value="公司新闻">公司新闻</option>
                    <option value="产品更新">产品更新</option>
                    <option value="行业资讯">行业资讯</option>
                </select>
            </div>

            <div class="form-group">
                <label>特色图片URL</label>
                <input type="url" id="featured_image" placeholder="https://example.com/image.jpg">
            </div>

            <div class="form-group">
                <label>新闻内容 <span class="required">*</span></label>
                <div id="editor"></div>
            </div>

            <button type="submit" class="btn">
                <span id="btnText">提交新闻</span>
            </button>
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/quill@2.0.0/dist/quill.js"></script>
    <script>
        // 初始化富文本编辑器
        var quill = new Quill('#editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'header': 1 }, { 'header': 2 }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'indent': '-1'}, { 'indent': '+1' }],
                    ['link', 'image'],
                    ['clean']
                ]
            }
        });

        const form = document.getElementById('newsForm');
        const messageDiv = document.getElementById('message');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitBtn = e.target.querySelector('.btn');
            const btnText = document.getElementById('btnText');
            
            submitBtn.disabled = true;
            btnText.textContent = '提交中...';

            // 获取富文本内容
            const content = quill.root.innerHTML;

            const formData = {
                title: document.getElementById('title').value,
                author: document.getElementById('author').value,
                category: document.getElementById('category').value,
                featured_image: document.getElementById('featured_image').value,
                content: content
            };

            try {
                const response = await fetch('/api/news/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (data.success) {
                    showMessage('success', '✅ 新闻提交成功！等待管理员审核。');
                    form.reset();
                    quill.setContents([]);
                } else {
                    showMessage('error', '❌ ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', '❌ 提交失败，请稍后重试');
            } finally {
                submitBtn.disabled = false;
                btnText.textContent = '提交新闻';
            }
        });

        function showMessage(type, text) {
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = text;
            messageDiv.style.display = 'block';

            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    </script>
</body>
</html>
```

---

## 4. 完整项目示例

### package.json
```json
{
  "name": "email-news-service",
  "version": "1.0.0",
  "description": "邮件和新闻服务完整实现",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "node test/email-test.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "nodemailer": "^6.9.7",
    "mysql2": "^3.6.5",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5",
    "body-parser": "^1.20.2",
    "multer": "^1.4.5-lts.1",
    "express-rate-limit": "^7.1.5",
    "helmet": "^7.1.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
```

### 启动项目
```bash
# 1. 安装依赖
npm install

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入真实配置

# 3. 创建数据库
mysql -u root -p < database.sql

# 4. 启动服务
npm run dev

# 5. 访问
# 联系表单: http://localhost:3000/contact.html
# 新闻提交: http://localhost:3000/news-submit.html
```

---

## 5. 生产环境部署

### 5.1 使用主流邮件服务商

#### Gmail 配置
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password  # 使用应用专用密码

# 获取Gmail应用密码步骤：
# 1. 访问 https://myaccount.google.com/security
# 2. 启用两步验证
# 3. 生成应用专用密码
```

#### SendGrid (国際推奨)
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-api-key

# 配置步骤：
# 1. 访问 https://sendgrid.com
# 2. 注册账号
# 3. 创建 API Key
# 4. 配置发信域名验证
```

#### 腾讯企业邮箱
```env
SMTP_HOST=smtp.exmail.qq.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=your-email@company.com
SMTP_PASS=your-password
```

#### SendGrid (国际推荐)
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
    to: 'recipient@example.com',
    from: 'sender@company.com',
    subject: 'Hello',
    html: '<strong>Email content</strong>',
};

sgMail.send(msg);
```

### 5.2 Docker 部署

#### Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      - db
    restart: always

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASS}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASS}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: always

volumes:
  mysql_data:
```

### 5.3 Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    
    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 静态文件
    location /static {
        alias /app/public;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API 请求
    location /api {
        proxy_pass http://web:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 其他请求
    location / {
        proxy_pass http://web:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5.4 安全增强

#### 添加安全中间件
```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// 安全头部
app.use(helmet());

// API 速率限制
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15分钟
    max: 100, // 最多100个请求
    message: '请求过于频繁，请稍后再试'
});

app.use('/api', apiLimiter);

// 联系表单特殊限制
const contactLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1小时
    max: 5, // 最多5次提交
    message: '提交次数过多，请1小时后再试'
});

app.use('/api/contact', contactLimiter);
```

### 5.5 监控和日志

#### PM2 部署
```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start server.js --name "email-service"

# 查看日志
pm2 logs email-service

# 监控
pm2 monit

# 开机自启
pm2 startup
pm2 save
```

#### ecosystem.config.js
```javascript
module.exports = {
    apps: [{
        name: 'email-news-service',
        script: './server.js',
        instances: 'max',
        exec_mode: 'cluster',
        env: {
            NODE_ENV: 'production',
            PORT: 3000
        },
        error_file: './logs/err.log',
        out_file: './logs/out.log',
        log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
        merge_logs: true
    }]
};
```

---

## 📚 总结

### 实现功能清单

✅ **邮件发送功能**
- 联系表单邮件通知
- 自动回复用户
- 新闻提交通知
- HTML 邮件模板

✅ **新闻管理功能**
- 新闻提交
- 新闻列表展示
- 新闻详情查看
- 新闻发布/删除
- 分类管理

✅ **数据存储**
- MySQL 数据库
- 联系记录保存
- 新闻内容管理

✅ **生产部署**
- Docker 容器化
- Nginx 反向代理
- SSL/HTTPS 配置
- PM2 进程管理
- 安全防护

### 成本估算

| 项目 | 方案 | 月费用 |
|------|------|--------|
| 邮件服务 | Gmail/企业邮箱 | ¥0-200 |
| 服务器 | Sakura VPS / AWS EC2 2核4G | ¥1,000-3,000 |
| 数据库 | MySQL (自建) | 包含在服务器 |
| 域名 | .com | ¥60/年 |
| SSL证书 | Let's Encrypt | 免费 |
| **总计** | - | **¥100-500/月** |

---

**文档创建时间**: 2026年1月6日
**适用场景**: 企业网站、新闻门户、内容管理系统
