#!/usr/bin/env python3
"""
验证网站完整性和匿名性
"""
import json
import os

def verify_anonymity():
    print("=" * 60)
    print("AI网站匿名性和完整性验证")
    print("=" * 60)
    
    # 检查主索引
    with open('content_index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tracking_fields = ['content_id', 'share_agent', 'uuid', 'trace_id', 'version', 'compliance_hash']
    found_tracking = []
    
    for item in data['index']:
        for field in tracking_fields:
            if field in item:
                found_tracking.append(field)
    
    if found_tracking:
        print(f"❌ 发现追踪字段: {set(found_tracking)}")
    else:
        print("✅ 主索引完全匿名（无追踪字段）")
    
    # 检查必需字段
    required_fields = ['title', 'content_type', 'summary', 'direct_link']
    missing_fields = []
    
    for i, item in enumerate(data['index']):
        for field in required_fields:
            if field not in item:
                missing_fields.append(f"资源{i}: 缺少{field}")
    
    if missing_fields:
        print(f"❌ 发现缺失字段: {len(missing_fields)}个")
        for msg in missing_fields[:5]:
            print(f"  {msg}")
    else:
        print("✅ 所有资源包含必需字段")
    
    # 检查压缩版本
    if os.path.exists('content_index.min.json'):
        original_size = os.path.getsize('content_index.json')
        compressed_size = os.path.getsize('content_index.min.json')
        print(f"✅ 压缩版本存在 (减少 {(1-compressed_size/original_size)*100:.1f}%)")
    else:
        print("⚠️  压缩版本不存在")
    
    # 检查搜索功能
    if os.path.exists('search.html') and os.path.exists('static/js/search.js'):
        print("✅ 搜索功能文件完整")
    else:
        print("❌ 搜索功能文件缺失")
    
    # 统计信息
    print(f"\n📊 统计信息:")
    print(f"  总资源数: {len(data['index'])}")
    
    categories = {}
    for item in data['index']:
        cat = item.get('content_type', '未分类')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"  分类数: {len(categories)}")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"    {cat}: {count}条")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    verify_anonymity()
