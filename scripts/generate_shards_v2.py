# 智能分片生成脚本 v2（零容错设计）
import json
import os
from pathlib import Path

BASE_DIR = r"C:\Users\HYX\Desktop\AI网站"
os.chdir(BASE_DIR)

STATIC = "static"
INDEXES = f"{STATIC}/indexes"
MAIN = "content_index.json"

# 创建目录
Path(INDEXES).mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("智能分片生成脚本 v2")
print("=" * 70)

# 读取主索引
print(f"\n读取主索引: {MAIN}")
with open(MAIN, 'r', encoding='utf-8') as f:
    data = json.load(f)

version = data.get('version', '未知')
total = data.get('total_count', 0)
print(f"版本: {version}")
print(f"总数: {total}条")

# 智能识别分类字段
categories = data.get('categories', [])
if not categories:
    categories = data.get('content_types', [])
if not categories:
    categories = list(data.get('category_stats', {}).keys())

print(f"分类数: {len(categories)}个")

# 按分类分组
category_map = {}

# 尝试多个可能的分类字段
for item in data.get("index", []):
    # 优先使用category字段
    cat = item.get("category")
    if not cat:
        # 备用：使用content_type字段
        cat = item.get("content_type")
    if not cat:
        cat = "未分类"
    
    if cat not in category_map:
        category_map[cat] = []
    category_map[cat].append(item)

print(f"\n实际分组: {len(category_map)}个")
for cat, items in category_map.items():
    print(f"  - {cat}: {len(items)}条")

# 生成分片索引（使用安全文件名）
print(f"\n开始生成分片索引...")

# 文件名映射（移除emoji和特殊字符）
def safe_filename(name):
    """生成安全的文件名"""
    # 移除emoji
    safe = ''
    for c in name:
        if '\u4e00' <= c <= '\u9fff':  # 中文
            safe += c
        elif c.isalnum():  # 字母数字
            safe += c
        elif c in ' -_':  # 允许的特殊字符
            safe += c
    
    safe = safe.strip()
    if not safe:
        safe = 'uncategorized'
    
    # 替换空格为下划线
    safe = safe.replace(' ', '_')
    
    return safe

success_count = 0
for cat, items in category_map.items():
    if not items:  # 跳过空分类
        print(f"  ⏭️  跳过空分类: {cat}")
        continue
    
    safe_name = safe_filename(cat)
    output_file = f"{INDEXES}/{safe_name}_shard.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ {cat} ({len(items)}条) → {safe_name}_shard.json")
        success_count += 1
    except Exception as e:
        print(f"  ❌ {cat} 生成失败: {e}")

print(f"\n" + "=" * 70)
print(f"生成完成: {success_count}/{len(category_map)} 个分片索引")
print(f"文件位置: {os.path.join(BASE_DIR, INDEXES)}")
print("=" * 70)
