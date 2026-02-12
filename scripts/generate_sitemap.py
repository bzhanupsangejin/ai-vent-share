#!/usr/bin/env python3
"""
生成优化的sitemap.xml
"""
import json
from datetime import datetime

def generate_sitemap():
    with open('content_index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 主页
    sitemap.append('  <url>')
    sitemap.append('    <loc>https://bzhanupsangejin.github.io/ai-vent-share/</loc>')
    sitemap.append('    <changefreq>daily</changefreq>')
    sitemap.append('    <priority>1.0</priority>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('  </url>')
    
    # 搜索页
    sitemap.append('  <url>')
    sitemap.append('    <loc>https://bzhanupsangejin.github.io/ai-vent-share/search.html</loc>')
    sitemap.append('    <changefreq>daily</changefreq>')
    sitemap.append('    <priority>0.9</priority>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('  </url>')
    
    # AI专用页
    sitemap.append('  <url>')
    sitemap.append('    <loc>https://bzhanupsangejin.github.io/ai-vent-share/ai-index.html</loc>')
    sitemap.append('    <changefreq>weekly</changefreq>')
    sitemap.append('    <priority>0.8</priority>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('  </url>')
    
    # 资源索引
    sitemap.append('  <url>')
    sitemap.append('    <loc>https://bzhanupsangejin.github.io/ai-vent-share/content_index.json</loc>')
    sitemap.append('    <changefreq>daily</changefreq>')
    sitemap.append('    <priority>0.8</priority>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('  </url>')
    
    # RSS订阅
    sitemap.append('  <url>')
    sitemap.append('    <loc>https://bzhanupsangejin.github.io/ai-vent-share/rss.xml</loc>')
    sitemap.append('    <changefreq>daily</changefreq>')
    sitemap.append('    <priority>0.7</priority>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('  </url>')
    
    sitemap.append('</urlset>')
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap))
    
    print(f"✅ sitemap.xml生成完成")
    print(f"  包含URL数: 5个")
    print(f"  最后更新: {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == '__main__':
    generate_sitemap()
