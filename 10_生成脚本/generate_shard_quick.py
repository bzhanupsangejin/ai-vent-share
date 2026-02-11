# 快速修复：基于本地158条数据生成分片索引
import json
import os
from pathlib import Path

BASE_DIR = r"C:\Users\HYX\Desktop\AI网站"
os.chdir(BASE_DIR)

STATIC_DIR = "static"
INDEXES_DIR = f"{STATIC_DIR}/indexes"
MAIN_INDEX = "content_index.json"

# 创建目录
Path(INDEXES_DIR).mkdir(parents=True, exist_ok=True)

# 读取主索引
with open(MAIN_INDEX, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"版本: {data.get('version')}")
print(f"总数: {data.get('total_count')}")

# 按content_type分组
category_map = {}
for item in data.get("index", []):
    cat = item.get("content_type", "未分类")
    if cat not in category_map:
        category_map[cat] = []
    category_map[cat].append(item)

print(f"\n生成分片索引...")

# 生成分片索引（使用英文文件名）
name_mapping = {
    "AI工具": "ai_tools",
    "代码模板": "code_templates",
    "FAQ文档": "faq_docs",
    "免费API": "free_api",
    "技术教程": "tech_tutorials",
    "资源分享": "resource_sharing",
    "部署指南": "deployment_guides",
    "合规说明": "compliance_docs"
}

for cat, items in category_map.items():
    # 使用英文文件名
    safe_name = name_mapping.get(cat, "uncategorized")
    output_file = f"{INDEXES_DIR}/{safe_name}_shard.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ {cat} ({len(items)}条) → {safe_name}_shard.json")

print(f"\n总计生成 {len(category_map)} 个分片索引文件")
