#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成content_index.min.json脚本
功能：从content_index.json生成压缩版本
设计原则：保持数据一致性
"""
import json
import os
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def main():
    """主函数"""
    print("="*60)
    print("重新生成 content_index.min.json")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 读取原始JSON
    input_path = os.path.join(PROJECT_DIR, "content_index.json")
    output_path = os.path.join(PROJECT_DIR, "content_index.min.json")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 读取成功: {input_path}")
        print(f"   资源数: {data.get('total_count', 0)}")
        print()
        
        # 清理summary中的分享者信息（如果有）
        for item in data.get('index', []):
            summary = item.get('summary', '')
            # 替换分享者编号为AI-Anonymous
            import re
            summary = re.sub(r'分享者：AI-\d+', '分享者：AI-Anonymous', summary)
            item['summary'] = summary
        
        # 保存压缩版本
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        
        print(f"✅ 保存成功: {output_path}")
        
        # 检查文件大小
        original_size = os.path.getsize(input_path)
        min_size = os.path.getsize(output_path)
        print(f"   原始大小: {original_size/1024:.1f} KB")
        print(f"   压缩大小: {min_size/1024:.1f} KB")
        print(f"   压缩率: {(1-min_size/original_size)*100:.1f}%")
        print()
        print("="*60)
        print("✅ 完成！")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
