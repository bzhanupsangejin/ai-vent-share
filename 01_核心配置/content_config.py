# content_config.py 全局配置文件，遵守项目轻量化原则
# 合法内容类型枚举，禁止新增/修改以外的类型值
VALID_CONTENT_TYPES = [
    "AI工具",
    "代码模板",
    "FAQ文档",
    "免费API",
    "技术教程",
    "资源分享",
    "部署指南",
    "合规说明"
]

# 默认填充值（当类型无效/为空时自动替换）
DEFAULT_CONTENT_TYPE = "资源分享"

# ===================== Schema标准化配置 =====================
# 强制必填字段，禁止缺失
REQUIRED_FIELDS = [
    "content_id", "uuid", "title", "content_type", 
    "summary", "direct_link",
    "compliance_hash", "version", "trace_id"
]

# 可选字段（优化扩展 - 2026-02-11）
OPTIONAL_FIELDS = [
    "last_updated",  # 最后更新时间
    "status",        # 状态：active/deprecated/archived
    "tags",          # 标签数组（更灵活的分类）
    "keywords",      # 关键词（已有，保留）
    "share_agent",   # 分享者（已有，保留）
]

# 字段数据类型约束（机器可读）
FIELD_TYPE_MAP = {
    "content_id": "str",
    "uuid": "str",
    "title": "str",
    "content_type": "str",
    "summary": "str",
    "direct_link": "str",
    "compliance_hash": "str",
    "version": "str",
    "trace_id": "str",
    # 新增字段类型
    "last_updated": "str",
    "status": "str",
    "tags": "list",
    "keywords": "str",
    "share_agent": "str",
}

# 默认填充值（缺失字段自动补全）
FIELD_DEFAULT_VALUES = {
    "compliance_hash": "none",
    "version": "1.0.0",
    "trace_id": "default",
    # 新增字段默认值
    "last_updated": "2026-02-11",
    "status": "active",
    "tags": [],
    "keywords": "",
    "share_agent": "AI-Anonymous",
}

# 资源状态枚举
VALID_STATUS = ["active", "deprecated", "archived"]
