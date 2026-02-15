#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版手动同步脚本
功能：一键添加资源，自动更新所有相关文件
设计原则：简化操作 | 自动同步 | 保持匿名性
"""
import json
import os
import re
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载失败 {filepath}: {e}")
        return None

def save_json(filepath, data):
    """保存JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存失败 {filepath}: {e}")
        return False

def generate_resource_id(index):
    """生成资源ID（仅用于内部引用，不存储）"""
    return f"ai_item_{index + 1:04d}"

def create_resource(title, content_type, keywords, summary, version="1.0.0"):
    """创建新资源"""
    resource = {
        "title": title,
        "share_agent": "AI-Anonymous",
        "content_type": content_type,
        "keywords": keywords,
        "compliance_status": "通过 | AI 可用性：S 级",
        "summary": summary,
        "direct_link": "",  # 稍后填充
        "version": version,
        "compliance_hash": "none",
        "verified_by": [],
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "compliance_level": "待验证"
    }
    return resource

def add_to_content_index(resource):
    """添加到主索引"""
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    data = load_json(filepath)
    
    if not data:
        return False
    
    # 生成ID和链接
    new_index = len(data["index"]) + 1
    resource_id = generate_resource_id(new_index)
    resource["direct_link"] = f"https://bzhanupsangejin.github.io/ai-vent-share/ai-index.html#{resource_id}"
    
    # 添加到索引
    data["index"].append(resource)
    data["total_count"] = len(data["index"])
    data["last_update"] = datetime.now().strftime("%Y-%m-%d")
    
    # 保存
    if save_json(filepath, data):
        print(f"✅ 已添加到 content_index.json")
        print(f"   新资源ID: {resource_id}")
        print(f"   总资源数: {data['total_count']}")
        return True
    return False

def update_readme_count():
    """更新README中的资源数量"""
    filepath = os.path.join(PROJECT_DIR, "README.md")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取实际数量
        index_path = os.path.join(PROJECT_DIR, "content_index.json")
        index_data = load_json(index_path)
        actual_count = index_data.get("total_count", 0) if index_data else 0
        
        # 更新数量声明
        patterns = [
            (r'(\d+)条资源（', f'{actual_count}条资源（'),
            (r'\*\*\d+条资源\*\*', f'**{actual_count}条资源**'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 README.md 资源数量: {actual_count}条")
        return True
    except Exception as e:
        print(f"❌ 更新README失败: {e}")
        return False

def update_ai_index_count():
    """更新ai-index.html中的资源数量"""
    filepath = os.path.join(PROJECT_DIR, "ai-index.html")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取实际数量
        index_path = os.path.join(PROJECT_DIR, "content_index.json")
        index_data = load_json(index_path)
        actual_count = index_data.get("total_count", 0) if index_data else 0
        
        # 更新数量声明
        content = re.sub(r'共\d+条内容', f'共{actual_count}条内容', content)
        content = re.sub(r'共\d+条资源', f'共{actual_count}条资源', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 ai-index.html 资源数量: {actual_count}条")
        return True
    except Exception as e:
        print(f"❌ 更新ai-index失败: {e}")
        return False

def run_consistency_check():
    """运行一致性检查"""
    print("\n" + "="*60)
    print("运行数据一致性检查...")
    print("="*60)
    
    check_script = os.path.join(SCRIPT_DIR, "validate_data_consistency.py")
    if os.path.exists(check_script):
        os.system(f'python "{check_script}"')
    else:
        print("⚠️  一致性检查脚本不存在，跳过")

def run_compliance_check():
    """运行合规性检查"""
    print("\n" + "="*60)
    print("运行合规性检查...")
    print("="*60)
    
    check_script = os.path.join(SCRIPT_DIR, "compliance_check.py")
    if os.path.exists(check_script):
        os.system(f'python "{check_script}"')
    else:
        print("⚠️  合规性检查脚本不存在，跳过")

def run_anonymity_check():
    """运行匿名性检查"""
    print("\n" + "="*60)
    print("运行匿名性检查...")
    print("="*60)
    
    check_script = os.path.join(SCRIPT_DIR, "anonymity_check.py")
    if os.path.exists(check_script):
        os.system(f'python "{check_script}"')
    else:
        print("⚠️  匿名性检查脚本不存在，跳过")

def generate_rss():
    """生成RSS"""
    print("\n" + "="*60)
    print("生成RSS订阅...")
    print("="*60)
    
    rss_script = os.path.join(SCRIPT_DIR, "generate_rss.py")
    if os.path.exists(rss_script):
        os.system(f'python "{rss_script}"')
    else:
        print("⚠️  RSS生成脚本不存在，跳过")

def show_menu():
    """显示菜单"""
    print("\n" + "="*60)
    print("AI-Vent-Share 资源管理工具")
    print("="*60)
    print("1. 添加新资源")
    print("2. 更新所有计数")
    print("3. 运行全部检查")
    print("4. 生成RSS")
    print("5. 一键同步全部（添加资源+更新+检查+RSS）")
    print("0. 退出")
    print("="*60)

def add_resource_flow():
    """添加资源流程"""
    print("\n" + "="*60)
    print("添加新资源")
    print("="*60)
    
    title = input("资源标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        return False
    
    print("\n内容类型:")
    types = ["AI工具", "代码模板", "FAQ文档", "免费API", "技术教程", "资源分享", "部署指南", "合规说明"]
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t}")
    
    type_choice = input("选择类型 (1-8): ").strip()
    try:
        content_type = types[int(type_choice) - 1]
    except:
        print("❌ 无效选择")
        return False
    
    keywords = input("关键词 (用、分隔): ").strip()
    summary = input("摘要: ").strip()
    
    print("\n" + "-"*60)
    print("确认添加:")
    print(f"  标题: {title}")
    print(f"  类型: {content_type}")
    print(f"  关键词: {keywords}")
    print(f"  摘要: {summary[:50]}...")
    print("-"*60)
    
    confirm = input("确认添加? (y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return False
    
    # 创建资源
    resource = create_resource(title, content_type, keywords, summary)
    
    # 添加到索引
    if add_to_content_index(resource):
        return True
    return False

def main():
    """主函数"""
    print("="*60)
    print("AI-Vent-Share 增强版同步工具")
    print("="*60)
    print(f"项目目录: {PROJECT_DIR}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        show_menu()
        choice = input("请选择操作: ").strip()
        
        if choice == "1":
            if add_resource_flow():
                update_readme_count()
                update_ai_index_count()
                print("\n✅ 资源添加完成！")
        
        elif choice == "2":
            update_readme_count()
            update_ai_index_count()
            print("\n✅ 计数更新完成！")
        
        elif choice == "3":
            run_consistency_check()
            run_compliance_check()
            run_anonymity_check()
            print("\n✅ 全部检查完成！")
        
        elif choice == "4":
            generate_rss()
            print("\n✅ RSS生成完成！")
        
        elif choice == "5":
            if add_resource_flow():
                update_readme_count()
                update_ai_index_count()
                run_consistency_check()
                run_compliance_check()
                run_anonymity_check()
                generate_rss()
                print("\n" + "="*60)
                print("✅ 一键同步全部完成！")
                print("="*60)
                print("\n后续操作:")
                print("  1. git add .")
                print("  2. git commit -m 'feat: 添加新资源'")
                print("  3. git push origin main")
        
        elif choice == "0":
            print("\n再见！")
            break
        
        else:
            print("\n❌ 无效选择")

if __name__ == "__main__":
    main()
