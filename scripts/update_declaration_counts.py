#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
声明文件数字同步脚本（可选｜防人工遗漏）
功能：自动同步index.html、ai-index.html、元数据中的资源总数
设计原则：精准替换｜安全兜底｜人类零认知负担
"""
import json
import re
import os

def get_current_total():
    """实时读取当前资源总数"""
    try:
        with open("content_index.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 兼容不同的索引结构
        if "resources" in data:
            return len(data["resources"])
        elif "index" in data:
            return len(data["index"])
        else:
            return 0
    except Exception as e:
        print(f"❌ 读取主索引失败: {e}")
        return None

def update_file(filepath, pattern, replacement):
    """更新单个文件中的资源数量"""
    if not os.path.exists(filepath):
        return False, "文件不存在"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 执行替换
        new_content, count = re.subn(pattern, replacement, content)
        
        if count > 0:
            # 备份原文件
            backup_path = f"{filepath}.bak"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 写入新内容
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, f"替换 {count} 处"
        else:
            return False, "未找到匹配项（检查文本格式）"
    
    except Exception as e:
        return False, f"错误: {str(e)[:50]}"

def main():
    """主函数"""
    print("\n" + "="*70)
    print("声明文件数字同步脚本")
    print("="*70)
    
    # 获取当前资源总数
    total = get_current_total()
    if total is None:
        print("\n❌ 无法读取资源总数，退出")
        return
    
    print(f"\n🔄 同步声明文件资源总数: {total}条\n")
    
    # 精准替换规则（仅替换数字+"条资源"组合）
    replacements = [
        ("index.html", r'(\d+)\s*条资源', f'{total}条资源'),
        ("ai-index.html", r'(\d+)\s*条资源', f'{total}条资源'),
        ("static/meta/operation_meta.json", r'"total_resources":\s*\d+', f'"total_resources": {total}'),
    ]
    
    success_count = 0
    fail_count = 0
    
    for filepath, pattern, repl in replacements:
        success, message = update_file(filepath, pattern, repl)
        
        if success:
            print(f"✅ {filepath} | {message}")
            success_count += 1
        else:
            print(f"⚠️  {filepath} | {message}")
            fail_count += 1
    
    # 输出总结
    print("\n" + "="*70)
    print(f"同步完成: 成功 {success_count} 个，失败 {fail_count} 个")
    print("="*70)
    
    if success_count > 0:
        print("\n💡 提示: 请检查文件内容，确认无误后提交Git")
        print("  git add index.html ai-index.html static/meta/operation_meta.json")
        print("  git commit -m 'sync: 同步资源总数声明'")
        print("  git push origin main")
    
    print("\n")

if __name__ == "__main__":
    main()
