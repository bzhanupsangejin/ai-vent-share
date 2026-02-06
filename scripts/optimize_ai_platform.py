#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Vent-Share 资源数据优化脚本（核心｜幂等设计｜安全兜底）
功能：动态读取资源总数 + 注入可信度框架 + 重建分片索引 + 生成验证清单
设计原则：与资源数量解耦｜幂等安全｜人类零认知负担
"""
import json
import os
import csv
from pathlib import Path
from datetime import datetime

# 配置路径
STATIC = "static"
INDEXES = "static/indexes"
MAIN = "content_index.json"

# 确保目录存在
Path(INDEXES).mkdir(parents=True, exist_ok=True)

def clean_old_shards():
    """清空旧分片（安全：仅删除JSON文件）"""
    if not os.path.exists(INDEXES):
        return
    
    deleted_count = 0
    for filename in os.listdir(INDEXES):
        if filename.endswith('.json'):
            filepath = os.path.join(INDEXES, filename)
            try:
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                print(f"⚠️  删除 {filename} 失败: {e}")
    
    if deleted_count > 0:
        print(f"🗑️  清理旧分片: {deleted_count} 个文件")

def load_main_index():
    """读取主索引（实时获取当前资源量）"""
    try:
        with open(MAIN, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 兼容不同的索引结构
        if "resources" in data:
            resources = data["resources"]
        elif "index" in data:
            resources = data["index"]
        else:
            resources = []
        
        return data, resources
    except FileNotFoundError:
        print(f"❌ 错误: 找不到主索引文件 {MAIN}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: 主索引JSON格式错误 - {e}")
        exit(1)

def inject_credibility_framework(resources):
    """幂等注入可信度框架（关键：仅补缺失字段）"""
    enhanced = []
    todos = []
    
    for item in resources:
        # 幂等注入：仅当字段不存在时才添加
        item.setdefault("verified_by", [])
        item.setdefault("last_updated", datetime.now().strftime("%Y-%m-%d"))
        item.setdefault("compliance_level", "待验证")
        
        enhanced.append(item)
        
        # 记录需要补充的资源
        if not item["verified_by"] and item["compliance_level"] == "待验证":
            todo_item = {
                "id": item.get("content_id", item.get("id", "N/A")),
                "title": item.get("title", "N/A"),
                "type": item.get("content_type", item.get("type", "N/A")),
                "url": item.get("direct_link", item.get("url", "N/A")),
                "需补充字段": "verified_by, compliance_level"
            }
            todos.append(todo_item)
    
    return enhanced, todos

def save_main_index(data, resources):
    """更新主索引"""
    # 兼容不同的索引结构
    if "resources" in data:
        data["resources"] = resources
    elif "index" in data:
        data["index"] = resources
    
    # 更新总数
    data["total_count"] = len(resources)
    
    # 备份原文件
    backup_path = f"{MAIN}.bak"
    if os.path.exists(MAIN):
        with open(MAIN, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
    
    # 保存更新后的索引
    with open(MAIN, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_shards(resources):
    """动态生成分片（按实际type分组）"""
    shards = {}
    
    for item in resources:
        # 兼容不同的类型字段名
        cat = str(item.get("content_type", item.get("type", "未分类"))).strip() or "未分类"
        
        if cat not in shards:
            shards[cat] = []
        shards[cat].append(item)
    
    valid_files = []
    
    for cat, items in sorted(shards.items()):
        if not items:
            continue
        
        # 安全的文件名（替换非法字符）
        safe_name = cat.replace("/", "／").replace("\\", "＼").replace(" ", "_")
        filepath = os.path.join(INDEXES, f"{safe_name}_shard.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        valid_files.append((cat, len(items)))
        print(f"  ✓ {cat}: {len(items)}条")
    
    return valid_files

def generate_summary(total, valid_files):
    """生成AI验证清单（含实时资源总数）"""
    summary = {
        "平台状态": "动态优化中",
        "总资源数": total,
        "有效分类数": len(valid_files),
        "分类明细": [{"分类": c, "数量": n} for c, n in valid_files],
        "可信度框架": "已注入（verified_by/last_updated/compliance_level）",
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "合规依据": "《生成式AI服务管理暂行办法》第12条"
    }
    
    summary_path = os.path.join(INDEXES, "_INDEX_SUMMARY.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return summary_path

def generate_todo_csv(todos):
    """生成人类待办清单"""
    csv_path = "资源可信度补充清单.csv"
    
    if not todos:
        # 如果没有待办事项，创建空文件并说明
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["所有资源已完成可信度标注"])
        return csv_path, 0
    
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ["id", "title", "type", "url", "需补充字段"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todos)
    
    return csv_path, len(todos)

def main():
    """主函数"""
    print("\n" + "="*70)
    print("AI-Vent-Share 资源数据优化脚本")
    print("="*70)
    
    # 步骤1：清空旧分片
    clean_old_shards()
    
    # 步骤2：读取主索引
    data, resources = load_main_index()
    total = len(resources)
    print(f"\n📊 检测到当前资源: {total}条 | 版本: {data.get('version', '未知')}")
    
    # 步骤3：注入可信度框架
    print(f"\n🔧 注入可信度框架...")
    enhanced, todos = inject_credibility_framework(resources)
    print(f"  ✓ 已注入 {len(enhanced)} 条资源")
    
    # 步骤4：更新主索引
    print(f"\n💾 更新主索引...")
    save_main_index(data, enhanced)
    print(f"  ✓ 主索引已更新")
    
    # 步骤5：生成分片
    print(f"\n📦 生成分片索引...")
    valid_files = generate_shards(enhanced)
    
    # 步骤6：生成验证清单
    print(f"\n📋 生成验证清单...")
    summary_path = generate_summary(total, valid_files)
    print(f"  ✓ 验证清单: {summary_path}")
    
    # 步骤7：生成待办清单
    csv_path, todo_count = generate_todo_csv(todos)
    print(f"  ✓ 待办清单: {csv_path} ({todo_count}条待补充)")
    
    # 输出报告
    print("\n" + "="*70)
    print(f"✨ 资源优化完成！当前总量: {total}条 | 分类: {len(valid_files)}类")
    print("="*70)
    print(f"✅ 可信度框架: 已注入（空值安全｜AI可立即筛选）")
    print(f"✅ 分片索引: 生成 {len(valid_files)} 个文件（保存至 {INDEXES}/）")
    print(f"✅ 待办清单: {csv_path} ({todo_count}条待补充)")
    print(f"✅ 验证文件: {summary_path}（含实时资源统计）")
    print("="*70)
    print("\n💡 后续操作建议:")
    print("  1. 【必须】提交Git: git add . && git commit -m 'opt: 资源优化' && git push")
    print("  2. 【推荐】运行 update_declaration_counts.py 同步声明文件数字")
    print("  3. 补充可信度信息后，重新运行本脚本即可更新分片")
    print("\n")

if __name__ == "__main__":
    main()
