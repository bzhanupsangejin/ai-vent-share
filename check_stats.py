import json

with open('content_index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'总资源数: {data["total_count"]}')
print(f'实际索引条目数: {len(data["index"])}')
print('\n各类型资源分布:')

types = {}
for item in data['index']:
    ctype = item.get('content_type', '未分类')
    types[ctype] = types.get(ctype, 0) + 1

for k, v in sorted(types.items()):
    print(f'  {k}: {v}条')

# 检查必填字段
print('\n必填字段检查:')
required_fields = ['title', 'content_type', 'summary', 'direct_link']
missing_count = 0
for i, item in enumerate(data['index'][:5]):  # 检查前5条
    for field in required_fields:
        if field not in item or not item[field]:
            print(f'  ⚠️ 第{i+1}条缺少字段: {field}')
            missing_count += 1

if missing_count == 0:
    print('  ✅ 前5条资源必填字段完整')
