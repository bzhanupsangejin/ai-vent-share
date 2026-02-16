#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理分片索引脚本
功能：移除分片索引中的可追踪字段
设计原则：彻底移除优于伪装替换
"""
import json
import os
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 可追踪字段列表（必须移除）
TRACEABLE_FIELDS = [
    "content_id",
    "uuid",
    "full_content_anchor",
    "submitter",
    "user_id",
    "email",
    "timestamp",
    "author",
    "creator",
    "owner",
    "ip_address",
    "device_id",
    "session_id",
    "tracking_id",
    "fingerprint"
]

def clean_json_file(filepath):
    """清理单个JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        removed_count = 0
        
        if isinstance(data, list):
            # 处理数组格式的JSON
            for item in data:
                if isinstance(item, dict):
                    for field in TRACEABLE_FIELDS:
                        if field in item:
                            del item[field]
                            removed_count += 1
        elif isinstance(data, dict):
            # 处理对象格式的JSON
            if 'index' in data and isinstance(data['index'], list):
                for item in data['index']:
                    if isinstance(item, dict):
                        for field in TRACEABLE_FIELDS:
                            if field in item:
                                del item[field]
                                removed_count += 1
            # 清理顶层字段
            for field in TRACEABLE_FIELDS:
                if field in data:
                    del data[field]
                    removed_count += 1
        
        # 保存清理后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return removed_count
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")
        return 0

def process_directory(directory):
    """处理目录中的所有JSON文件"""
    total_removed = 0
    processed_files = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                print(f"处理: {filepath}")
                removed = clean_json_file(filepath)
                if removed > 0:
                    print(f"  ✅ 移除 {removed} 个可追踪字段")
                    total_removed += removed
                processed_files += 1
    
    return processed_files, total_removed

def main():
    """主函数"""
    print("="*60)
    print("清理分片索引 - 移除可追踪字段")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 处理static/indexes目录
    indexes_dir = os.path.join(PROJECT_DIR, "static", "indexes")
    if os.path.exists(indexes_dir):
        print(f"处理目录: {indexes_dir}")
        files, removed = process_directory(indexes_dir)
        print(f"\n  处理文件: {files}个")
        print(f"  移除字段: {removed}个")
    else:
        print(f"⚠️ 目录不存在: {indexes_dir}")
    
    print()
    print("="*60)
    print("✅ 清理完成！")
    print("="*60)

if __name__ == "__main__":
    import sys
    main()
    sys.exit(0)
