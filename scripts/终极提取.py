#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极提取脚本 - 处理所有边界情况
"""
import json
import re

def clean_json_string(content):
    """清理JSON字符串"""
    # 移除Windows换行符
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')
    
    # 移除多余的空白
    content = re.sub(r'\n\s*\n', '\n', content)
    
    return content

def extract_all_by_pattern():
    """使用模式匹配提取所有资源"""
    try:
        with open("C:/Users/HYX/Desktop/21.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = clean_json_string(content)
        
        # 找到JSON数组部分
        json_start = content.find('[')
        if json_start == -1:
            return []
        
        content = content[json_start:]
        
        # 使用更宽松的正则表达式匹配每个对象
        # 匹配 {...} 包括可能跨多行的内容
        pattern = r'\{[^{}]*?"title"[^{}]*?"type"[^{}]*?"url"[^{}]*?"description"[^{}]*?\}'
        
        # 先尝试简单匹配
        matches = re.findall(pattern, content, re.DOTALL)
        
        resources = []
        for match in matches:
            try:
                # 清理匹配的字符串
                match = match.strip()
                obj = json.loads(match)
                if 'title' in obj and 'url' in obj:
                    resources.append(obj)
            except:
                # 如果解析失败，尝试手动提取字段
                try:
                    title_match = re.search(r'"title"\s*:\s*"([^"]+)"', match)
                    url_match = re.search(r'"url"\s*:\s*"([^"]+)"', match)
                    type_match = re.search(r'"type"\s*:\s*"([^"]+)"', match)
                    desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', match)
                    
                    if title_match and url_match:
                        resource = {
                            'title': title_match.group(1),
                            'url': url_match.group(1),
                            'type': type_match.group(1) if type_match else '资源分享',
                            'description': desc_match.group(1) if desc_match else '',
                            'verified_by': ['人工审核'],
                            'last_updated': '2026-02-06',
                            'compliance_level': '待验证'
                        }
                        resources.append(resource)
                except:
                    pass
        
        print(f"模式匹配提取: {len(resources)}条")
        return resources
    except Exception as e:
        print(f"模式匹配失败: {e}")
        return []

def extract_by_splitting():
    """通过分割提取"""
    try:
        with open("C:/Users/HYX/Desktop/21.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = clean_json_string(content)
        
        # 找到JSON数组部分
        json_start = content.find('[')
        json_end = content.rfind(']')
        
        if json_start == -1 or json_end == -1:
            return []
        
        json_content = content[json_start+1:json_end]
        
        # 按 },{ 分割
        parts = re.split(r'\},\s*\{', json_content)
        
        resources = []
        for i, part in enumerate(parts):
            # 补全大括号
            if not part.strip().startswith('{'):
                part = '{' + part
            if not part.strip().endswith('}'):
                part = part + '}'
            
            try:
                obj = json.loads(part)
                if 'title' in obj and 'url' in obj:
                    # 补充缺失字段
                    obj.setdefault('type', '资源分享')
                    obj.setdefault('description', '')
                    obj.setdefault('verified_by', ['人工审核'])
                    obj.setdefault('last_updated', '2026-02-06')
                    obj.setdefault('compliance_level', '待验证')
                    resources.append(obj)
            except:
                # 手动提取
                try:
                    title_match = re.search(r'"title"\s*:\s*"([^"]+)"', part)
                    url_match = re.search(r'"url"\s*:\s*"([^"]+)"', part)
                    type_match = re.search(r'"type"\s*:\s*"([^"]+)"', part)
                    desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', part)
                    
                    if title_match and url_match:
                        resource = {
                            'title': title_match.group(1),
                            'url': url_match.group(1),
                            'type': type_match.group(1) if type_match else '资源分享',
                            'description': desc_match.group(1) if desc_match else '',
                            'verified_by': ['人工审核'],
                            'last_updated': '2026-02-06',
                            'compliance_level': '待验证'
                        }
                        resources.append(resource)
                except:
                    pass
        
        print(f"分割提取: {len(resources)}条")
        return resources
    except Exception as e:
        print(f"分割提取失败: {e}")
        return []

def main():
    """主函数"""
    print("\n" + "="*70)
    print("终极提取 - 目标218条资源")
    print("="*70)
    
    all_resources = []
    seen_urls = set()
    
    print("\n方法1: 模式匹配...")
    resources1 = extract_all_by_pattern()
    for res in resources1:
        url = res.get('url', '')
        if url and url not in seen_urls:
            all_resources.append(res)
            seen_urls.add(url)
    
    print("\n方法2: 分割提取...")
    resources2 = extract_by_splitting()
    for res in resources2:
        url = res.get('url', '')
        if url and url not in seen_urls:
            all_resources.append(res)
            seen_urls.add(url)
    
    print("\n" + "="*70)
    print(f"✅ 总共提取: {len(all_resources)}条")
    print(f"📊 目标: 218条")
    print(f"📊 完成度: {len(all_resources)/218*100:.1f}%")
    print("="*70)
    
    # 保存
    with open("all_extracted.json", 'w', encoding='utf-8') as f:
        json.dump(all_resources, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存到: all_extracted.json")
    
    # 显示前5条
    print("\n前5条资源:")
    for i, res in enumerate(all_resources[:5], 1):
        print(f"{i}. {res.get('title', 'N/A')}")

if __name__ == "__main__":
    main()
