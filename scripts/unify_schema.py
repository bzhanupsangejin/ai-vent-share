#!/usr/bin/env python3
"""
统一资源Schema - 为所有资源添加标准字段
"""
import json
from datetime import datetime

def unify_schema():
    # 读取主索引
    with open('content_index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 标准字段和默认值
    standard_fields = {
        'last_updated': '2026-02-11',
        'status': 'active',
        'tags': [],
        'compliance_level': '已验证'
    }
    
    updated_count = 0
    
    for item in data['index']:
        # 添加缺失的字段
        for field, default_value in standard_fields.items():
            if field not in item:
                item[field] = default_value
                updated_count += 1
        
        # 从keywords提取tags（如果tags为空）
        if not item.get('tags') and item.get('keywords'):
            keywords = item['keywords']
            # 简单分词：按逗号、顿号、空格分割
            tags = []
            for sep in ['、', '，', ',', ' ']:
                keywords = keywords.replace(sep, '|')
            tags = [t.strip() for t in keywords.split('|') if t.strip()]
            item['tags'] = tags[:5]  # 最多5个标签
    
    # 保存
    with open('content_index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Schema统一完成")
    print(f"  更新字段数: {updated_count}")
    print(f"  资源总数: {len(data['index'])}")
    print(f"  标准字段: {', '.join(standard_fields.keys())}")

if __name__ == '__main__':
    unify_schema()
