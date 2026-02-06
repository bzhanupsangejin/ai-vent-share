#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入资源脚本（终极版）
功能：从new_resources.txt批量导入资源，使用正则表达式逐条提取
设计原则：严格匿名｜合规优先｜强大容错
"""
import json
import os
import re
from datetime import datetime

def extract_resources_regex():
    """使用正则表达式逐条提取资源"""
    try:
        with open("new_resources.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取每个资源对象
        # 匹配模式：{"title":"...","type":"...","url":"...","description":"...","verified_by":[...],"last_updated":"...","compliance_level":"..."}
        pattern = r'\{[^{}]*?"title"[^{}]*?\}'
        matches = re.findall(pattern, content)
        
        resources = []
        for match in matches:
            try:
                # 尝试解析每个匹配的对象
                obj = json.loads(match)
                if "title" in obj and "url" in obj:
                    resources.append(obj)
            except:
                continue
        
        if resources:
            print(f"✅ 正则提取成功，读取 {len(resources)} 条资源")
            return resources
        else:
            print("❌ 正则提取失败，尝试手动解析...")
            return manual_parse(content)
    
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return None

def manual_parse(content):
    """手动解析（最后的手段）"""
    # 提取JSON数组部分
    json_start = content.find('[')
    if json_start == -1:
        return None
    
    json_content = content[json_start:]
    
    # 逐行处理，提取关键信息
    resources = []
    lines = json_content.split('\n')
    
    current_resource = {}
    for line in lines:
        line = line.strip()
        
        # 提取title
        if '"title"' in line:
            match = re.search(r'"title"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['title'] = match.group(1)
        
        # 提取type
        if '"type"' in line:
            match = re.search(r'"type"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['type'] = match.group(1)
        
        # 提取url
        if '"url"' in line:
            match = re.search(r'"url"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['url'] = match.group(1)
        
        # 提取description
        if '"description"' in line:
            match = re.search(r'"description"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['description'] = match.group(1)
        
        # 提取verified_by
        if '"verified_by"' in line:
            match = re.search(r'"verified_by"\s*:\s*\[([^\]]*)\]', line)
            if match:
                verified_str = match.group(1)
                current_resource['verified_by'] = [v.strip('"') for v in verified_str.split(',')]
        
        # 提取last_updated
        if '"last_updated"' in line:
            match = re.search(r'"last_updated"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['last_updated'] = match.group(1)
        
        # 提取compliance_level
        if '"compliance_level"' in line:
            match = re.search(r'"compliance_level"\s*:\s*"([^"]*)"', line)
            if match:
                current_resource['compliance_level'] = match.group(1)
        
        # 如果遇到对象结束，保存当前资源
        if line.endswith('},') or line.endswith('}'):
            if 'title' in current_resource and 'url' in current_resource:
                resources.append(current_resource.copy())
            current_resource = {}
    
    if resources:
        print(f"✅ 手动解析成功，读取 {len(resources)} 条资源")
        return resources
    else:
        return None

def load_main_index():
    """读取主索引"""
    try:
        with open("content_index.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "index" in data:
            resources = data["index"]
        elif "resources" in data:
            resources = data["resources"]
        else:
            resources = []
        
        print(f"📊 当前资源数: {len(resources)}条")
        return data, resources
    
    except Exception as e:
        print(f"❌ 读取主索引失败: {e}")
        return None, None

def convert_to_standard_format(new_resource, index):
    """转换为标准格式（匿名性强化）"""
    standard_resource = {
        "title": new_resource.get("title", ""),
        "content_type": new_resource.get("type", "资源分享"),
        "summary": new_resource.get("description", ""),
        "direct_link": new_resource.get("url", ""),
        "verified_by": new_resource.get("verified_by", []),
        "last_updated": new_resource.get("last_updated", datetime.now().strftime("%Y-%m-%d")),
        "compliance_level": new_resource.get("compliance_level", "待验证"),
        "keywords": "",
        "compliance_status": "通过",
        "version": "1.0.0",
        "compliance_hash": "batch_import",
        "content_id": f"ai_item_{index:04d}",
        "full_content_anchor": f"ai_item_{index:04d}"
    }
    
    return standard_resource

def merge_resources(existing_resources, new_resources):
    """合并资源（去重）"""
    existing_urls = {r.get("direct_link", r.get("url", "")) for r in existing_resources}
    
    merged = existing_resources.copy()
    added_count = 0
    duplicate_count = 0
    
    for new_res in new_resources:
        url = new_res.get("url", "")
        if url and url not in existing_urls:
            standard_res = convert_to_standard_format(new_res, len(merged) + 1)
            merged.append(standard_res)
            existing_urls.add(url)
            added_count += 1
        else:
            duplicate_count += 1
    
    print(f"✅ 新增资源: {added_count}条")
    if duplicate_count > 0:
        print(f"⚠️  重复跳过: {duplicate_count}条")
    
    return merged

def save_main_index(data, resources):
    """保存主索引"""
    backup_path = "content_index.json.bak"
    if os.path.exists("content_index.json"):
        with open("content_index.json", 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        print(f"💾 已备份原文件: {backup_path}")
    
    if "index" in data:
        data["index"] = resources
    elif "resources" in data:
        data["resources"] = resources
    
    data["total_count"] = len(resources)
    
    with open("content_index.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 主索引已更新: {len(resources)}条资源")

def main():
    """主函数"""
    print("\n" + "="*70)
    print("批量导入资源脚本（终极版）")
    print("="*70)
    print("🔒 匿名性保障：不生成任何可追踪字段")
    print("="*70)
    
    print("\n[步骤1] 读取新资源...")
    new_resources = extract_resources_regex()
    if not new_resources:
        return
    
    print("\n[步骤2] 读取主索引...")
    data, existing_resources = load_main_index()
    if data is None:
        return
    
    print("\n[步骤3] 合并资源（去重）...")
    merged_resources = merge_resources(existing_resources, new_resources)
    
    print("\n[步骤4] 保存主索引...")
    save_main_index(data, merged_resources)
    
    print("\n" + "="*70)
    print("✨ 批量导入完成！")
    print("="*70)
    print(f"📊 原有资源: {len(existing_resources)}条")
    print(f"📊 新增资源: {len(merged_resources) - len(existing_resources)}条")
    print(f"📊 总资源数: {len(merged_resources)}条")
    print("="*70)
    print("\n💡 后续操作建议：")
    print("  1. 【必须】运行匿名优化脚本：python scripts/optimize_anonymous.py")
    print("  2. 提交代码：git add . && git commit -m 'add: 批量导入资源' && git push")
    print("\n")

if __name__ == "__main__":
    main()
