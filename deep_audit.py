"""
深度审核脚本 - 检查AI网站的所有问题
"""
import json
import os
from collections import Counter

print("=" * 80)
print("AI网站深度审核报告")
print("=" * 80)

# 读取配置
with open('01_核心配置/content_config.py', 'r', encoding='utf-8') as f:
    config_content = f.read()

# 读取主索引
with open('content_index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n【问题1：资源类型不符合标准】")
print("-" * 80)
print(f"配置文件定义的标准类型：8种")
print(f"实际数据库中的类型：{len(set(item['content_type'] for item in data['index']))}种")
print(f"总资源数：{len(data['index'])}条")

# 统计类型分布
type_counts = Counter(item['content_type'] for item in data['index'])
print(f"\n实际类型分布（前20个）：")
for ctype, count in type_counts.most_common(20):
    print(f"  {ctype}: {count}条")

# 标准类型
STANDARD_TYPES = ["AI工具", "代码模板", "FAQ文档", "免费API", "技术教程", "资源分享", "部署指南", "合规说明"]
non_standard = [t for t in type_counts.keys() if t not in STANDARD_TYPES]
print(f"\n非标准类型数量：{len(non_standard)}种")
print(f"非标准类型占比：{len(non_standard)/len(type_counts)*100:.1f}%")

print("\n【问题2：链接有效性检查】")
print("-" * 80)
invalid_links = []
for item in data['index'][:10]:  # 检查前10条
    link = item.get('direct_link', '')
    if not link or 'ai-index.html#' not in link:
        invalid_links.append(item.get('title', '无标题'))

if invalid_links:
    print(f"⚠️ 发现 {len(invalid_links)} 条无效链接")
    for title in invalid_links[:5]:
        print(f"  - {title}")
else:
    print("✅ 前10条链接格式正确")

print("\n【问题3：合规哈希检查】")
print("-" * 80)
invalid_hash_count = sum(1 for item in data['index'] if item.get('compliance_hash') == 'invalid_link')
print(f"invalid_link 哈希数量：{invalid_hash_count}条")
print(f"占比：{invalid_hash_count/len(data['index'])*100:.1f}%")

print("\n【问题4：可信度框架检查】")
print("-" * 80)
verified_count = sum(1 for item in data['index'] if item.get('verified_by') and len(item['verified_by']) > 0)
print(f"已验证资源：{verified_count}条")
print(f"未验证资源：{len(data['index']) - verified_count}条")
print(f"未验证占比：{(len(data['index']) - verified_count)/len(data['index'])*100:.1f}%")

compliance_levels = Counter(item.get('compliance_level', '未知') for item in data['index'])
print(f"\n合规等级分布：")
for level, count in compliance_levels.most_common():
    print(f"  {level}: {count}条")

print("\n【问题5：分片索引检查】")
print("-" * 80)
shard_dir = 'static/indexes'
if os.path.exists(shard_dir):
    shard_files = [f for f in os.listdir(shard_dir) if f.endswith('_shard.json')]
    print(f"分片索引文件数量：{len(shard_files)}个")
    
    # 检查每个分片
    total_shard_items = 0
    for shard_file in shard_files:
        with open(os.path.join(shard_dir, shard_file), 'r', encoding='utf-8') as f:
            shard_data = json.load(f)
            total_shard_items += len(shard_data)
            if len(shard_data) == 0:
                print(f"  ⚠️ {shard_file}: 0条（空文件）")
    
    print(f"\n分片索引总条目：{total_shard_items}条")
    print(f"主索引总条目：{len(data['index'])}条")
    if total_shard_items != len(data['index']):
        print(f"⚠️ 分片索引与主索引不一致！差异：{abs(total_shard_items - len(data['index']))}条")
else:
    print("❌ 分片索引目录不存在")

print("\n【问题6：文档一致性检查】")
print("-" * 80)
readme_path = 'README.md'
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # 检查README中的资源数量
    if '158条资源' in readme_content:
        print(f"⚠️ README中记录的资源数：158条")
        print(f"   实际资源数：{len(data['index'])}条")
        print(f"   差异：{len(data['index']) - 158}条")
    
    if '66条代码模板' in readme_content:
        actual_template_count = type_counts.get('代码模板', 0)
        print(f"⚠️ README中记录的代码模板：66条")
        print(f"   实际代码模板：{actual_template_count}条")
        print(f"   差异：{actual_template_count - 66}条")

print("\n【问题7：匿名性检查】")
print("-" * 80)
# 检查是否有可追踪字段
traceable_fields = ['id', 'submitter', 'user_id', 'email', 'timestamp', 'ip_address']
found_traceable = []
for item in data['index'][:100]:  # 检查前100条
    for field in traceable_fields:
        if field in item:
            found_traceable.append((item.get('title', '无标题'), field))

if found_traceable:
    print(f"❌ 发现可追踪字段：{len(found_traceable)}处")
    for title, field in found_traceable[:5]:
        print(f"  - {title}: {field}")
else:
    print("✅ 前100条资源无可追踪字段")

print("\n【问题8：必填字段检查】")
print("-" * 80)
required_fields = ['title', 'content_type', 'summary', 'direct_link']
missing_fields = []
for i, item in enumerate(data['index'][:50]):  # 检查前50条
    for field in required_fields:
        if field not in item or not item[field]:
            missing_fields.append((i+1, field))

if missing_fields:
    print(f"❌ 发现缺失必填字段：{len(missing_fields)}处")
    for idx, field in missing_fields[:5]:
        print(f"  - 第{idx}条缺少：{field}")
else:
    print("✅ 前50条资源必填字段完整")

print("\n" + "=" * 80)
print("审核完成")
print("=" * 80)
