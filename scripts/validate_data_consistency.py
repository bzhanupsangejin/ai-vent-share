#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据一致性检查脚本
功能：验证content_index.json、ai-index.html、README.md等文件的数据一致性
设计原则：自动化检查 | 发现问题 | 生成报告
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

def check_content_index():
    """检查content_index.json"""
    print("\n" + "="*60)
    print("检查 content_index.json")
    print("="*60)
    
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    data = load_json(filepath)
    
    if not data:
        return False, []
    
    issues = []
    
    # 检查必要字段
    required_fields = ["version", "last_update", "total_count", "content_types", "index"]
    for field in required_fields:
        if field not in data:
            issues.append(f"缺少必要字段: {field}")
    
    # 检查资源数量
    actual_count = len(data.get("index", []))
    declared_count = data.get("total_count", 0)
    
    if actual_count != declared_count:
        issues.append(f"资源数量不一致: 声明{declared_count}条，实际{actual_count}条")
    
    print(f"✅ 声明资源数: {declared_count}")
    print(f"✅ 实际资源数: {actual_count}")
    
    # 检查内容类型
    content_types = data.get("content_types", [])
    print(f"✅ 内容类型: {len(content_types)}种")
    for ct in content_types:
        print(f"  - {ct}")
    
    # 检查每条资源的必要字段
    index = data.get("index", [])
    resource_required = ["title", "share_agent", "content_type", "keywords", 
                         "compliance_status", "summary", "direct_link"]
    
    missing_fields_count = 0
    for i, item in enumerate(index):
        for field in resource_required:
            if field not in item:
                missing_fields_count += 1
                if missing_fields_count <= 5:  # 只显示前5个
                    issues.append(f"资源[{i}]缺少字段: {field}")
    
    if missing_fields_count > 5:
        issues.append(f"还有{missing_fields_count - 5}条资源缺少字段...")
    
    # 检查匿名性
    non_anonymous = []
    for i, item in enumerate(index):
        share_agent = item.get("share_agent", "")
        if share_agent != "AI-Anonymous":
            non_anonymous.append((i, share_agent))
    
    if non_anonymous:
        issues.append(f"发现{len(non_anonymous)}条资源share_agent不是AI-Anonymous")
        for i, agent in non_anonymous[:3]:
            print(f"  ⚠️  资源[{i}] share_agent='{agent}'")
    else:
        print("✅ 所有资源share_agent均为AI-Anonymous")
    
    # 检查可追踪字段
    traceable_fields = ["content_id", "uuid", "full_content_anchor", "submitter", 
                        "user_id", "email", "timestamp"]
    found_traceable = []
    
    for i, item in enumerate(index):
        for field in traceable_fields:
            if field in item:
                found_traceable.append((i, field))
    
    if found_traceable:
        issues.append(f"发现{len(found_traceable)}条资源包含可追踪字段")
        for i, field in found_traceable[:3]:
            print(f"  ⚠️  资源[{i}]包含可追踪字段: {field}")
    else:
        print("✅ 未发现可追踪字段")
    
    # 统计各类型数量
    type_counts = {}
    for item in index:
        ct = item.get("content_type", "未知")
        type_counts[ct] = type_counts.get(ct, 0) + 1
    
    print("\n📊 各类型资源统计:")
    for ct, count in sorted(type_counts.items()):
        print(f"  - {ct}: {count}条")
    
    if issues:
        print(f"\n❌ 发现{len(issues)}个问题")
        for issue in issues:
            print(f"  - {issue}")
        return False, issues
    else:
        print("\n✅ content_index.json 检查通过")
        return True, []

def check_readme():
    """检查README.md"""
    print("\n" + "="*60)
    print("检查 README.md")
    print("="*60)
    
    filepath = os.path.join(PROJECT_DIR, "README.md")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return False, [f"无法读取README.md: {e}"]
    
    issues = []
    
    # 检查资源数量声明
    # 匹配 "309条资源" 或 "**309条资源**"
    count_patterns = [
        r'(\d+)条资源',
        r'\*\*(\d+)条资源\*\*',
        r'总资源.*?(\d+)条'
    ]
    
    found_counts = []
    for pattern in count_patterns:
        matches = re.findall(pattern, content)
        found_counts.extend([int(m) for m in matches])
    
    if found_counts:
        # 获取content_index中的实际数量
        index_path = os.path.join(PROJECT_DIR, "content_index.json")
        index_data = load_json(index_path)
        actual_count = index_data.get("total_count", 0) if index_data else 0
        
        readme_count = found_counts[0]
        print(f"README声明: {readme_count}条")
        print(f"实际资源数: {actual_count}条")
        
        if readme_count != actual_count:
            issues.append(f"README资源数量声明错误: {readme_count} != {actual_count}")
    else:
        issues.append("README中未找到资源数量声明")
    
    # 检查必要章节
    required_sections = ["项目简介", "核心特点", "项目结构", "访问地址"]
    for section in required_sections:
        if section not in content:
            issues.append(f"README缺少章节: {section}")
    
    if issues:
        print(f"\n❌ 发现{len(issues)}个问题")
        for issue in issues:
            print(f"  - {issue}")
        return False, issues
    else:
        print("\n✅ README.md 检查通过")
        return True, []

def check_ai_index():
    """检查ai-index.html"""
    print("\n" + "="*60)
    print("检查 ai-index.html")
    print("="*60)
    
    filepath = os.path.join(PROJECT_DIR, "ai-index.html")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return False, [f"无法读取ai-index.html: {e}"]
    
    issues = []
    
    # 检查资源数量声明
    count_patterns = [
        r'(\d+)条内容',
        r'(\d+)条资源',
        r'共(\d+)条'
    ]
    
    found_counts = []
    for pattern in count_patterns:
        matches = re.findall(pattern, content)
        found_counts.extend([int(m) for m in matches])
    
    if found_counts:
        index_path = os.path.join(PROJECT_DIR, "content_index.json")
        index_data = load_json(index_path)
        actual_count = index_data.get("total_count", 0) if index_data else 0
        
        ai_index_count = found_counts[0]
        print(f"ai-index声明: {ai_index_count}条")
        print(f"实际资源数: {actual_count}条")
        
        if ai_index_count != actual_count:
            issues.append(f"ai-index资源数量声明错误: {ai_index_count} != {actual_count}")
    
    # 检查JSON引用
    if "content_index.json" not in content:
        issues.append("ai-index.html未引用content_index.json")
    else:
        print("✅ 已引用content_index.json")
    
    if issues:
        print(f"\n❌ 发现{len(issues)}个问题")
        for issue in issues:
            print(f"  - {issue}")
        return False, issues
    else:
        print("\n✅ ai-index.html 检查通过")
        return True, []

def check_shard_indexes():
    """检查分片索引"""
    print("\n" + "="*60)
    print("检查分片索引")
    print("="*60)
    
    indexes_dir = os.path.join(PROJECT_DIR, "static", "indexes")
    
    if not os.path.exists(indexes_dir):
        print("❌ 分片索引目录不存在")
        return False, ["static/indexes目录不存在"]
    
    # 期望的分片文件
    expected_shards = [
        "ai_tools_index.json",
        "code_templates_index.json",
        "faq_docs_index.json",
        "free_api_index.json",
        "tech_tutorials_index.json",
        "resources_index.json",
        "deploy_guides_index.json",
        "compliance_docs_index.json"
    ]
    
    issues = []
    existing_shards = []
    
    for shard in expected_shards:
        shard_path = os.path.join(indexes_dir, shard)
        if os.path.exists(shard_path):
            existing_shards.append(shard)
            data = load_json(shard_path)
            if data:
                count = data.get("count", 0)
                type_name = data.get("type", "未知")
                print(f"✅ {shard}: {type_name} ({count}条)")
        else:
            issues.append(f"缺少分片文件: {shard}")
            print(f"❌ {shard}: 文件不存在")
    
    print(f"\n📊 分片索引统计: {len(existing_shards)}/{len(expected_shards)}")
    
    if issues:
        print(f"\n❌ 发现{len(issues)}个问题")
        return False, issues
    else:
        print("\n✅ 分片索引检查通过")
        return True, []

def generate_report(results):
    """生成检查报告"""
    report_path = os.path.join(PROJECT_DIR, f"data_consistency_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("数据一致性检查报告\n")
        f.write("="*60 + "\n")
        f.write(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r[0])
        
        f.write(f"检查项目: {total_checks}个\n")
        f.write(f"通过: {passed_checks}个\n")
        f.write(f"失败: {total_checks - passed_checks}个\n\n")
        
        for check_name, (passed, issues) in results.items():
            status = "✅ 通过" if passed else "❌ 失败"
            f.write(f"\n{status} - {check_name}\n")
            if issues:
                for issue in issues:
                    f.write(f"  - {issue}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("报告结束\n")
        f.write("="*60 + "\n")
    
    return report_path

def main():
    """主函数"""
    print("="*60)
    print("AI-Vent-Share 数据一致性检查")
    print("="*60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目目录: {PROJECT_DIR}")
    
    results = {}
    
    # 执行各项检查
    results["content_index.json"] = check_content_index()
    results["README.md"] = check_readme()
    results["ai-index.html"] = check_ai_index()
    results["分片索引"] = check_shard_indexes()
    
    # 生成报告
    report_path = generate_report(results)
    
    # 总结
    print("\n" + "="*60)
    print("检查总结")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r[0])
    
    print(f"总检查项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    
    if passed == total:
        print("\n✅ 所有检查通过！数据一致性良好。")
    else:
        print(f"\n⚠️  发现{total - passed}项检查失败，请查看报告修复问题。")
    
    print(f"\n📄 报告已保存: {report_path}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
