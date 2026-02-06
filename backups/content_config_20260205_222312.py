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
