#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入extracted_resources.json中的资源
"""
import json
import os
from datetime import datetime

def load_extracted_resources():
    """读取提取的资源"""
    try:
        with open("extracted_resources.json", 'r', encoding='utf-8') as f:
            resources = json.load(f)
        print(f"✅ 读取提取的资源: {len(resources)}条")
        return resources
    except Exception as e:
        print(f"❌ 读取失败: {e}")
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
        "summary": new_resource.get("description", "")[:200],
        "direct_link": new_resource.get("url", ""),
        "verified_by": new_resource.get("verified_by", ["人工审核"]),
        "last_updated": new_resource.get("last_updated", datetime.now().strftime("%Y-%m-%d")),
        "compliance_level": new_resource.get("compliance_level", "待验证"),
        "keywords": "",
        "compliance_status": "通过",
        "version": "1.0.0",
        "compliance_hash": "batch_import_完整",
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
    print("导入extracted_resources.json中的资源")
    print("="*70)
    
    print("\n[步骤1] 读取提取的资源...")
    new_resources = load_extracted_resources()
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
    print("✨ 导入完成！")
    print("="*70)
    print(f"📊 原有资源: {len(existing_resources)}条")
    print(f"📊 新增资源: {len(merged_resources) - len(existing_resources)}条")
    print(f"📊 总资源数: {len(merged_resources)}条")
    print("="*70)
    print("\n💡 后续操作：")
    print("  python scripts/optimize_anonymous.py")
    print("\n")

if __name__ == "__main__":
    main()
