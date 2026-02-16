#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理content_index.json脚本
功能：移除summary中的分享者编号
设计原则：彻底匿名
"""
import json
import os
import re
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def main():
    """主函数"""
    print("="*60)
    print("清理 content_index.json - 移除分享者编号")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 读取成功")
        print(f"   资源数: {data.get('total_count', 0)}")
        print()
        
        # 清理summary中的分享者编号
        fixed_count = 0
        for item in data.get('index', []):
            summary = item.get('summary', '')
            # 查找分享者编号（如AI-0193）
            if re.search(r'AI-\d{3,4}', summary):
                # 替换为AI-Anonymous
                summary = re.sub(r'AI-\d{3,4}', 'AI-Anonymous', summary)
                item['summary'] = summary
                fixed_count += 1
        
        print(f"✅ 修复资源: {fixed_count}条")
        print()
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 保存成功: {filepath}")
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
