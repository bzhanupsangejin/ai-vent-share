#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元数据部署验证脚本
用于验证GitHub Pages部署后，元数据文件是否可正常访问
"""
import requests
import json

def verify_meta_deployment():
    """验证元数据文件部署状态"""
    print("=" * 70)
    print("元数据部署验证")
    print("=" * 70)
    
    # 待验证的线上元数据地址
    url_list = [
        "https://bzhanupsangejin.github.io/ai-vent-share/static/meta/function_boundary.json",
        "https://bzhanupsangejin.github.io/ai-vent-share/static/meta/usage_guide.json",
        "https://bzhanupsangejin.github.io/ai-vent-share/static/meta/operation_meta.json"
    ]
    
    success_count = 0
    fail_count = 0
    
    # 批量校验访问状态
    for url in url_list:
        file_name = url.split("/")[-1]
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            
            # 验证JSON格式
            data = json.loads(resp.text)
            
            print(f"✅ {file_name}")
            print(f"   URL: {url}")
            print(f"   状态码: {resp.status_code}")
            print(f"   大小: {len(resp.text)} 字节")
            print(f"   JSON格式: 正确")
            print()
            
            success_count += 1
        except requests.exceptions.Timeout:
            print(f"❌ {file_name}")
            print(f"   URL: {url}")
            print(f"   错误: 请求超时（可能GitHub Pages尚未同步）")
            print()
            fail_count += 1
        except requests.exceptions.HTTPError as e:
            print(f"❌ {file_name}")
            print(f"   URL: {url}")
            print(f"   错误: HTTP {e.response.status_code}（文件不存在或未部署）")
            print()
            fail_count += 1
        except json.JSONDecodeError:
            print(f"❌ {file_name}")
            print(f"   URL: {url}")
            print(f"   错误: JSON格式错误")
            print()
            fail_count += 1
        except Exception as e:
            print(f"❌ {file_name}")
            print(f"   URL: {url}")
            print(f"   错误: {str(e)}")
            print()
            fail_count += 1
    
    # 输出总结
    print("=" * 70)
    print(f"验证完成：成功 {success_count} 个，失败 {fail_count} 个")
    print("=" * 70)
    
    if fail_count > 0:
        print("\n⚠️ 提示：")
        print("1. 如果刚推送代码，请等待1-3分钟后重试（GitHub Pages需要同步时间）")
        print("2. 确认代码已成功推送到GitHub")
        print("3. 检查GitHub仓库的Actions是否执行成功")
        print("\n重新验证命令：python scripts/verify_meta_deployment.py")
    else:
        print("\n🎉 所有元数据文件部署成功！")
        print("AI可以正常访问这些元数据文件了。")

if __name__ == "__main__":
    verify_meta_deployment()
