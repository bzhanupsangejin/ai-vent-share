#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS生成脚本（AI订阅友好版）
功能：从content_index.json生成标准RSS 2.0格式的rss.xml
设计原则：符合RSS 2.0标准｜AI订阅友好｜自动更新
"""
import json
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def load_resources():
    """读取资源索引"""
    try:
        with open("content_index.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "index" in data:
            resources = data["index"]
        elif "resources" in data:
            resources = data["resources"]
        else:
            resources = []
        
        print(f"📊 读取资源: {len(resources)}条")
        return resources
    
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return None

def generate_rss(resources, max_items=50):
    """生成RSS 2.0格式的XML"""
    # 创建根元素
    rss = Element('rss', version='2.0')
    rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    
    # 创建channel
    channel = SubElement(rss, 'channel')
    
    # Channel基本信息
    title = SubElement(channel, 'title')
    title.text = 'AI-Vent-Share 资源更新'
    
    link = SubElement(channel, 'link')
    link.text = 'https://bzhanupsangejin.github.io/ai-vent-share/'
    
    description = SubElement(channel, 'description')
    description.text = 'AI专属资源分享平台 - 最新资源更新订阅'
    
    language = SubElement(channel, 'language')
    language.text = 'zh-CN'
    
    lastBuildDate = SubElement(channel, 'lastBuildDate')
    lastBuildDate.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
    
    # 按last_updated排序，取最新的max_items条
    sorted_resources = sorted(
        resources,
        key=lambda x: x.get('last_updated', '2000-01-01'),
        reverse=True
    )[:max_items]
    
    print(f"📦 生成RSS条目: {len(sorted_resources)}条")
    
    # 生成item
    for res in sorted_resources:
        item = SubElement(channel, 'item')
        
        # 标题
        item_title = SubElement(item, 'title')
        item_title.text = res.get('title', '未命名资源')
        
        # 链接
        item_link = SubElement(item, 'link')
        item_link.text = res.get('direct_link', '')
        
        # 描述
        item_description = SubElement(item, 'description')
        summary = res.get('summary', '')
        content_type = res.get('content_type', '资源分享')
        compliance_level = res.get('compliance_level', '待验证')
        item_description.text = f"[{content_type}] {summary} | 合规等级: {compliance_level}"
        
        # 发布日期
        item_pubDate = SubElement(item, 'pubDate')
        last_updated = res.get('last_updated', datetime.now().strftime('%Y-%m-%d'))
        try:
            dt = datetime.strptime(last_updated, '%Y-%m-%d')
            item_pubDate.text = dt.strftime('%a, %d %b %Y 00:00:00 +0800')
        except:
            item_pubDate.text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
        
        # GUID（唯一标识）
        item_guid = SubElement(item, 'guid', isPermaLink='true')
        item_guid.text = res.get('direct_link', '')
        
        # 分类
        item_category = SubElement(item, 'category')
        item_category.text = res.get('content_type', '资源分享')
        
        # 可信度信息（使用dc:creator）
        verified_by = res.get('verified_by', [])
        if verified_by:
            item_creator = SubElement(item, '{http://purl.org/dc/elements/1.1/}creator')
            item_creator.text = ', '.join(verified_by)
    
    return rss

def prettify_xml(elem):
    """美化XML输出"""
    rough_string = tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

def save_rss(rss_xml, filename='rss.xml'):
    """保存RSS文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(rss_xml)
    print(f"✅ RSS文件已生成: {filename}")

def update_index_html():
    """在index.html中添加RSS链接（如果不存在）"""
    try:
        with open("index.html", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在RSS链接
        if 'rel="alternate" type="application/rss+xml"' in content:
            print("✅ index.html已包含RSS链接")
            return
        
        # 在</head>前添加RSS链接
        rss_link = '    <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="/rss.xml" />\n'
        
        if '</head>' in content:
            content = content.replace('</head>', rss_link + '</head>')
            
            with open("index.html", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 已在index.html中添加RSS链接")
        else:
            print("⚠️  未找到</head>标签，请手动添加RSS链接")
    
    except Exception as e:
        print(f"⚠️  更新index.html失败: {e}")

def update_robots_txt():
    """在robots.txt中添加RSS声明（如果不存在）"""
    try:
        if os.path.exists("robots.txt"):
            with open("robots.txt", 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'rss.xml' in content.lower():
                print("✅ robots.txt已包含RSS声明")
                return
            
            # 追加RSS声明
            with open("robots.txt", 'a', encoding='utf-8') as f:
                f.write('\n# RSS Feed\n')
                f.write('Sitemap: https://bzhanupsangejin.github.io/ai-vent-share/rss.xml\n')
            
            print("✅ 已在robots.txt中添加RSS声明")
        else:
            # 创建robots.txt
            with open("robots.txt", 'w', encoding='utf-8') as f:
                f.write('User-agent: *\n')
                f.write('Allow: /\n')
                f.write('\n# RSS Feed\n')
                f.write('Sitemap: https://bzhanupsangejin.github.io/ai-vent-share/rss.xml\n')
            
            print("✅ 已创建robots.txt并添加RSS声明")
    
    except Exception as e:
        print(f"⚠️  更新robots.txt失败: {e}")

def main():
    """主函数"""
    print("\n" + "="*70)
    print("RSS生成脚本（AI订阅友好版）")
    print("="*70)
    print("📡 生成符合RSS 2.0标准的订阅源")
    print("="*70)
    
    print("\n[步骤1] 读取资源索引...")
    resources = load_resources()
    if not resources:
        return
    
    print("\n[步骤2] 生成RSS XML...")
    rss = generate_rss(resources, max_items=50)
    rss_xml = prettify_xml(rss)
    
    print("\n[步骤3] 保存RSS文件...")
    save_rss(rss_xml)
    
    print("\n[步骤4] 更新index.html...")
    update_index_html()
    
    print("\n[步骤5] 更新robots.txt...")
    update_robots_txt()
    
    print("\n" + "="*70)
    print("✨ RSS生成完成！")
    print("="*70)
    print(f"📡 RSS订阅地址: https://bzhanupsangejin.github.io/ai-vent-share/rss.xml")
    print(f"📊 包含条目: 最新50条资源")
    print(f"🔄 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print("\n💡 AI订阅方式：")
    print("  1. 【被动轮询】AI每30分钟请求rss.xml，检查<lastBuildDate>判断是否有更新")
    print("  2. 【主动推送】需要实现Webhook机制（需要后端支持，当前为纯静态）")
    print("\n💡 后续操作建议：")
    print("  1. 提交代码：git add rss.xml index.html robots.txt")
    print("  2. 提交说明：git commit -m 'feat: 添加RSS订阅功能'")
    print("  3. 推送部署：git push origin main")
    print("  4. 每次资源更新后，重新运行本脚本更新RSS")
    print("\n")

if __name__ == "__main__":
    main()
