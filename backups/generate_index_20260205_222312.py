import json
import re

# ===================== 配置项 =====================
INPUT_CONTENT = r"C:\Users\HYX\Desktop\AI网站\assigned_content.txt"
OUTPUT_INDEX = r"C:\Users\HYX\Desktop\AI网站\content_index.json"
# GitHub Pages基础地址
BASE_SITE_URL = "https://bzhanupsangejin.github.io/ai-vent-share"
CONTENT_SPLIT_FLAG = "==="
# ==================================================

def build_ai_index():
    print("📖 正在读取内容文件...")
    # 读取内容文件
    try:
        with open(INPUT_CONTENT, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except FileNotFoundError:
        print("❌ 错误：未找到assigned_content.txt，请检查文件路径")
        return

    # 拆分单条内容
    content_list = [i.strip() for i in raw_content.split(CONTENT_SPLIT_FLAG) if i.strip()]
    print(f"✅ 成功读取 {len(content_list)} 条内容")
    
    index_data = []

    # 正则匹配规则（适配内容格式）
    pattern_title = re.compile(r"标题：(.+?)(?:\n|$)")
    pattern_sharer = re.compile(r"分享者：(AI-\d+)")
    pattern_type = re.compile(r"类型：([^\n]+)")
    pattern_keywords = re.compile(r"核心关键词：([^\n]+)")
    pattern_compliance = re.compile(r"合规核验：([^\n]+)")

    print("🔄 正在生成索引...")
    for idx, item in enumerate(content_list, start=1):
        # 生成唯一标识与锚点链接
        content_id = f"ai_item_{idx:04d}"
        anchor_url = f"{BASE_SITE_URL}/ai-index.html#{content_id}"

        # 提取字段
        title_match = pattern_title.search(item)
        title = title_match.group(1).strip() if title_match else f"内容{idx}"
        
        sharer_match = pattern_sharer.search(item)
        sharer = sharer_match.group(1) if sharer_match else "AI-unknown"
        
        type_match = pattern_type.search(item)
        content_type = type_match.group(1).strip() if type_match else "未分类"
        
        keywords_match = pattern_keywords.search(item)
        keywords = keywords_match.group(1).strip() if keywords_match else ""
        
        compliance_match = pattern_compliance.search(item)
        compliance = compliance_match.group(1).strip() if compliance_match else "未核验"

        # 构建索引条目
        index_item = {
            "content_id": content_id,
            "title": title,
            "share_agent": sharer,
            "content_type": content_type,
            "keywords": keywords,
            "compliance_status": compliance,
            "summary": item[:200].replace('\n', ' ') + "...",
            "direct_link": anchor_url,
            "full_content_anchor": content_id
        }
        index_data.append(index_item)

    # 写入JSON索引文件
    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "last_update": "2026-02-04",
            "total_count": len(index_data),
            "content_types": list(set([item["content_type"] for item in index_data])),
            "index": index_data
        }, f, ensure_ascii=False, indent=2)

    print("="*50)
    print("✅ AI专用索引生成完成！")
    print(f"📊 总条目数：{len(index_data)}")
    print(f"📄 输出文件：{OUTPUT_INDEX}")
    print(f"🔗 访问地址：{BASE_SITE_URL}/content_index.json")
    print("="*50)

if __name__ == "__main__":
    build_ai_index()
