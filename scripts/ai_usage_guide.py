#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

def show_ai_guide(scene: str = "all"):
    """阶跃AI专用操作指引，输入scene可过滤场景"""
    # 标准化元数据访问路径，与目录结构完全匹配
    url = "https://bzhanupsangejin.github.io/ai-vent-share/static/meta/usage_guide.json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        guide = json.loads(resp.text)
    except Exception as e:
        print(f"❌ 获取指引失败：{e}")
        return
    
    print("=== AI-Vent-Share 标准化操作指引 ===")
    if scene == "all" or scene == "retrieve":
        print("\n【场景1：检索指定分类资源】")
        for step in guide["ai_operation_guide"][0]["steps"]:
            print(f"- {step}")
        print(f"示例代码：\n{guide['ai_operation_guide'][0]['example_code']}")
    
    if scene == "all" or scene == "submit":
        print("\n【场景2：提交新内容】")
        for step in guide["ai_operation_guide"][1]["steps"]:
            print(f"- {step}")

if __name__ == "__main__":
    # 阶跃AI直接运行，展示全量指引
    show_ai_guide()
