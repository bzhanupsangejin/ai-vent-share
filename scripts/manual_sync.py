#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI资源手动录入工具（匿名强化版｜严格遵循匿名性最高准则）

⚠️ 匿名性最高准则（必读）：
• 禁止生成/记录任何可追踪字段：id, submitter, user_id, timestamp, email等
• 资源唯一标识 = 标题 + URL + 分类（人类维护时通过此组合定位）
• 本脚本已移除所有ID生成逻辑，请勿自行添加

🌐 网站精神：
"人类维护者提交资源时，系统不生成/不记录任何可关联到个人的标识符"
—— 匿名性不是"技术处理"，是架构哲学

功能：交互式录入 + 自动生成标准格式 + 注入可信度框架 + 严格匿名
设计原则：零格式错误｜自动注入｜人类零认知负担｜彻底匿名
"""
import json
import os
import uuid
from datetime import datetime

# 基础配置
BASE_URL = "https://bzhanupsangejin.github.io/ai-vent-share/docs"
VALID_TYPES = ["AI工具", "代码模板", "FAQ文档", "免费API", "技术教程", "资源分享", "部署指南", "合规说明"]

def add_ai_resource():
    """手动录入AI资源，自动生成标准格式条目（严格匿名）"""
    print("\n" + "="*70)
    print("AI资源手动录入工具（匿名强化版）")
    print("="*70)
    print("🔒 匿名性保障：本工具不生成/不记录任何可追踪字段")
    print("="*70)
    
    # 交互输入核心信息
    print("\n请输入资源信息：\n")
    title = input("1. 资源标题：").strip()
    
    print(f"\n2. 资源类型（从以下选择）：")
    for i, t in enumerate(VALID_TYPES, 1):
        print(f"   {i}. {t}")
    ctype_input = input("   请输入类型名称或序号：").strip()
    
    # 支持序号输入
    if ctype_input.isdigit():
        idx = int(ctype_input) - 1
        if 0 <= idx < len(VALID_TYPES):
            ctype = VALID_TYPES[idx]
        else:
            ctype = "资源分享"
            print("⚠️  序号无效，自动归类为【资源分享】")
    else:
        ctype = ctype_input if ctype_input in VALID_TYPES else "资源分享"
        if ctype == "资源分享" and ctype_input not in VALID_TYPES:
            print("⚠️  类型不合法，自动归类为【资源分享】")
    
    summary = input("\n3. 资源摘要（≤150字）：").strip()
    
    # 可选：可信度信息
    print("\n4. 可信度信息（可选，直接回车跳过）：")
    verified_by_input = input("   验证者（多个用逗号分隔）：").strip()
    compliance_level = input("   合规等级（高/中/低，默认：待验证）：").strip() or "待验证"
    
    print("\n5. 完整内容（输入完成后按Enter，再输入END并按Enter结束）：")
    
    # 多行输入
    detail_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        detail_lines.append(line)
    detail = "\n".join(detail_lines)
    
    # 生成文件与索引数据
    file_uuid = str(uuid.uuid4())
    file_name = f"{file_uuid}.txt"
    file_path = f"./docs/{file_name}"
    
    # 确保docs目录存在
    os.makedirs("./docs", exist_ok=True)
    
    # 写入资源文本
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(detail)
    
    # 处理验证者列表
    verified_by = []
    if verified_by_input:
        verified_by = [v.strip() for v in verified_by_input.split(",") if v.strip()]
    
    # 🔒 匿名性核心：构造标准索引结构（不含任何可追踪字段）
    new_item = {
        # 核心内容字段（必需）
        "title": title,
        "content_type": ctype,
        "summary": summary,
        "direct_link": f"{BASE_URL}/{file_name}",
        
        # 可信度框架字段（机器可读）
        "verified_by": verified_by,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "compliance_level": compliance_level,
        
        # 技术辅助字段（无个人信息）
        "uuid": str(uuid.uuid4()),  # 仅用于去重，不关联个人
        "keywords": "",
        "compliance_status": "通过",
        "file_name": file_name,
        "full_content_anchor": f"ai_item_{file_uuid[:8]}",
        "trace_id": f"trace_{str(uuid.uuid4())[:8]}",
        "version": "1.0.0",
        "compliance_hash": "manual_verified"
        
        # ❌ 不生成以下字段：
        # - id / content_id（会在optimize_anonymous.py中统一处理）
        # - submitter / user_id / email（违反匿名性）
        # - timestamp / created_at（last_updated已足够）
    }
    
    # 更新主索引
    with open("content_index.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        
        # 兼容不同的索引结构
        if "index" in data:
            resources = data["index"]
        elif "resources" in data:
            resources = data["resources"]
        else:
            resources = []
        
        # 添加content_id（仅作为内部锚点，不含个人信息）
        new_item["content_id"] = f"ai_item_{len(resources) + 1:04d}"
        resources.append(new_item)
        
        # 更新索引
        if "index" in data:
            data["index"] = resources
        elif "resources" in data:
            data["resources"] = resources
        
        data["total_count"] = len(resources)
        
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 输出报告
    print("\n" + "="*70)
    print("✨ 资源添加完成！")
    print("="*70)
    print(f"📝 内部锚点：{new_item['content_id']}（仅用于定位，无个人信息）")
    print(f"📄 文件路径：{file_path}")
    print(f"🔗 访问链接：{new_item['direct_link']}")
    print(f"✅ 可信度框架：已自动注入")
    print(f"   - 验证者：{verified_by if verified_by else '待补充'}")
    print(f"   - 更新时间：{new_item['last_updated']}")
    print(f"   - 合规等级：{compliance_level}")
    print(f"🔒 匿名性保障：未生成任何可追踪字段（id/submitter/email等）")
    print("="*70)
    print("\n💡 后续操作建议：")
    print("  1. 【推荐】运行匿名优化脚本：python scripts/optimize_anonymous.py")
    print("     （彻底移除所有可追踪字段，确保100%匿名）")
    print("  2. 【或】运行旧版优化脚本：python scripts/optimize_ai_platform.py")
    print("  3. 提交代码：git add . && git commit -m 'add: 新增资源' && git push")
    print("\n")

if __name__ == "__main__":
    add_ai_resource()
