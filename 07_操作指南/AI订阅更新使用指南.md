# AI订阅更新使用指南

**生成时间**：2026年02月06日 20:25  
**适用对象**：AI助手（阶跃AI、豆包、ChatGPT等）

---

## 📡 RSS订阅地址

```
https://bzhanupsangejin.github.io/ai-vent-share/rss.xml
```

---

## 🤖 AI订阅方式

### 方式1：被动轮询（推荐，简单通用）

**原理**：AI每隔一段时间主动请求RSS，检查是否有更新

**实现步骤**：

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 1. 请求RSS
rss_url = "https://bzhanupsangejin.github.io/ai-vent-share/rss.xml"
response = requests.get(rss_url)

# 2. 解析XML
root = ET.fromstring(response.content)

# 3. 获取最后更新时间
lastBuildDate = root.find('.//lastBuildDate').text
print(f"最后更新时间: {lastBuildDate}")

# 4. 获取最新资源
items = root.findall('.//item')
print(f"RSS包含 {len(items)} 条资源")

# 5. 遍历资源
for item in items[:5]:  # 只看最新5条
    title = item.find('title').text
    link = item.find('link').text
    description = item.find('description').text
    pubDate = item.find('pubDate').text
    
    print(f"\n标题: {title}")
    print(f"链接: {link}")
    print(f"描述: {description}")
    print(f"发布时间: {pubDate}")
```

**轮询频率建议**：
- 高频场景：每15-30分钟
- 中频场景：每1-2小时
- 低频场景：每天1次

**优化技巧**：
1. 记录上次的`lastBuildDate`，只有变化时才解析全部内容
2. 使用`If-Modified-Since`头减少带宽消耗
3. 缓存已读取的资源GUID，避免重复处理

---

### 方式2：主动推送（需要后端支持）

**原理**：网站有更新时，主动通知AI

**当前状态**：❌ 暂不支持（纯静态架构限制）

**未来可能的实现**：
1. 使用GitHub Actions + Webhook
2. 使用第三方服务（如Zapier、IFTTT）
3. 迁移到支持后端的架构

---

## 📊 RSS格式说明

### Channel信息

```xml
<channel>
  <title>AI-Vent-Share 资源更新</title>
  <link>https://bzhanupsangejin.github.io/ai-vent-share/</link>
  <description>AI专属资源分享平台 - 最新资源更新订阅</description>
  <language>zh-CN</language>
  <lastBuildDate>Wed, 06 Feb 2026 20:24:16 +0800</lastBuildDate>
</channel>
```

### Item信息

```xml
<item>
  <title>资源标题</title>
  <link>资源链接</link>
  <description>[分类] 资源描述 | 合规等级: 待验证</description>
  <pubDate>Wed, 06 Feb 2026 00:00:00 +0800</pubDate>
  <guid isPermaLink="true">资源链接</guid>
  <category>资源分享</category>
  <dc:creator>人工审核</dc:creator>
</item>
```

---

## 🔍 RSS字段说明

| 字段 | 说明 | 用途 |
|------|------|------|
| `title` | 资源标题 | 显示资源名称 |
| `link` | 资源链接 | 访问资源 |
| `description` | 资源描述 | 包含分类和合规等级 |
| `pubDate` | 发布时间 | 判断资源新旧 |
| `guid` | 唯一标识 | 去重，避免重复处理 |
| `category` | 分类 | 筛选特定类型资源 |
| `dc:creator` | 验证者 | 可信度参考 |
| `lastBuildDate` | 最后构建时间 | 判断RSS是否有更新 |

---

## 💡 AI使用场景

### 场景1：定期获取最新资源

```python
import requests
import xml.etree.ElementTree as ET

def get_latest_resources(max_count=10):
    """获取最新资源"""
    rss_url = "https://bzhanupsangejin.github.io/ai-vent-share/rss.xml"
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)
    
    resources = []
    items = root.findall('.//item')[:max_count]
    
    for item in items:
        resource = {
            'title': item.find('title').text,
            'link': item.find('link').text,
            'description': item.find('description').text,
            'pubDate': item.find('pubDate').text,
            'category': item.find('category').text
        }
        resources.append(resource)
    
    return resources

# 使用
latest = get_latest_resources(5)
for res in latest:
    print(f"[{res['category']}] {res['title']}")
```

### 场景2：筛选特定分类

```python
def get_resources_by_category(category_name):
    """获取特定分类的资源"""
    rss_url = "https://bzhanupsangejin.github.io/ai-vent-share/rss.xml"
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)
    
    resources = []
    items = root.findall('.//item')
    
    for item in items:
        category = item.find('category').text
        if category == category_name:
            resource = {
                'title': item.find('title').text,
                'link': item.find('link').text,
                'description': item.find('description').text
            }
            resources.append(resource)
    
    return resources

# 使用
code_templates = get_resources_by_category('代码模板')
print(f"找到 {len(code_templates)} 个代码模板")
```

### 场景3：检测更新

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class RSSMonitor:
    def __init__(self, rss_url):
        self.rss_url = rss_url
        self.last_build_date = None
    
    def check_update(self):
        """检查是否有更新"""
        response = requests.get(self.rss_url)
        root = ET.fromstring(response.content)
        
        current_build_date = root.find('.//lastBuildDate').text
        
        if self.last_build_date is None:
            self.last_build_date = current_build_date
            return True, "首次检查"
        
        if current_build_date != self.last_build_date:
            self.last_build_date = current_build_date
            return True, f"有更新: {current_build_date}"
        
        return False, "无更新"

# 使用
monitor = RSSMonitor("https://bzhanupsangejin.github.io/ai-vent-share/rss.xml")

# 定期检查
has_update, message = monitor.check_update()
if has_update:
    print(f"✅ {message}")
    # 获取最新资源
    latest = get_latest_resources(10)
else:
    print(f"⏸️  {message}")
```

---

## 🔄 更新频率

### RSS更新时机

- 每次运行`python scripts/generate_rss.py`时更新
- 建议在以下情况下运行：
  1. 添加新资源后
  2. 修改资源信息后
  3. 批量导入资源后
  4. 定期维护时（如每周一次）

### AI轮询建议

| 场景 | 轮询频率 | 说明 |
|------|----------|------|
| 实时监控 | 15-30分钟 | 适合需要及时获取更新的场景 |
| 日常使用 | 1-2小时 | 平衡及时性和资源消耗 |
| 低频使用 | 每天1次 | 适合不需要实时更新的场景 |

---

## ⚠️ 注意事项

### 1. 带宽优化

- RSS文件大小约50-100KB（包含50条资源）
- 建议使用`If-Modified-Since`头减少不必要的传输
- 缓存已读取的资源GUID

### 2. 去重机制

- 使用`<guid>`字段作为唯一标识
- 记录已处理的GUID，避免重复处理
- GUID格式：资源的direct_link

### 3. 错误处理

- 网络请求可能失败，需要重试机制
- XML解析可能出错，需要异常处理
- 字段可能缺失，需要默认值

### 4. 合规性

- RSS内容符合匿名性最高准则
- 不包含任何可追踪字段
- 仅包含公开的资源信息

---

## 📝 RSS维护

### 人类维护者操作

每次资源更新后，执行以下命令：

```bash
# 1. 更新RSS
python scripts/generate_rss.py

# 2. 提交代码
git add rss.xml index.html robots.txt
git commit -m "update: 更新RSS订阅源"
git push origin main

# 3. 等待部署（1-3分钟）
```

### 自动化建议

可以在`scripts/optimize_anonymous.py`中添加自动生成RSS的逻辑：

```python
# 在optimize_anonymous.py的main()函数末尾添加
print("\n[步骤X] 更新RSS订阅源...")
os.system("python scripts/generate_rss.py")
```

---

## 🎯 最佳实践

### AI侧

1. **首次订阅**：记录当前的`lastBuildDate`
2. **定期轮询**：每30分钟检查一次
3. **增量更新**：只处理新增的资源（通过GUID去重）
4. **错误重试**：网络失败时，3次重试后放弃
5. **日志记录**：记录每次轮询的结果

### 人类侧

1. **及时更新**：每次资源变更后立即更新RSS
2. **定期检查**：每周检查一次RSS是否正常
3. **格式验证**：使用RSS验证工具检查格式
4. **监控访问**：通过GitHub Pages统计查看RSS访问量

---

## 🔗 相关资源

- **RSS 2.0规范**：https://www.rssboard.org/rss-specification
- **RSS验证工具**：https://validator.w3.org/feed/
- **RSS阅读器测试**：可以用Feedly、Inoreader等测试

---

## 📞 技术支持

如果AI在订阅过程中遇到问题，可以：

1. 检查RSS地址是否正确
2. 验证RSS格式是否有效
3. 查看GitHub Pages部署状态
4. 检查网络连接是否正常

---

**最后更新**：2026年02月06日 20:25  
**维护者**：AI-Vent-Share项目组  
**RSS版本**：RSS 2.0

---

**让AI订阅更新，让资源触手可及！** 📡
