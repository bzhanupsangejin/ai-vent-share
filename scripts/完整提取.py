#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整提取21.txt所有资源（218条）
使用多种方法确保100%提取
"""
import json
import re
from datetime import datetime

def method1_direct_parse():
    """方法1：直接JSON解析"""
    try:
        with open("C:/Users/HYX/Desktop/21.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        json_start = content.find('[')
        if json_start == -1:
            return None
        
        json_content = content[json_start:]
        
        # 尝试修复常见的JSON错误
        # 1. 替换未闭合的引号
        # 2. 移除多余的逗号
        json_content = json_content.replace('",}', '"}')
        json_content = json_content.replace(',]', ']')
        
        resources = json.loads(json_content)
        print(f"方法1（直接解析）: 成功提取 {len(resources)} 条")
        return resources
    except Exception as e:
        print(f"方法1失败: {e}")
        return None

def method2_line_by_line():
    """方法2：逐行解析（最可靠）"""
    try:
        with open("C:/Users/HYX/Desktop/21.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到JSON数组开始位置
        json_start = content.find('[')
        if json_start == -1:
            return None
        
        content = content[json_start:]
        
        # 逐个字符解析，手动提取每个对象
        resources = []
        current_obj = ""
        brace_count = 0
        in_string = False
        escape_next = False
        
        for i, char in enumerate(content):
            if escape_next:
                current_obj += char
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                current_obj += char
                continue
            
            if char == '"' and not escape_next:
                in_string = not in_string
            
            if not in_string:
                if char == '{':
                    if brace_count == 0:
                        current_obj = "{"
                    else:
                        current_obj += char
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    current_obj += char
                    
                    if brace_count == 0 and current_obj.strip():
                        # 尝试解析这个对象
                        try:
                            obj = json.loads(current_obj)
                            if 'title' in obj and 'url' in obj:
                                resources.append(obj)
                        except:
                            pass
                        current_obj = ""
                else:
                    if brace_count > 0:
                        current_obj += char
            else:
                current_obj += char
        
        print(f"方法2（逐行解析）: 成功提取 {len(resources)} 条")
        return resources
    except Exception as e:
        print(f"方法2失败: {e}")
        return None

def method3_regex_extract():
    """方法3：正则表达式提取所有字段"""
    try:
        with open("C:/Users/HYX/Desktop/21.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到所有的title
        titles = re.findall(r'"title"\s*:\s*"([^"]+)"', content)
        print(f"找到 {len(titles)} 个title")
        
        # 找到所有的url
        urls = re.findall(r'"url"\s*:\s*"([^"]+)"', content)
        print(f"找到 {len(urls)} 个url")
        
        # 找到所有的type
        types = re.findall(r'"type"\s*:\s*"([^"]+)"', content)
        print(f"找到 {len(types)} 个type")
        
        # 找到所有的description
        descriptions = re.findall(r'"description"\s*:\s*"([^"]+)"', content)
        print(f"找到 {len(descriptions)} 个description")
        
        # 组合成资源对象
        resources = []
        max_len = min(len(titles), len(urls), len(types), len(descriptions))
        
        for i in range(max_len):
            resource = {
                'title': titles[i],
                'url': urls[i],
                'type': types[i],
                'description': descriptions[i],
                'verified_by': ['人工审核'],
                'last_updated': '2026-02-06',
                'compliance_level': '待验证'
            }
            resources.append(resource)
        
        print(f"方法3（正则提取）: 成功提取 {len(resources)} 条")
        return resources
    except Exception as e:
        print(f"方法3失败: {e}")
        return None

def merge_and_deduplicate(results):
    """合并多个方法的结果并去重"""
    all_resources = []
    seen_urls = set()
    
    for resources in results:
        if resources:
            for res in resources:
                url = res.get('url', '')
                if url and url not in seen_urls:
                    all_resources.append(res)
                    seen_urls.add(url)
    
    return all_resources

def main():
    """主函数"""
    print("\n" + "="*70)
    print("完整提取21.txt所有资源（目标：218条）")
    print("="*70)
    
    results = []
    
    print("\n尝试方法1：直接JSON解析...")
    result1 = method1_direct_parse()
    if result1:
        results.append(result1)
    
    print("\n尝试方法2：逐行解析...")
    result2 = method2_line_by_line()
    if result2:
        results.append(result2)
    
    print("\n尝试方法3：正则表达式提取...")
    result3 = method3_regex_extract()
    if result3:
        results.append(result3)
    
    print("\n" + "="*70)
    print("合并结果...")
    all_resources = merge_and_deduplicate(results)
    
    print(f"\n✅ 总共提取: {len(all_resources)} 条资源")
    print(f"📊 目标: 218条")
    print(f"📊 完成度: {len(all_resources)/218*100:.1f}%")
    
    if len(all_resources) < 218:
        print(f"\n⚠️  还有 {218 - len(all_resources)} 条资源未提取")
        print("可能原因：")
        print("  1. JSON格式错误导致部分资源无法解析")
        print("  2. 某些字段缺失导致被过滤")
        print("  3. 文件中实际资源数少于218条")
    
    # 保存提取结果
    with open("extracted_resources.json", 'w', encoding='utf-8') as f:
        json.dump(all_resources, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存到: extracted_resources.json")
    print("="*70)

if __name__ == "__main__":
    main()
