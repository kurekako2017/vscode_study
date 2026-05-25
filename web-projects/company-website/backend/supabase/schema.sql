-- 数据库架构设计
-- 使用 Supabase PostgreSQL

-- ============================================
-- 1. 新闻表 (news)
-- ============================================
CREATE TABLE IF NOT EXISTS news (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    cover_image_url TEXT,
    category VARCHAR(50) DEFAULT 'general',
    tags TEXT[],
    author_id UUID REFERENCES auth.users(id),
    published_at TIMESTAMP WITH TIME ZONE,
    is_published BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 新闻表索引
CREATE INDEX idx_news_slug ON news(slug);
CREATE INDEX idx_news_published ON news(is_published, published_at DESC);
CREATE INDEX idx_news_category ON news(category);

-- ============================================
-- 2. 联系表单提交表 (contact_submissions)
-- ============================================
CREATE TABLE IF NOT EXISTS contact_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new', -- new, read, replied, archived
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    replied_at TIMESTAMP WITH TIME ZONE
);

-- 联系表单索引
CREATE INDEX idx_contact_status ON contact_submissions(status, created_at DESC);
CREATE INDEX idx_contact_email ON contact_submissions(email);

-- ============================================
-- 3. 新闻订阅表 (newsletter_subscribers)
-- ============================================
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    confirmed_at TIMESTAMP WITH TIME ZONE,
    unsubscribed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 订阅表索引
CREATE INDEX idx_newsletter_email ON newsletter_subscribers(email);
CREATE INDEX idx_newsletter_active ON newsletter_subscribers(is_active);

-- ============================================
-- 4. 管理员用户扩展表 (admin_profiles)
-- ============================================
CREATE TABLE IF NOT EXISTS admin_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    display_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'editor', -- admin, editor, viewer
    avatar_url TEXT,
    bio TEXT,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 5. 系统日志表 (activity_logs)
-- ============================================
CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    action VARCHAR(50) NOT NULL, -- create, update, delete, login
    resource_type VARCHAR(50), -- news, contact, user
    resource_id UUID,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 日志索引
CREATE INDEX idx_logs_user ON activity_logs(user_id, created_at DESC);
CREATE INDEX idx_logs_resource ON activity_logs(resource_type, resource_id);

-- ============================================
-- 触发器：自动更新 updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_news_updated_at 
    BEFORE UPDATE ON news
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Row Level Security (RLS) 策略
-- ============================================

-- 启用 RLS
ALTER TABLE news ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_profiles ENABLE ROW LEVEL SECURITY;

-- 新闻表策略
-- 公开访问已发布的新闻
CREATE POLICY "Anyone can view published news" 
    ON news FOR SELECT 
    USING (is_published = true);

-- 管理员可以管理所有新闻
CREATE POLICY "Admins can manage news" 
    ON news FOR ALL 
    USING (auth.jwt() ->> 'role' = 'admin');

-- 联系表单策略
-- 任何人可以创建提交
CREATE POLICY "Anyone can submit contact form" 
    ON contact_submissions FOR INSERT 
    WITH CHECK (true);

-- 管理员可以查看所有提交
CREATE POLICY "Admins can view all submissions" 
    ON contact_submissions FOR SELECT 
    USING (auth.jwt() ->> 'role' = 'admin');

-- ============================================
-- 初始数据
-- ============================================

-- 插入示例新闻分类
INSERT INTO news (title, slug, summary, content, category, is_published, published_at) VALUES
('欢迎访问我们的网站', 'welcome', '这是我们的第一篇新闻', '欢迎访问我们的公司网站，这里将定期发布公司最新动态和行业资讯。', 'announcement', true, NOW()),
('公司成立十周年', 'company-10th-anniversary', '感谢一路相伴', '在这个特殊的日子里，我们迎来了公司成立十周年的重要时刻...', 'company', true, NOW()),
('新产品发布会预告', 'new-product-launch', '敬请期待', '我们将于下月举办新产品发布会，届时将展示我们最新的技术成果...', 'product', true, NOW());
