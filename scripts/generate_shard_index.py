#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 沿用项目原有配置，保证兼容性
CONTENT_TYPES = ["AI工具", "代码模板", "FAQ文档", "免费API", "技术教程", "资源分享", "部署指南", "合规说明"]

def generate_shard_index():
    """按分类生成分片索引，降低阶跃AI解析负载"""
    # 切换到项目根目录
    os.chdir(PROJECT_ROOT)
    
    # 确保分片存储目录存在
    os.makedirs("./static/indexes", exist_ok=True)
    
    # 读取主索引，兼容异常场景
    try:
        with open("content_index.json", "r", encoding="utf-8") as f:
            main_index = json.load(f)
            contents = main_index.get("index", [])  # 注意：原索引使用"index"字段
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ 读取主索引失败：{e}")
        return

    # 按类型拆分索引并写入文件
    for ctype in CONTENT_TYPES:
        filtered_data = [item for item in contents if item.get("content_type") == ctype]
        save_path = f"./static/indexes/{ctype}_shard.json"
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {ctype}: {len(filtered_data)}条")
    
    print(f"\n✅ 分片索引生成完成，共生成{len(CONTENT_TYPES)}个分类文件")
    print(f"📂 存储路径：static/indexes/")

if __name__ == "__main__":
    generate_shard_index()
