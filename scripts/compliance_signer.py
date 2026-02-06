#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规哈希签名脚本
功能：为所有资源生成合规哈希，支持机器自主核验
"""
import json
import hashlib
import os


def compute_compliance_hash(content: str) -> str:
    """生成内容合规哈希，用于机器校验"""
    # 清理内容（去除空白字符）
    cleaned = content.strip().replace("\n", "").replace(" ", "").replace("\r", "")
    # 生成MD5哈希（轻量化适配）
    return hashlib.md5(cleaned.encode("utf-8")).hexdigest()


def sign_all_resources():
    """为所有资源生成合规哈希签名"""
    print("=" * 60)
    print("合规哈希签名脚本")
    print("=" * 60)
    print()
    
    # 读取主索引
    index_file = "content_index.json"
    if not os.path.exists(index_file):
        print(f"❌ 错误：{index_file} 文件不存在")
        return
    
    with open(index_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    contents = data.get("index", [])
    print(f"✅ 读取主索引: {len(contents)} 条")
    print()
    
    # 为每个资源生成合规哈希
    print("【生成合规哈希】")
    signed_count = 0
    failed_count = 0
    hash_chain = {}
    
    for item in contents:
        uuid_val = item.get("uuid", "")
        direct_link = item.get("direct_link", "")
        
        # 尝试读取文件内容
        if direct_link and direct_link.startswith("./"):
            file_path = direct_link[2:]  # 去掉 ./
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 生成哈希
                    hash_value = compute_compliance_hash(content)
                    item["compliance_hash"] = hash_value
                    hash_chain[uuid_val] = hash_value
                    signed_count += 1
                    
                except Exception as e:
                    item["compliance_hash"] = "read_error"
                    failed_count += 1
                    print(f"  ⚠️  读取失败: {file_path}")
            else:
                item["compliance_hash"] = "file_not_found"
                failed_count += 1
        else:
            item["compliance_hash"] = "invalid_link"
            failed_count += 1
    
    print(f"  ✅ 成功签名: {signed_count} 条")
    if failed_count > 0:
        print(f"  ⚠️  失败/跳过: {failed_count} 条")
    print()
    
    # 保存哈希链
    print("【保存哈希链】")
    os.makedirs("static/compliance", exist_ok=True)
    
    with open("static/compliance/hash_chain.json", "w", encoding="utf-8") as f:
        json.dump({
            "total": len(hash_chain),
            "algorithm": "md5",
            "purpose": "机器自主合规核验",
            "chain": hash_chain
        }, f, ensure_ascii=False, indent=2)
    print(f"  ✅ hash_chain.json ({len(hash_chain)} 条)")
    print()
    
    # 回写主索引
    print("【更新主索引】")
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {index_file} 已更新")
    print()
    
    print("=" * 60)
    print("✅ 合规哈希签名完成")
    print("=" * 60)
    print()
    print("🎯 AI核验方式：")
    print("   1. 下载 /static/compliance/hash_chain.json")
    print("   2. 本地计算文件MD5哈希")
    print("   3. 与hash_chain中的值比对")
    print("   4. 一致则通过合规校验")


if __name__ == "__main__":
    sign_all_resources()
