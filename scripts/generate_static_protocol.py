#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态机器交互协议生成脚本
功能：生成分类索引、哈希索引、轻量清单
"""
import json
import os

# 配置
INDEX_FILE = "content_index.json"
OUTPUT_DIR = "./static/indexes"

# 合法类型
VALID_CONTENT_TYPES = [
    "AI工具", "代码模板", "FAQ文档", "免费API",
    "技术教程", "资源分享", "部署指南", "合规说明"
]


def generate_static_protocol():
    """生成静态机器交互协议"""
    print("=" * 60)
    print("静态机器交互协议生成")
    print("=" * 60)
    print()
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 读取主索引
    if not os.path.exists(INDEX_FILE):
        print(f"❌ 错误：{INDEX_FILE} 文件不存在")
        return
    
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    contents = data.get("index", [])
    print(f"✅ 读取主索引: {len(contents)} 条")
    print()
    
    # 1. 生成分类索引（AI按类型拉取）
    print("【生成分类索引】")
    for type_name in VALID_CONTENT_TYPES:
        filtered = [i for i in contents if i.get("content_type") == type_name]
        output_file = f"{OUTPUT_DIR}/{type_name}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "content_type": type_name,
                "total": len(filtered),
                "items": filtered
            }, f, ensure_ascii=False, indent=2)
        print(f"  ✅ {type_name}.json ({len(filtered)} 条)")
    print()
    
    # 2. 生成轻量清单（仅ID+链接，极低算力开销）
    print("【生成轻量清单】")
    lightweight = [{
        "uuid": i.get("uuid", ""),
        "content_id": i.get("content_id", ""),
        "direct_link": i.get("direct_link", ""),
        "content_type": i.get("content_type", "")
    } for i in contents]
    
    with open(f"{OUTPUT_DIR}/lightweight_manifest.json", "w", encoding="utf-8") as f:
        json.dump({
            "total": len(lightweight),
            "items": lightweight
        }, f, ensure_ascii=False, indent=2)
    print(f"  ✅ lightweight_manifest.json ({len(lightweight)} 条)")
    print()
    
    # 3. 生成UUID哈希索引（O(1)查询）
    print("【生成哈希索引】")
    hash_map = {item.get("uuid", ""): item for item in contents if item.get("uuid")}
    with open(f"{OUTPUT_DIR}/uuid_hash_index.json", "w", encoding="utf-8") as f:
        json.dump(hash_map, f, ensure_ascii=False, indent=2)
    print(f"  ✅ uuid_hash_index.json ({len(hash_map)} 条)")
    print()
    
    # 4. 生成content_id哈希索引
    id_map = {item.get("content_id", ""): item for item in contents if item.get("content_id")}
    with open(f"{OUTPUT_DIR}/id_hash_index.json", "w", encoding="utf-8") as f:
        json.dump(id_map, f, ensure_ascii=False, indent=2)
    print(f"  ✅ id_hash_index.json ({len(id_map)} 条)")
    print()
    
    print("=" * 60)
    print("✅ 静态机器交互协议生成完成")
    print("=" * 60)
    print()
    print("📋 生成文件清单：")
    print(f"   - 8个分类索引文件")
    print(f"   - 1个轻量清单文件")
    print(f"   - 2个哈希索引文件")
    print()
    print("🎯 AI访问方式：")
    print("   - 按类型: /static/indexes/代码模板.json")
    print("   - 轻量清单: /static/indexes/lightweight_manifest.json")
    print("   - UUID查询: /static/indexes/uuid_hash_index.json")
    print("   - ID查询: /static/indexes/id_hash_index.json")


if __name__ == "__main__":
    generate_static_protocol()
