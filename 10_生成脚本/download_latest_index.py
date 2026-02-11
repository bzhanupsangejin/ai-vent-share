import urllib.request
import ssl
import json

# 忽略SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://bzhanupsangejin.github.io/ai-vent-share/content_index.json"
output = r"C:\Users\HYX\Desktop\AI网站\content_index.json"

print("下载最新的content_index.json...")
print(f"URL: {url}")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        content = response.read().decode('utf-8')
    
    # 验证JSON格式
    data = json.loads(content)
    
    # 保存文件
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 下载成功！")
    print(f"版本: {data.get('version')}")
    print(f"总数: {data.get('total_count')}")
    print(f"分类: {data.get('categories', data.get('content_types'))}")
    print(f"保存位置: {output}")
    
except Exception as e:
    print(f"❌ 下载失败: {e}")
