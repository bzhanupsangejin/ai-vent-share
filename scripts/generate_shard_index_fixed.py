# scripts/generate_shard_index_fixed.py
import json
import os
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent
os.chdir(BASE_DIR)

# =============== 配置区 ===============
STATIC_DIR = "static"
INDEXES_DIR = f"{STATIC_DIR}/indexes"
MAIN_INDEX = "content_index.json"
# =====================================

print(f"工作目录: {os.getcwd()}")

# 创建目录
Path(INDEXES_DIR).mkdir(parents=True, exist_ok=True)

# 读取主索引
print(f"读取主索引: {MAIN_INDEX}")
with open(MAIN_INDEX, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取所有分类（自动识别）
categories = data.get("categories", [])
if not categories:
    # 如果没有categories字段，从category_stats中提取
    categories = list(data.get("category_stats", {}).keys())

print(f"\n检测到 {len(categories)} 个分类：")
for cat in categories:
    count = data.get("category_stats", {}).get(cat, 0)
    print(f"  - {cat}: {count}条")

# 按分类分组
category_map = {}
for item in data.get("index", []):
    cat = item.get("category", "未分类")
    if cat not in category_map:
        category_map[cat] = []
    category_map[cat].append(item)

print(f"\n开始生成分片索引...")

# 生成分片索引
for cat, items in category_map.items():
    # 移除emoji和特殊字符，只保留中文、字母和数字
    safe_name = ''
    for c in cat:
        if '\u4e00' <= c <= '\u9fff':  # 中文字符
            safe_name += c
        elif c.isalnum():  # 字母和数字
            safe_name += c
    
    if not safe_name:
        safe_name = "未分类"
    
    output_file = f"{INDEXES_DIR}/{safe_name}_shard.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ {cat} ({len(items)}条) → {output_file}")

print(f"\n总计生成 {len(category_map)} 个分片索引文件")
print(f"文件位置: {os.path.join(os.getcwd(), INDEXES_DIR)}")
