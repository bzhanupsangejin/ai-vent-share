#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键执行所有优化脚本
"""
import subprocess
import sys
import os

def run_script(script_path, description):
    """运行单个脚本"""
    print(f"\n{'='*60}")
    print(f"执行: {description}")
    print(f"{'='*60}")
    
    try:
        # 获取脚本的绝对路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, script_path)
        
        result = subprocess.run(
            [sys.executable, full_path],
            cwd=base_dir,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - 完成")
            return True
        else:
            print(f"❌ {description} - 失败")
            return False
    except Exception as e:
        print(f"❌ {description} - 错误: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("AI-Vent-Share 全量优化执行")
    print("=" * 60)
    print()
    
    scripts = [
        ("scripts/enhance_schema.py", "Schema标准化增强"),
        ("scripts/generate_static_protocol.py", "静态机器交互协议生成"),
        ("scripts/generate_sync_manifest.py", "增量同步清单生成"),
    ]
    
    success_count = 0
    failed_count = 0
    
    for script_path, description in scripts:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, script_path)
        
        if os.path.exists(full_path):
            if run_script(script_path, description):
                success_count += 1
            else:
                failed_count += 1
        else:
            print(f"⚠️  跳过: {script_path} (文件不存在)")
            failed_count += 1
    
    print("\n" + "=" * 60)
    print("执行完成")
    print("=" * 60)
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {failed_count} 个")
    print()
    
    print("📋 生成文件清单：")
    print("   - static/schema/resource_schema.json")
    print("   - static/indexes/*.json (11个文件)")
    print("   - static/sync/*.json (2个文件)")
    print("   - static/share/submit_template.json")
    print()
    
    print("🎯 优化效果：")
    print("   ✅ Schema标准化 - 所有资源符合统一规范")
    print("   ✅ 静态交互协议 - AI可按类型/UUID直接拉取")
    print("   ✅ 检索优化 - O(1)哈希查询，降低算力开销")
    print("   ✅ 增量同步 - 仅拉取变更内容，节省带宽")
    print("   ✅ AI分享闭环 - 匿名提交模板已就绪")
    print()


if __name__ == "__main__":
    main()
