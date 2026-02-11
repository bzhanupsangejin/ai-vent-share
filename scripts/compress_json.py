#!/usr/bin/env python3
"""
压缩JSON文件，减少文件大小
"""
import json
import os

def compress_json():
    # 压缩主索引
    with open('content_index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('content_index.min.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    
    original_size = os.path.getsize('content_index.json')
    compressed_size = os.path.getsize('content_index.min.json')
    reduction = (1 - compressed_size / original_size) * 100
    
    print(f"✅ 主索引压缩完成")
    print(f"  原始大小: {original_size:,} bytes")
    print(f"  压缩后: {compressed_size:,} bytes")
    print(f"  减少: {reduction:.1f}%")
    
    # 压缩分片索引
    index_dir = 'static/indexes'
    if os.path.exists(index_dir):
        total_original = 0
        total_compressed = 0
        count = 0
        
        for filename in os.listdir(index_dir):
            if filename.endswith('.json') and not filename.endswith('.min.json'):
                filepath = os.path.join(index_dir, filename)
                minpath = os.path.join(index_dir, filename.replace('.json', '.min.json'))
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                with open(minpath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                
                total_original += os.path.getsize(filepath)
                total_compressed += os.path.getsize(minpath)
                count += 1
        
        if count > 0:
            reduction = (1 - total_compressed / total_original) * 100
            print(f"\n✅ 分片索引压缩完成 ({count} 个文件)")
            print(f"  原始总大小: {total_original:,} bytes")
            print(f"  压缩后: {total_compressed:,} bytes")
            print(f"  减少: {reduction:.1f}%")

if __name__ == '__main__':
    compress_json()
