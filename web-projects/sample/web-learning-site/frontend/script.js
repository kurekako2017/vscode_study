// --- 自动化渲染 news.json 新闻内容 ---
document.addEventListener('DOMContentLoaded', function () {
    fetch('news.json')
        .then(response => response.json())
        .then(newsList => {
            const newsContainer = document.querySelector('.news-list');
            if (!newsContainer) return;
            newsList.forEach(item => {
                const article = document.createElement('article');
                article.className = 'news-item';
                article.innerHTML = `
                    <time class="news-date">${item.date}</time>
                    <h3 class="news-title">
                        <a href="${item.link}" target="_blank" rel="noopener noreferrer">${item.title}</a>
                    </h3>
                    <p class="news-summary">${item.summary}</p>
                `;
                newsContainer.appendChild(article);
            });
        });
});
// モバイルメニュー切り替え
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// メニューリンククリック時にメニューを閉じる（モバイル）
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            navMenu.classList.remove('active');
        }
    });
});

// スムーススクロール（古いブラウザ対応）
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 70; // ナビバーの高さ分調整
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// フォーム送信処理
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // フォームデータ取得
        const formData = {
            name: document.getElementById('name').value,
            company: document.getElementById('company').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            message: document.getElementById('message').value,
            timestamp: new Date().toISOString()
        };

        // 簡易バリデーション
        if (!formData.name || !formData.email || !formData.message) {
            showMessage('必須項目を入力してください。', 'error');
            return;
        }

        // メールアドレス形式チェック
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            showMessage('有効なメールアドレスを入力してください。', 'error');
            return;
        }

        // 送信ボタン無効化
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = '送信中...';

        try {
            // デモ用：コンソールにデータ表示（実際はここでAPIにPOST）
            console.log('送信データ:', formData);
            
            // 実際のバックエンド実装例：
            // const response = await fetch('/api/contact', {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify(formData)
            // });
            // if (!response.ok) throw new Error('送信失敗');

            // デモ用：2秒待機してから成功表示
            await new Promise(resolve => setTimeout(resolve, 2000));

            showMessage('お問い合わせを受け付けました。担当者より折り返しご連絡いたします。', 'success');
            contactForm.reset();

        } catch (error) {
            console.error('送信エラー:', error);
            showMessage('送信に失敗しました。しばらく経ってから再度お試しください。', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '送信する';
        }
    });
}

// メッセージ表示関数
function showMessage(message, type) {
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
    formMessage.style.display = 'block';
    
    // 5秒後に非表示
    setTimeout(() => {
        formMessage.style.display = 'none';
    }, 5000);
}

// スクロール時のナビバー背景変更（オプション）
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
    
    lastScroll = currentScroll;
});

// ページ読み込み時のアニメーション（オプション）
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});
