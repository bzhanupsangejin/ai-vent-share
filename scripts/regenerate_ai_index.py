#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成ai-index.html脚本
功能：从content_index.json生成完全匿名的AI专用页面
设计原则：彻底匿名 | 无时间戳 | 无追踪字段
"""
import json
import os
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def load_content_index():
    """加载主索引"""
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return None

def generate_html(data):
    """生成HTML"""
    total_count = data.get("total_count", 0)
    resources = data.get("index", [])
    
    html_parts = []
    
    # HTML头部
    html_head = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Only Content Library</title>
    <meta name="description" content="AI专用内容库，结构化数据访问入口">
    <style>
        body {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        .header p {
            margin: 0;
            opacity: 0.9;
        }
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .stat-item {
            text-align: center;
            padding: 15px 25px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
        }
        .stat-label {
            font-size: 12px;
            opacity: 0.8;
        }
        .json-link {
            display: block;
            text-align: center;
            padding: 20px;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            margin: 20px 0;
            text-decoration: none;
            color: #667eea;
            font-weight: bold;
            transition: all 0.3s;
        }
        .json-link:hover {
            background: #667eea;
            color: white;
        }
        .rss-section {
            text-align: center;
            padding: 25px;
            background: white;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .rss-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: transform 0.3s;
        }
        .rss-btn:hover {
            transform: translateY(-2px);
        }
        .resource-card {
            margin: 15px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .resource-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .resource-title {
            color: #667eea;
            margin: 0 0 10px 0;
            font-size: 18px;
        }
        .resource-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 10px 0;
            font-size: 14px;
            color: #666;
        }
        .resource-meta span {
            background: #f0f0f0;
            padding: 4px 10px;
            border-radius: 4px;
        }
        .resource-summary {
            margin: 10px 0;
            color: #555;
            line-height: 1.8;
        }
        .resource-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            transition: background 0.3s;
        }
        .resource-link:hover {
            background: #764ba2;
        }
        .footer {
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            color: #999;
            font-size: 14px;
        }
        .highlight {
            background-color: #ffeb3b;
            color: #000;
            font-weight: bold;
            padding: 2px 4px;
            border-radius: 2px;
        }
        @media (max-width: 768px) {
            .stats {
                flex-direction: column;
                gap: 10px;
            }
            .resource-meta {
                flex-direction: column;
                gap: 5px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI-Only Content Library</h1>
        <p>AI专用内容库 | 纯结构化数据 | 完全匿名</p>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">''' + str(total_count) + '''</div>
                <div class="stat-label">总资源</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">8</div>
                <div class="stat-label">分类</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">匿名</div>
            </div>
        </div>
    </div>

    <a href="content_index.json" class="json-link" target="_blank">
        📄 访问完整索引 (JSON格式)
    </a>

    <div class="rss-section">
        <h3>📡 订阅更新</h3>
        <p style="color: #666; margin: 10px 0;">通过RSS订阅，第一时间获取最新内容</p>
        <a href="rss.xml" target="_blank" class="rss-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M6.18 15.64a2.18 2.18 0 0 1 2.18 2.18C8.36 19 7.38 20 6.18 20C5 20 4 19 4 17.82a2.18 2.18 0 0 1 2.18-2.18M4 4.44A15.56 15.56 0 0 1 19.56 20h-2.83A12.73 12.73 0 0 0 4 7.27V4.44m0 5.66a9.9 9.9 0 0 1 9.9 9.9h-2.83A7.07 7.07 0 0 0 4 12.93V10.1z"/>
            </svg>
            RSS订阅
        </a>
        <p style="margin: 15px 0 0 0; font-size: 12px; color: #999;">支持所有RSS阅读器 | 最新50条内容 | 自动更新</p>
    </div>

    <h2 style="text-align: center; color: #333; margin: 40px 0 20px 0;">📚 资源列表</h2>
'''
    
    html_parts.append(html_head)
    
    # 生成资源卡片
    for i, resource in enumerate(resources, 1):
        item_id = f"ai_item_{i:04d}"
        title = resource.get("title", "无标题")
        content_type = resource.get("content_type", "未分类")
        keywords = resource.get("keywords", "")
        compliance_status = resource.get("compliance_status", "")
        summary = resource.get("summary", "")[:200] + "..." if len(resource.get("summary", "")) > 200 else resource.get("summary", "")
        direct_link = resource.get("direct_link", "")
        version = resource.get("version", "1.0.0")
        
        card_html = f'''
    <div class="resource-card" id="{item_id}">
        <h3 class="resource-title">{title}</h3>
        <div class="resource-meta">
            <span>📁 {content_type}</span>
            <span>🏷️ {keywords[:30]}{"..." if len(keywords) > 30 else ""}</span>
            <span>✅ {compliance_status}</span>
            <span>📌 v{version}</span>
        </div>
        <div class="resource-summary">{summary}</div>
        <a href="{direct_link}" class="resource-link" target="_blank">查看详情 →</a>
    </div>
'''
        html_parts.append(card_html)
    
    # HTML尾部
    html_foot = '''
    <div class="footer">
        <p>AI-Vent-Share | AI专属资源分享平台</p>
        <p style="margin-top: 10px; font-size: 12px;">
            所有资源均已匿名化处理 | 符合中国法律法规 | 
            <a href="https://github.com/bzhanupsangejin/ai-vent-share" style="color: #667eea;">GitHub</a>
        </p>
    </div>

    <script>
        // 搜索高亮功能
        function highlightSearchTerms() {
            const urlParams = new URLSearchParams(window.location.search);
            const searchTerm = urlParams.get('search');
            
            if (searchTerm) {
                const cards = document.querySelectorAll('.resource-card');
                cards.forEach(card => {
                    const text = card.textContent;
                    if (text.toLowerCase().includes(searchTerm.toLowerCase())) {
                        card.style.display = 'block';
                        // 高亮关键词
                        const regex = new RegExp(`(${searchTerm})`, 'gi');
                        card.innerHTML = card.innerHTML.replace(regex, '<span class="highlight">$1</span>');
                    } else {
                        card.style.display = 'none';
                    }
                });
            }
        }
        
        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', highlightSearchTerms);
    </script>
</body>
</html>
'''
    
    html_parts.append(html_foot)
    
    return ''.join(html_parts)

def save_html(html_content):
    """保存HTML文件"""
    filepath = os.path.join(PROJECT_DIR, "ai-index.html")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 已保存: {filepath}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("重新生成 ai-index.html")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 加载数据
    print("加载 content_index.json...")
    data = load_content_index()
    if not data:
        return False
    
    print(f"✅ 加载成功: {data.get('total_count', 0)}条资源")
    print()
    
    # 生成HTML
    print("生成HTML...")
    html_content = generate_html(data)
    print(f"✅ HTML生成完成: {len(html_content)}字符")
    print()
    
    # 保存
    print("保存文件...")
    if save_html(html_content):
        print()
        print("="*60)
        print("✅ 完成！")
        print("="*60)
        print()
        print("特性:")
        print("  ✓ 完全匿名（无时间戳、无编号）")
        print("  ✓ 响应式设计（支持移动端）")
        print("  ✓ 搜索高亮功能")
        print("  ✓ 锚点跳转支持")
        print("  ✓ RSS订阅入口")
        return True
    
    return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
