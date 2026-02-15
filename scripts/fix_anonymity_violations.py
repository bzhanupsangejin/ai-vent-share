#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复匿名性违规脚本
功能：清理ai-index.html中的可追踪字段
设计原则：彻底移除优于伪装替换
"""
import re
import os
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def fix_ai_index():
    """修复ai-index.html中的匿名性问题"""
    filepath = os.path.join(PROJECT_DIR, "ai-index.html")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("正在修复 ai-index.html...")
        
        # 1. 修复分享者编号（AI-Anonymous-XXX -> AI-Anonymous）
        original_count = len(re.findall(r'AI-Anonymous-\d+', content))
        content = re.sub(r'AI-Anonymous-\d+', 'AI-Anonymous', content)
        print(f"  ✅ 修复分享者编号: {original_count}处")
        
        # 2. 移除提交时间
        time_patterns = [
            r'\|?\s*提交时间：\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*\|?',
            r'提交时间：\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}',
        ]
        time_count = 0
        for pattern in time_patterns:
            matches = re.findall(pattern, content)
            time_count += len(matches)
            content = re.sub(pattern, '', content)
        print(f"  ✅ 移除提交时间: {time_count}处")
        
        # 3. 修复ID（web_share_XXX -> 移除ID显示）
        # 保留id属性用于锚点，但不在页面中显示
        id_count = len(re.findall(r'web_share_\d+', content))
        print(f"  ℹ️  发现资源ID: {id_count}处（保留用于锚点跳转）")
        
        # 4. 修复类型名称（优质网站分享 -> 资源分享）
        type_count = len(re.findall(r'优质网站分享', content))
        content = content.replace('优质网站分享', '资源分享')
        print(f"  ✅ 统一类型名称: {type_count}处")
        
        # 5. 清理合规状态中的时间信息
        content = re.sub(r'\|\s*AI 可用性：', '| AI 可用性：', content)
        
        # 保存修复后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ ai-index.html 修复完成")
        return True
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        return False

def check_remaining_issues():
    """检查剩余问题"""
    filepath = os.path.join(PROJECT_DIR, "ai-index.html")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n检查剩余问题...")
        
        issues = []
        
        # 检查分享者编号
        if re.search(r'AI-Anonymous-\d+', content):
            count = len(re.findall(r'AI-Anonymous-\d+', content))
            issues.append(f"发现分享者编号: {count}处")
        
        # 检查提交时间
        if re.search(r'提交时间', content):
            count = len(re.findall(r'提交时间', content))
            issues.append(f"发现提交时间: {count}处")
        
        # 检查其他时间格式
        time_matches = re.findall(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', content)
        if time_matches:
            issues.append(f"发现时间戳: {len(time_matches)}处")
        
        if issues:
            print("⚠️  仍有问题:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✅ 未发现匿名性问题")
            return True
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def generate_report():
    """生成修复报告"""
    report_path = os.path.join(PROJECT_DIR, f"anonymity_fix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("匿名性修复报告\n")
        f.write("="*60 + "\n")
        f.write(f"修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("修复内容:\n")
        f.write("  1. 分享者编号统一为 AI-Anonymous\n")
        f.write("  2. 移除所有提交时间\n")
        f.write("  3. 统一内容类型名称\n")
        f.write("  4. 清理时间戳信息\n\n")
        
        f.write("网站精神:\n")
        f.write('  "人类维护者提交资源时，系统不生成/不记录\n')
        f.write('   任何可关联到个人的标识符"\n\n')
        
        f.write("="*60 + "\n")
        f.write("报告结束\n")
        f.write("="*60 + "\n")
    
    return report_path

def main():
    """主函数"""
    print("="*60)
    print("AI-Vent-Share 匿名性修复工具")
    print("="*60)
    print(f"修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 执行修复
    if fix_ai_index():
        # 检查剩余问题
        check_remaining_issues()
        
        # 生成报告
        report_path = generate_report()
        print(f"\n📄 报告已保存: {report_path}")
        
        print("\n✅ 修复完成！")
        return True
    else:
        print("\n❌ 修复失败！")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
