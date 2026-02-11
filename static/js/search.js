/**
 * AI资源网站 - 轻量级前端搜索引擎
 * 纯JS实现，无后端依赖，保持匿名性
 * 优化版本 - 2026-02-11
 */

class AIResourceSearch {
    constructor() {
        this.resources = [];
        this.filteredResources = [];
        this.currentPage = 0;
        this.pageSize = 20;
    }

    /**
     * 加载资源数据
     * @param {string} indexUrl - 索引文件URL
     */
    async loadResources(indexUrl) {
        try {
            const response = await fetch(indexUrl);
            const data = await response.json();
            this.resources = data.index || [];
            this.filteredResources = this.resources;
            return this.resources;
        } catch (error) {
            console.error('加载资源失败:', error);
            return [];
        }
    }

    /**
     * 搜索资源
     * @param {Object} filters - 筛选条件
     * @param {string} filters.keyword - 关键词
     * @param {string} filters.category - 分类
     * @param {Array} filters.tags - 标签数组
     * @param {string} filters.status - 状态
     */
    search(filters = {}) {
        const { keyword, category, tags, status } = filters;

        this.filteredResources = this.resources.filter(resource => {
            // 关键词匹配（标题、摘要、关键词）
            const matchKeyword = !keyword || 
                resource.title.toLowerCase().includes(keyword.toLowerCase()) ||
                resource.summary.toLowerCase().includes(keyword.toLowerCase()) ||
                (resource.keywords && resource.keywords.toLowerCase().includes(keyword.toLowerCase()));

            // 分类匹配
            const matchCategory = !category || resource.content_type === category;

            // 标签匹配
            const matchTags = !tags || tags.length === 0 || 
                (resource.tags && tags.some(tag => resource.tags.includes(tag)));

            // 状态匹配
            const matchStatus = !status || resource.status === status || !resource.status;

            return matchKeyword && matchCategory && matchTags && matchStatus;
        });

        this.currentPage = 0;
        return this.filteredResources;
    }

    /**
     * 获取当前页资源
     */
    getCurrentPage() {
        const start = this.currentPage * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredResources.slice(start, end);
    }

    /**
     * 加载更多
     */
    loadMore() {
        this.currentPage++;
        return this.getCurrentPage();
    }

    /**
     * 是否还有更多
     */
    hasMore() {
        return (this.currentPage + 1) * this.pageSize < this.filteredResources.length;
    }

    /**
     * 获取统计信息
     */
    getStats() {
        const stats = {
            total: this.resources.length,
            filtered: this.filteredResources.length,
            categories: {},
            status: {}
        };

        // 统计分类
        this.filteredResources.forEach(resource => {
            const cat = resource.content_type || '未分类';
            stats.categories[cat] = (stats.categories[cat] || 0) + 1;

            const st = resource.status || 'active';
            stats.status[st] = (stats.status[st] || 0) + 1;
        });

        return stats;
    }

    /**
     * 按字段排序
     * @param {string} field - 排序字段
     * @param {string} order - 排序方向 (asc/desc)
     */
    sort(field, order = 'asc') {
        this.filteredResources.sort((a, b) => {
            const aVal = a[field] || '';
            const bVal = b[field] || '';

            if (order === 'asc') {
                return aVal > bVal ? 1 : -1;
            } else {
                return aVal < bVal ? 1 : -1;
            }
        });

        return this.filteredResources;
    }
}

// 渲染工具类
class ResourceRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    /**
     * 渲染资源列表
     */
    render(resources) {
        if (!this.container) return;

        this.container.innerHTML = '';

        if (resources.length === 0) {
            this.container.innerHTML = '<div class="no-results">未找到匹配的资源</div>';
            return;
        }

        resources.forEach(resource => {
            const card = this.createCard(resource);
            this.container.appendChild(card);
        });
    }

    /**
     * 创建资源卡片
     */
    createCard(resource) {
        const card = document.createElement('div');
        card.className = 'resource-card';
        card.innerHTML = `
            <div class="card-header">
                <h3 class="card-title">${this.escapeHtml(resource.title)}</h3>
                <span class="card-category">${resource.content_type}</span>
            </div>
            <div class="card-body">
                <p class="card-summary">${this.escapeHtml(resource.summary.substring(0, 150))}...</p>
                ${resource.tags && resource.tags.length > 0 ? 
                    `<div class="card-tags">
                        ${resource.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>` : ''}
            </div>
            <div class="card-footer">
                <span class="card-date">${resource.last_updated || '未知'}</span>
                <a href="${resource.direct_link}" class="card-link" target="_blank">查看详情</a>
            </div>
        `;
        return card;
    }

    /**
     * 转义HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * 渲染统计信息
     */
    renderStats(stats, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">总资源</span>
                    <span class="stat-value">${stats.total}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">当前显示</span>
                    <span class="stat-value">${stats.filtered}</span>
                </div>
            </div>
        `;
    }
}

// 全局实例
let searchEngine = null;
let renderer = null;

// 初始化
async function initSearch() {
    searchEngine = new AIResourceSearch();
    renderer = new ResourceRenderer('resource-list');

    // 加载资源（使用压缩版本）
    await searchEngine.loadResources('content_index.min.json');

    // 渲染初始结果
    const initialResults = searchEngine.getCurrentPage();
    renderer.render(initialResults);

    // 渲染统计
    const stats = searchEngine.getStats();
    renderer.renderStats(stats, 'stats-container');

    // 绑定搜索事件
    bindSearchEvents();
}

// 绑定搜索事件
function bindSearchEvents() {
    const searchInput = document.getElementById('search-input');
    const categorySelect = document.getElementById('category-select');
    const loadMoreBtn = document.getElementById('load-more');

    if (searchInput) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', performSearch);
    }

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            const moreResults = searchEngine.loadMore();
            renderer.render([...document.querySelectorAll('.resource-card'), ...moreResults]);

            if (!searchEngine.hasMore()) {
                loadMoreBtn.style.display = 'none';
            }
        });
    }
}

// 执行搜索
function performSearch() {
    const keyword = document.getElementById('search-input')?.value || '';
    const category = document.getElementById('category-select')?.value || '';

    const results = searchEngine.search({ keyword, category });
    const pageResults = searchEngine.getCurrentPage();

    renderer.render(pageResults);

    const stats = searchEngine.getStats();
    renderer.renderStats(stats, 'stats-container');

    // 显示/隐藏加载更多按钮
    const loadMoreBtn = document.getElementById('load-more');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = searchEngine.hasMore() ? 'block' : 'none';
    }
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch);
} else {
    initSearch();
}
