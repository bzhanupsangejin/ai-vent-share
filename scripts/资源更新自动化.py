#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源更新后的自动化任务（一键执行）

执行顺序：
1. 运行匿名化优化脚本（optimize_anonymous.py）
2. 运行RSS生成脚本（generate_rss.py）
3. 验证RSS文件
4. 提示Git提交命令

设计原则：自动化｜零遗漏｜实时反馈
"""
import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

# 尝试导入requests，如果失败则跳过线上验证
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def print_section(title):
    """打印分隔线"""
    print("\n" + "="*70)
    print(title)
    print("="*70)

def run_script(script_path, script_name):
    """运行Python脚本"""
    print(f"\n🔧 正在运行: {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} 执行成功")
            # 显示输出的关键信息
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if '✅' in line or '📊' in line or '总资源数' in line or 'RSS' in line:
                    print(f"   {line}")
            return True
        else:
            print(f"❌ {script_name} 执行失败")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 运行 {script_name} 时出错: {e}")
        return False

def validate_rss_local():
    """验证本地RSS文件"""
    print("\n🔍 验证本地RSS文件...")
    try:
        if not os.path.exists("rss.xml"):
            print("❌ rss.xml 文件不存在")
            return False
        
        # 解析XML
        tree = ET.parse("rss.xml")
        root = tree.getroot()
        
        # 检查基本结构
        if root.tag != 'rss':
            print("❌ 根元素不是<rss>")
            return False
        
        channel = root.find('channel')
        if channel is None:
            print("❌ 缺少<channel>元素")
            return False
        
        # 检查必需字段
        title = channel.find('title')
        link = channel.find('link')
        description = channel.find('description')
        lastBuildDate = channel.find('lastBuildDate')
        
        if title is None or link is None or description is None:
            print("❌ 缺少必需字段（title/link/description）")
            return False
        
        # 统计item数量
        items = channel.findall('item')
        
        print(f"✅ RSS文件格式正确")
        print(f"   - 标题: {title.text}")
        print(f"   - 链接: {link.text}")
        print(f"   - 最后更新: {lastBuildDate.text if lastBuildDate is not None else 'N/A'}")
        print(f"   - 包含条目: {len(items)}条")
        
        return True
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def validate_rss_online():
    """验证线上RSS文件（可选）"""
    if not HAS_REQUESTS:
        print("\n⚠️  跳过线上RSS验证（requests模块未安装）")
        print("   安装方法: pip install requests")
        return None
    
    print("\n🌐 验证线上RSS文件...")
    rss_url = "https://bzhanupsangejin.github.io/ai-vent-share/rss.xml"
    
    try:
        response = requests.get(rss_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ 线上RSS可访问")
            print(f"   - URL: {rss_url}")
            print(f"   - 状态码: {response.status_code}")
            print(f"   - 文件大小: {len(response.content)} 字节")
            
            # 尝试解析
            try:
                root = ET.fromstring(response.content)
                channel = root.find('channel')
                items = channel.findall('item')
                print(f"   - 包含条目: {len(items)}条")
            except:
                pass
            
            return True
        else:
            print(f"⚠️  线上RSS访问失败（状态码: {response.status_code}）")
            print(f"   可能原因: GitHub Pages尚未同步最新文件")
            return False
    except requests.exceptions.Timeout:
        print(f"⚠️  请求超时（可能GitHub Pages尚未部署）")
        return False
    except Exception as e:
        print(f"⚠️  验证失败: {e}")
        return False

def check_git_status():
    """检查Git状态"""
    print("\n📝 检查Git状态...")
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                print("✅ 检测到文件变更:")
                change_lines = changes.split('\n')
                for line in change_lines[:10]:  # 只显示前10行
                    print(f"   {line}")
                if len(change_lines) > 10:
                    remaining = len(change_lines) - 10
                    print(f"   ... 还有 {remaining} 个文件")
                return True
            else:
                print("⚠️  没有检测到文件变更")
                return False
        else:
            print("⚠️  无法检查Git状态（可能未初始化Git仓库）")
            return False
    except FileNotFoundError:
        print("⚠️  Git未安装或不在PATH中")
        return False
    except Exception as e:
        print(f"⚠️  检查Git状态失败: {e}")
        return False

def generate_git_commands():
    """生成Git提交命令"""
    print("\n📋 Git提交命令（复制执行）:")
    print("-" * 70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    commands = f"""
# 添加所有变更文件
git add .

# 提交变更（自动生成提交信息）
git commit -m "update: 资源更新 - {timestamp}"

# 推送到远程仓库
git push origin main

# 等待GitHub Pages部署（1-3分钟后验证）
# 验证地址: https://bzhanupsangejin.github.io/ai-vent-share/rss.xml
"""
    
    print(commands)
    print("-" * 70)

def main():
    """主函数"""
    print_section("资源更新后的自动化任务")
    print("🤖 自动执行: 匿名化优化 → RSS生成 → 验证 → Git提交提示")
    print("="*70)
    
    # 步骤1: 运行匿名化优化脚本
    print_section("[步骤1/4] 运行匿名化优化脚本")
    success1 = run_script("scripts/optimize_anonymous.py", "optimize_anonymous.py")
    
    if not success1:
        print("\n❌ 匿名化优化失败，终止流程")
        return
    
    # 步骤2: 运行RSS生成脚本
    print_section("[步骤2/4] 运行RSS生成脚本")
    success2 = run_script("scripts/generate_rss.py", "generate_rss.py")
    
    if not success2:
        print("\n❌ RSS生成失败，终止流程")
        return
    
    # 步骤3: 验证RSS文件
    print_section("[步骤3/4] 验证RSS文件")
    
    # 3.1 验证本地文件
    local_valid = validate_rss_local()
    
    # 3.2 验证线上文件（可选）
    online_valid = validate_rss_online()
    
    if not local_valid:
        print("\n⚠️  本地RSS文件验证失败，请检查")
    
    # 步骤4: Git提交提示
    print_section("[步骤4/4] Git提交提示")
    
    has_changes = check_git_status()
    
    if has_changes:
        generate_git_commands()
    else:
        print("\n⚠️  没有检测到文件变更，无需提交")
    
    # 最终总结
    print_section("✨ 自动化任务完成")
    
    print("\n📊 执行结果:")
    print(f"   ✅ 匿名化优化: {'成功' if success1 else '失败'}")
    print(f"   ✅ RSS生成: {'成功' if success2 else '失败'}")
    print(f"   ✅ 本地RSS验证: {'通过' if local_valid else '失败'}")
    print(f"   {'✅' if online_valid else '⚠️ '} 线上RSS验证: {'通过' if online_valid else '待部署'}")
    print(f"   {'✅' if has_changes else '⚠️ '} Git变更检测: {'有变更' if has_changes else '无变更'}")
    
    print("\n💡 后续操作:")
    if has_changes:
        print("   1. 复制上方Git命令并执行")
        print("   2. 等待GitHub Pages部署（1-3分钟）")
        print("   3. 访问RSS地址验证: https://bzhanupsangejin.github.io/ai-vent-share/rss.xml")
        print("   4. 使用RSS验证工具: https://validator.w3.org/feed/")
    else:
        print("   无需操作（没有文件变更）")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
