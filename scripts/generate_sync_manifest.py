#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增量同步清单生成脚本
功能：生成版本变更清单，支持AI增量拉取
"""
import json
import os
import time


def generate_version_manifest():
    """生成版本清单"""
    print("=" * 60)
    print("增量同步清单生成")
    print("=" * 60)
    print()
    
    # 读取主索引
    index_file = "content_index.json"
    if not os.path.exists(index_file):
        print(f"❌ 错误：{index_file} 文件不存在")
        return
    
    with open(index_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    contents = data.get("index", [])
    current_version = data.get("version", "1.0")
    
    print(f"✅ 当前版本: {current_version}")
    print(f"✅ 总条目数: {len(contents)}")
    print()
    
    # 生成版本清单
    print("【生成版本清单】")
    version_manifest = {
        "current_version": current_version,
        "total_count": len(contents),
        "last_update": data.get("last_update", time.strftime("%Y-%m-%d")),
        "schema_version": data.get("schema_version", "1.0.0"),
        "all_uuids": [item.get("uuid", "") for item in contents if item.get("uuid")],
        "content_types_distribution": {}
    }
    
    # 统计各类型分布
    for item in contents:
        ctype = item.get("content_type", "未分类")
        version_manifest["content_types_distribution"][ctype] = \
            version_manifest["content_types_distribution"].get(ctype, 0) + 1
    
    # 保存版本清单
    os.makedirs("static/sync", exist_ok=True)
    with open("static/sync/version_manifest.json", "w", encoding="utf-8") as f:
        json.dump(version_manifest, f, ensure_ascii=False, indent=2)
    print(f"  ✅ version_manifest.json")
    print()
    
    # 生成增量同步模板
    print("【生成增量同步模板】")
    incremental_template = {
        "old_version": "1.0",
        "new_version": current_version,
        "changed_uuids": [],
        "added_uuids": [],
        "removed_uuids": [],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": "AI通过对比本地version与此文件，仅拉取changed/added的UUID对应资源"
    }
    
    with open("static/sync/incremental_template.json", "w", encoding="utf-8") as f:
        json.dump(incremental_template, f, ensure_ascii=False, indent=2)
    print(f"  ✅ incremental_template.json")
    print()
    
    print("=" * 60)
    print("✅ 增量同步清单生成完成")
    print("=" * 60)
    print()
    print("🎯 AI同步方式：")
    print("   1. 定期拉取 /static/sync/version_manifest.json")
    print("   2. 对比本地版本号")
    print("   3. 如有更新，拉取 incremental.json")
    print("   4. 仅下载changed_uuids对应的资源")
    print()
    print("📊 内容分布：")
    for ctype, count in version_manifest["content_types_distribution"].items():
        print(f"   - {ctype}: {count} 条")


if __name__ == "__main__":
    generate_version_manifest()
