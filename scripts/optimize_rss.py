#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS优化脚本
功能：简化RSS内容，移除冗余信息，减小文件大小
"""
import re
from datetime import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def optimize_rss():
    """优化RSS文件"""
    print("="*60)
    print("优化RSS订阅文件")
    print("="*60)
    
    rss_path = os.path.join(PROJECT_DIR, "rss.xml")
    
    if not os.path.exists(rss_path):
        print(f"❌ RSS文件不存在: {rss_path}")
        return False
    
    with open(rss_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取原始大小
    original_size = len(content)
    print(f"原始大小: {original_size} 字节")
    
    # 简化description：只保留分类和简短描述
    # 匹配description标签内容
    def simplify_description(match):
        desc = match.group(1)
        # 提取分类
        category_match = re.search(r'\[(.*?)\]', desc)
        category = category_match.group(1) if category_match else "资源"
        
        # 提取核心描述（前100字符）
        # 移除正文部分
        core_desc = re.sub(r'正文：.*', '', desc)
        core_desc = re.sub(r'分享者：.*?类型：.*?\s*', '', core_desc)
        core_desc = re.sub(r'标题：.*?\s*', '', core_desc)
        core_desc = core_desc.strip()
        
        # 限制长度
        if len(core_desc) > 150:
            core_desc = core_desc[:147] + "..."
        
        simplified = f"[{category}] {core_desc}"
        return f"<description>{simplified}</description>"
    
    # 替换所有description
    optimized_content = re.sub(
        r'<description>(.*?)</description>',
        simplify_description,
        content,
        flags=re.DOTALL
    )
    
    # 更新lastBuildDate
    current_time = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
    optimized_content = re.sub(
        r'<lastBuildDate>.*?</lastBuildDate>',
        f'<lastBuildDate>{current_time}</lastBuildDate>',
        optimized_content
    )
    
    # 保存优化后的RSS
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    # 获取优化后大小
    optimized_size = len(optimized_content)
    reduction = original_size - optimized_size
    reduction_percent = (reduction / original_size) * 100
    
    print(f"优化后大小: {optimized_size} 字节")
    print(f"减少: {reduction} 字节 ({reduction_percent:.1f}%)")
    print("✅ RSS优化完成")
    
    return True

def main():
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    optimize_rss()
    print("\n" + "="*60)
    print("RSS优化完成！")
    print("="*60)

if __name__ == "__main__":
    main()
