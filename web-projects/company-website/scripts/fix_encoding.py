# -*- coding: utf-8 -*-
import codecs

# 修改 WEB_QUOTATION_STANDARD.md
with codecs.open('WEB_QUOTATION_STANDARD.md', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace('¥', '円')
content = content.replace('.com.cn', '.co.jp')  # 先替换长的
content = content.replace('.cn', '.jp')
content = content.replace('方案 A：', '')
content = content.replace('方案 B：', '')
content = content.replace('方案 C：', '')
content = content.replace('（方案A）', '（含后台）')
content = content.replace('（方案B）', '（含后台）')
content = content.replace('（方案C）', '（含后台）')

with codecs.open('WEB_QUOTATION_STANDARD.md', 'w', 'utf-8') as f:
    f.write(content)

print('WEB_QUOTATION_STANDARD.md updated successfully')

# 修改 ECOMMERCE_QUOTATION_TEMPLATE.md
with codecs.open('ECOMMERCE_QUOTATION_TEMPLATE.md', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace('¥', '円')
content = content.replace('.com.cn', '.co.jp')  # 先替换长的
content = content.replace(' / .cn', ' / .jp')
content = content.replace('方案 A：', '')
content = content.replace('方案 B：', '')

with codecs.open('ECOMMERCE_QUOTATION_TEMPLATE.md', 'w', 'utf-8') as f:
    f.write(content)

print('ECOMMERCE_QUOTATION_TEMPLATE.md updated successfully')
