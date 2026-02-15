#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规性检查脚本
功能：检查所有资源是否符合中国法律法规
设计原则：关键词过滤 | 敏感信息检测 | 生成合规报告
"""
import json
import os
import re
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 硬编码法律条款（源自宪法+网络安全法）
FORBIDDEN_WORDS = [
    "危害国家安全",
    "窃取个人信息",
    "网络攻击",
    "非法获取数据",
    "侵犯隐私",
    "颠覆国家",
    "分裂国家",
    "恐怖活动",
    "极端主义",
    "传播谣言",
    "虚假信息",
    "网络诈骗",
    "黑客攻击",
    "病毒传播",
    "恶意软件",
    "非法入侵",
    "数据泄露",
    "隐私侵犯",
    "人肉搜索",
    "网络暴力"
]

SENSITIVE_PATTERNS = [
    r'\d{18}',  # 身份证号
    r'1[3-9]\d{9}',  # 手机号
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱
    r'\d{16,19}',  # 银行卡号
]

def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载失败 {filepath}: {e}")
        return None

def check_forbidden_words(text, resource_title):
    """检查禁用词"""
    violations = []
    text_lower = text.lower()
    
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            violations.append({
                "type": "禁用词",
                "content": word,
                "resource": resource_title
            })
    
    return violations

def check_sensitive_info(text, resource_title):
    """检查敏感信息"""
    violations = []
    
    for pattern in SENSITIVE_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            violations.append({
                "type": "敏感信息",
                "content": match[:10] + "..." if len(match) > 10 else match,
                "resource": resource_title
            })
    
    return violations

def check_resource_compliance(resource):
    """检查单个资源的合规性"""
    violations = []
    
    # 检查标题
    title = resource.get("title", "")
    violations.extend(check_forbidden_words(title, title))
    violations.extend(check_sensitive_info(title, title))
    
    # 检查摘要
    summary = resource.get("summary", "")
    violations.extend(check_forbidden_words(summary, title))
    violations.extend(check_sensitive_info(summary, title))
    
    # 检查关键词
    keywords = resource.get("keywords", "")
    violations.extend(check_forbidden_words(keywords, title))
    
    # 检查compliance_status字段
    compliance_status = resource.get("compliance_status", "")
    if "通过" not in compliance_status and "合规" not in compliance_status:
        violations.append({
            "type": "合规状态异常",
            "content": f"compliance_status='{compliance_status}'",
            "resource": title
        })
    
    return violations

def check_content_index():
    """检查主索引合规性"""
    print("\n" + "="*60)
    print("检查 content_index.json 合规性")
    print("="*60)
    
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    data = load_json(filepath)
    
    if not data:
        return False, []
    
    all_violations = []
    index = data.get("index", [])
    
    print(f"📊 检查资源数: {len(index)}条")
    
    for i, resource in enumerate(index):
        violations = check_resource_compliance(resource)
        all_violations.extend(violations)
        
        if (i + 1) % 50 == 0:
            print(f"  已检查 {i + 1}/{len(index)} 条...")
    
    print(f"\n📋 检查结果:")
    print(f"  - 检查资源: {len(index)}条")
    print(f"  - 违规发现: {len(all_violations)}处")
    
    if all_violations:
        print(f"\n⚠️  发现违规内容:")
        for v in all_violations[:10]:  # 只显示前10个
            print(f"  [{v['type']}] {v['content']}")
            print(f"    资源: {v['resource'][:50]}...")
        
        if len(all_violations) > 10:
            print(f"  ... 还有 {len(all_violations) - 10} 处违规")
        
        return False, all_violations
    else:
        print("\n✅ 所有资源合规性检查通过")
        return True, []

def check_legal_documents():
    """检查法律文档完整性"""
    print("\n" + "="*60)
    print("检查法律文档完整性")
    print("="*60)
    
    legal_dir = os.path.join(PROJECT_DIR, "法律文档")
    
    required_docs = [
        "中华人民共和国宪法.txt",
        "中华人民共和国网络安全法.txt",
        "社会主义核心价值观官方权威解释全文_v1_20260203.txt"
    ]
    
    missing = []
    existing = []
    
    for doc in required_docs:
        doc_path = os.path.join(legal_dir, doc)
        if os.path.exists(doc_path):
            existing.append(doc)
            print(f"✅ {doc}")
        else:
            missing.append(doc)
            print(f"❌ {doc} - 缺失")
    
    if missing:
        return False, [f"缺少法律文档: {', '.join(missing)}"]
    else:
        print("\n✅ 所有法律文档齐全")
        return True, []

def check_core_values():
    """检查核心价值观关键词"""
    print("\n" + "="*60)
    print("检查核心价值观体现")
    print("="*60)
    
    core_values = [
        "富强", "民主", "文明", "和谐",
        "自由", "平等", "公正", "法治",
        "爱国", "敬业", "诚信", "友善"
    ]
    
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    data = load_json(filepath)
    
    if not data:
        return False, []
    
    # 读取所有文本
    all_text = ""
    for resource in data.get("index", []):
        all_text += resource.get("title", "") + " "
        all_text += resource.get("summary", "") + " "
        all_text += resource.get("keywords", "")
    
    found_values = []
    for value in core_values:
        if value in all_text:
            found_values.append(value)
    
    print(f"📊 发现核心价值观关键词: {len(found_values)}/12")
    print(f"  {', '.join(found_values)}")
    
    # 检查合规说明类资源
    compliance_resources = [
        r for r in data.get("index", [])
        if r.get("content_type") == "合规说明"
    ]
    
    print(f"\n📋 合规说明类资源: {len(compliance_resources)}条")
    for r in compliance_resources[:3]:
        print(f"  - {r.get('title', '无标题')}")
    
    print("\n✅ 核心价值观检查完成")
    return True, []

def generate_report(results, violations):
    """生成合规性检查报告"""
    report_path = os.path.join(PROJECT_DIR, f"compliance_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("合规性检查报告\n")
        f.write("="*60 + "\n")
        f.write(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"检查标准: 《宪法》《网络安全法》《社会主义核心价值观》\n\n")
        
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r[0])
        
        f.write(f"检查项目: {total_checks}个\n")
        f.write(f"通过: {passed_checks}个\n")
        f.write(f"失败: {total_checks - passed_checks}个\n\n")
        
        for check_name, (passed, issues) in results.items():
            status = "✅ 通过" if passed else "❌ 失败"
            f.write(f"\n{status} - {check_name}\n")
            if issues:
                for issue in issues[:20]:  # 最多显示20个
                    if isinstance(issue, dict):
                        f.write(f"  - [{issue['type']}] {issue['content']}\n")
                        f.write(f"    资源: {issue['resource'][:60]}\n")
                    else:
                        f.write(f"  - {issue}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("禁用词列表:\n")
        for word in FORBIDDEN_WORDS:
            f.write(f"  - {word}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("报告结束\n")
        f.write("="*60 + "\n")
    
    return report_path

def main():
    """主函数"""
    print("="*60)
    print("AI-Vent-Share 合规性检查")
    print("="*60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"检查标准:")
    print(f"  - 《中华人民共和国宪法》")
    print(f"  - 《中华人民共和国网络安全法》")
    print(f"  - 《社会主义核心价值观》")
    
    results = {}
    all_violations = []
    
    # 执行各项检查
    passed, violations = check_content_index()
    results["资源内容合规性"] = (passed, violations)
    all_violations.extend(violations)
    
    passed, violations = check_legal_documents()
    results["法律文档完整性"] = (passed, violations)
    
    passed, violations = check_core_values()
    results["核心价值观体现"] = (passed, violations)
    
    # 生成报告
    report_path = generate_report(results, all_violations)
    
    # 总结
    print("\n" + "="*60)
    print("检查总结")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r[0])
    
    print(f"总检查项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"违规发现: {len(all_violations)}处")
    
    if len(all_violations) == 0:
        print("\n✅ 所有资源符合中国法律法规！")
    else:
        print(f"\n⚠️  发现{len(all_violations)}处违规，请查看报告并修复。")
    
    print(f"\n📄 报告已保存: {report_path}")
    
    return len(all_violations) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
