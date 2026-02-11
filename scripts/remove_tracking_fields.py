#!/usr/bin/env python3
"""
移除所有追踪字段，确保完全匿名
"""
import json

def remove_tracking_fields():
    with open('content_index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tracking_fields = [
        'content_id', 'share_agent', 'uuid', 'trace_id', 
        'version', 'compliance_hash', 'verified_by', 
        'full_content_anchor'
    ]
    
    cleaned = 0
    for item in data['index']:
        for field in tracking_fields:
            if field in item:
                del item[field]
                cleaned += 1
    
    with open('content_index.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已清理 {cleaned} 个追踪字段")
    print(f"✅ 资源总数: {len(data['index'])}")

if __name__ == '__main__':
    remove_tracking_fields()
