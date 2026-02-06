#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schema校验和索引增强脚本
功能：为现有content_index.json添加Schema标准化字段
"""
import json
import uuid
import os

# 内联配置
REQUIRED_FIELDS = [
    "content_id", "uuid", "title", "content_type", 
    "summary", "direct_link",
    "compliance_hash", "version", "trace_id"
]

FIELD_DEFAULT_VALUES = {
    "compliance_hash": "pending",
    "version": "1.0.0",
    "trace_id": "default"
}


def validate_schema(item: dict, index: int) -> dict:
    """校验并补全字段，保证符合标准化Schema"""
    # 确保content_id存在
    if "content_id" not in item:
        item["content_id"] = item.get("content_id", f"ai_item_{index:04d}")
    
    # 生成UUID（如果不存在）
    if "uuid" not in item or not item["uuid"]:
        item["uuid"] = str(uuid.uuid4())
    
    # 生成trace_id（如果不存在）
    if "trace_id" not in item or not item["trace_id"]:
        item["trace_id"] = f"trace_{item['uuid'][:8]}"
    
    # 确保version存在
    if "version" not in item or not item["version"]:
        item["version"] = "1.0.0"
    
    # 确保compliance_hash存在
    if "compliance_hash" not in item or not item["compliance_hash"]:
        item["compliance_hash"] = "pending"
    
    # 补全其他缺失字段
    for field in REQUIRED_FIELDS:
        if field not in item or item[field] is None or item[field] == "":
            item[field] = FIELD_DEFAULT_VALUES.get(field, "")
    
    return item


def enhance_index():
    """增强现有索引文件"""
    print("=" * 60)
    print("Schema标准化增强脚本")
    print("=" * 60)
    print()
    
    # 读取现有索引
    index_file = "content_index.json"
    if not os.path.exists(index_file):
        print(f"❌ 错误：{index_file} 文件不存在")
        return
    
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ 成功读取索引文件")
        print(f"   总条目数: {data.get('total_count', 0)}")
    except json.JSONDecodeError:
        print("❌ 错误：JSON格式错误")
        return
    print()
    
    # 处理每个条目
    enhanced_count = 0
    items = data.get("index", [])
    
    for i, item in enumerate(items):
        original_keys = set(item.keys())
        item = validate_schema(item, i + 1)
        new_keys = set(item.keys())
        
        if new_keys != original_keys:
            enhanced_count += 1
    
    # 更新索引
    data["index"] = items
    
    # 添加Schema元信息
    if "schema_version" not in data:
        data["schema_version"] = "1.0.0"
    if "schema_url" not in data:
        data["schema_url"] = "./static/schema/resource_schema.json"
    
    # 保存增强后的索引
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print("增强统计")
    print("=" * 60)
    print(f"增强条目数: {enhanced_count}")
    print(f"总条目数: {len(items)}")
    print()
    print("✅ Schema标准化完成")
    print(f"✅ 已保存到: {index_file}")
    print()


if __name__ == "__main__":
    enhance_index()
