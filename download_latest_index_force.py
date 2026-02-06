import urllib.request
import ssl
import os

# 忽略SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# GitHub Raw URL（绕过Pages缓存）
url = "https://raw.githubusercontent.com/bzhanupsangejin/ai-vent-share/main/content_index.json"
output = r"C:\Users\HYX\Desktop\AI网站\static\content_index.json"

# 确保目录存在
os.makedirs(os.path.dirname(output), exist_ok=True)

print("强制下载最新主索引...")
print(f"URL: {url}")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        content = response.read()
    
    # 保存文件
    with open(output, 'wb') as f:
        f.write(content)
    
    # 验证
    import json
    with open(output, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n✅ 主索引已强制更新")
    print(f"版本: {data.get('version')}")
    print(f"总数: {data.get('total_count')}")
    print(f"分类: {len(data.get('categories', []))}个")
    print(f"保存位置: {output}")
    
except Exception as e:
    print(f"❌ 下载失败: {e}")
    print("\n尝试备用方案...")
    
    # 备用：从Pages下载
    url2 = "https://bzhanupsangejin.github.io/ai-vent-share/content_index.json"
    try:
        req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            content = response.read()
        
        with open(output, 'wb') as f:
            f.write(content)
        
        import json
        with open(output, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ 备用方案成功")
        print(f"版本: {data.get('version')}")
        print(f"总数: {data.get('total_count')}")
        
    except Exception as e2:
        print(f"❌ 备用方案也失败: {e2}")
