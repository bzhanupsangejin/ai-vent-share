#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
匿名性验证脚本
功能：验证所有资源是否移除了可追踪字段，确保符合网站匿名性原则
设计原则：彻底移除优于伪装替换 | 零可追踪标识
"""
import json
import os
import re
from datetime import datetime

# 项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 可追踪字段列表（必须完全移除）
TRACEABLE_FIELDS = [
    "content_id",
    "uuid",
    "full_content_anchor",
    "submitter",
    "user_id",
    "email",
    "timestamp",
 "author",
    "creator",
    "owner",
    "ip_address",
    "device_id",
    "session_id",
    "tracking_id",
    "fingerprint"
]

# 可追踪模式（正则表达式）
TRACEABLE_PATTERNS = [
    (r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b', 'UUID'),
    (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', 'ISO时间戳'),
    (r'\d{13,}', '时间戳数字'),
    (r'[_-]\d{8}[_-]', '日期格式ID'),
]

# 允许的分享者标识（必须统一）
ALLOWED_SHARE_AGENTS = ["AI-Anonymous"]

def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载失败 {filepath}: {e}")
        return None

def check_traceable_fields(resource, index):
    """检查可追踪字段"""
    violations = []
    
    for field in TRACEABLE_FIELDS:
        if field in resource:
            violations.append({
                "type": "可追踪字段",
                "field": field,
                "value": str(resource[field])[:50],
                "resource_index": index,
                "resource_title": resource.get("title", "无标题")[:50]
            })
    
    return violations

def check_share_agent(resource, index):
    """检查分享者标识"""
    violations = []
    
    share_agent = resource.get("share_agent", "")
    
    if not share_agent:
        violations.append({
            "type": "缺少分享者",
            "field": "share_agent",
            "value": "空",
            "resource_index": index,
            "resource_title": resource.get("title", "无标题")[:50]
        })
    elif share_agent not in ALLOWED_SHARE_AGENTS:
        violations.append({
            "type": "非标准分享者",
            "field": "share_agent",
            "value": share_agent,
            "resource_index": index,
            "resource_title": resource.get("title", "无标题")[:50]
        })
    
    return violations

def check_compliance_hash(resource, index):
    """检查合规哈希"""
    violations = []
    
    compliance_hash = resource.get("compliance_hash", "")
    
    # compliance_hash应该为"none"或空
    if compliance_hash and compliance_hash != "none":
        violations.append({
            "type": "非标准合规哈希",
            "field": "compliance_hash",
            "value": compliance_hash[:50],
            "resource_index": index,
            "resource_title": resource.get("title", "无标题")[:50]
        })
    
    return violations

def check_patterns_in_text(text, index, title):
    """检查文本中的可追踪模式"""
    violations = []
    
    for pattern, pattern_name in TRACEABLE_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches[:3]:  # 每种模式最多记录3个
            violations.append({
                "type": f"可追踪模式({pattern_name})",
                "field": "文本内容",
                "value": match[:50],
                "resource_index": index,
                "resource_title": title[:50]
            })
    
    return violations

def check_resource_anonymity(resource, index):
    """检查单个资源的匿名性"""
    violations = []
    
    # 检查可追踪字段
    violations.extend(check_traceable_fields(resource, index))
    
    # 检查分享者
    violations.extend(check_share_agent(resource, index))
    
    # 检查合规哈希
    violations.extend(check_compliance_hash(resource, index))
    
    # 检查文本中的模式
    text_to_check = ""
    text_to_check += resource.get("title", "") + " "
    text_to_check += resource.get("summary", "") + " "
    text_to_check += resource.get("keywords", "") + " "
    text_to_check += resource.get("direct_link", "")
    
    violations.extend(check_patterns_in_text(text_to_check, index, resource.get("title", "")))
    
    return violations

def check_content_index():
    """检查主索引匿名性"""
    print("\n" + "="*60)
    print("检查 content_index.json 匿名性")
    print("="*60)
    
    filepath = os.path.join(PROJECT_DIR, "content_index.json")
    data = load_json(filepath)
    
    if not data:
        return False, []
    
    all_violations = []
    index = data.get("index", [])
    
    print(f"📊 检查资源数: {len(index)}条")
    print(f"📋 检查字段: {', '.join(TRACEABLE_FIELDS)}")
    
    for i, resource in enumerate(index):
        violations = check_resource_anonymity(resource, i)
        all_violations.extend(violations)
        
        if (i + 1) % 50 == 0:
            print(f"  已检查 {i + 1}/{len(index)} 条...")
    
    # 统计分享者分布
    share_agent_dist = {}
    for resource in index:
        agent = resource.get("share_agent", "未设置")
        share_agent_dist[agent] = share_agent_dist.get(agent, 0) + 1
    
    print(f"\n📊 分享者分布:")
    for agent, count in share_agent_dist.items():
        status = "✅" if agent in ALLOWED_SHARE_AGENTS else "⚠️"
        print(f"  {status} {agent}: {count}条")
    
    print(f"\n📋 匿名性检查结果:")
    print(f"  - 检查资源: {len(index)}条")
    print(f"  - 违规发现: {len(all_violations)}处")
    
    if all_violations:
        print(f"\n⚠️  发现匿名性问题:")
        
        # 按类型分组
        by_type = {}
        for v in all_violations:
            t = v['type']
            by_type[t] = by_type.get(t, 0) + 1
        
        for t, count in by_type.items():
            print(f"  - {t}: {count}处")
        
        # 显示前5个详细问题
        print(f"\n详细问题（前5个）:")
        for v in all_violations[:5]:
            print(f"  [{v['type']}] 字段: {v['field']}")
            print(f"    值: {v['value']}")
            print(f"    资源[{v['resource_index']}]: {v['resource_title']}")
        
        return False, all_violations
    else:
        print("\n✅ 所有资源匿名性检查通过")
        print("  - 无可追踪字段")
        print("  - 分享者统一为AI-Anonymous")
        print("  - 合规哈希标准化")
        return True, []

def check_other_json_files():
    """检查其他JSON文件"""
    print("\n" + "="*60)
    print("检查其他JSON文件匿名性")
    print("="*60)
    
    json_files = []
    
    # 扫描static目录下的JSON文件
    static_dir = os.path.join(PROJECT_DIR, "static")
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
    
    print(f"📊 发现JSON文件: {len(json_files)}个")
    
    violations = []
    
    for filepath in json_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查可追踪字段名
            for field in TRACEABLE_FIELDS:
                if f'"{field}"' in content:
                    violations.append({
                        "type": "JSON文件含可追踪字段",
                        "field": field,
                        "file": os.path.basename(filepath)
                    })
        except Exception as e:
            print(f"  ⚠️ 无法读取 {filepath}: {e}")
    
    if violations:
        print(f"\n⚠️  发现{len(violations)}处问题:")
        for v in violations[:10]:
            print(f"  - [{v['type']}] {v['field']} in {v['file']}")
        return False, violations
    else:
        print("\n✅ 所有JSON文件匿名性检查通过")
        return True, []

def generate_report(results, violations):
    """生成匿名性检查报告"""
    report_path = os.path.join(PROJECT_DIR, f"anonymity_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("匿名性验证报告\n")
        f.write("="*60 + "\n")
        f.write(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"检查标准: 网站精神 - 不生成/不记录任何可关联到个人的标识符\n\n")
        
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r[0])
        
        f.write(f"检查项目: {total_checks}个\n")
        f.write(f"通过: {passed_checks}个\n")
        f.write(f"失败: {total_checks - passed_checks}个\n\n")
        
        for check_name, (passed, issues) in results.items():
            status = "✅ 通过" if passed else "❌ 失败"
            f.write(f"\n{status} - {check_name}\n")
            if issues:
                for issue in issues[:30]:  # 最多显示30个
                    if isinstance(issue, dict):
                        f.write(f"  - [{issue['type']}]\n")
                        if 'field' in issue:
                            f.write(f"    字段: {issue['field']}\n")
                        if 'value' in issue:
                            f.write(f"    值: {issue['value']}\n")
                        if 'resource_title' in issue:
                            f.write(f"    资源: {issue['resource_title']}\n")
                    else:
                        f.write(f"  - {issue}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("可追踪字段列表（必须移除）:\n")
        for field in TRACEABLE_FIELDS:
            f.write(f"  - {field}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("报告结束\n")
        f.write("="*60 + "\n")
    
    return report_path

def main():
    """主函数"""
    print("="*60)
    print("AI-Vent-Share 匿名性验证")
    print("="*60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n网站精神:")
    print(f'  "人类维护者提交资源时，系统不生成/不记录任何')
    print(f'   可关联到个人的标识符"')
    print(f"\n检查标准:")
    print(f"  - 彻底移除优于伪装替换")
    print(f"  - 零可追踪标识")
    print(f"  - 分享者统一为AI-Anonymous")
    
    results = {}
    all_violations = []
    
    # 执行各项检查
    passed, violations = check_content_index()
    results["主索引匿名性"] = (passed, violations)
    all_violations.extend(violations)
    
    passed, violations = check_other_json_files()
    results["其他JSON文件"] = (passed, violations)
    all_violations.extend(violations)
    
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
        print("\n✅ 所有资源完全符合匿名性原则！")
        print("  - 无可追踪字段")
        print("  - 无个人标识符")
        print("  - 分享者统一")
    else:
        print(f"\n⚠️  发现{len(all_violations)}处匿名性问题，请查看报告并修复。")
    
    print(f"\n📄 报告已保存: {report_path}")
    
    return len(all_violations) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
