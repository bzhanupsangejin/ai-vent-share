/**
 * AI资源网站 - 轻量级前端搜索引擎
 * 纯JS实现，无后端依赖，保持匿名性
 * 优化版本 - 2026-02-12 (CDN加速+智能排序+高亮显示)
 */

class AIResourceSearch {
    constructor() {
        this.resources = [];
        this.filteredResources = [];
        this.currentPage = 0;
        this.pageSize = 20;
        this.currentKeyword = '';
    }

    /**
     * 加载资源数据（CDN加速+回退机制）
     */
    async loadResources() {
        const cdnUrl = 'https://cdn.jsdelivr.net/gh/bzhanupsangejin/ai-vent-share@main/content_index.min.json';
        const fallbackUrl = 'content_index.min.json';
        
        try {
            console.log('尝试从CDN加载...');
            const response = await fetch(cdnUrl, { cache: 'default' });
            if (response.ok) {
                const data = await response.json();
                this.resources = data.index || [];
                this.filteredResources = this.resources;
                console.log('✅ CDN加载成功');
                return this.resources;
            }
        } catch (e) {
            console.log('⚠️ CDN加载失败，使用本地资源');
        }
        
        // 回退到本地
        try {
            const response = await fetch(fallbackUrl);
            const data = await response.json();
            this.resources = data.index || [];
            this.filteredResources = this.resources;
            console.log('✅ 本地资源加载成功');
            return this.resources;
        } catch (error) {
            console.error('❌ 加载资源失败:', error);
            return [];
        }
    }

    /**
     * 计算资源相关性得分
     */
    calculateRelevance(resource, keyword) {
        if (!keyword) return 0;
        
        let score = 0;
        const lowerKeyword = keyword.toLowerCase();
        const title = (resource.title || '').toLowerCase();
        const summary = (resource.summary || '').toLowerCase();
        const keywords = (resource.keywords || '').toLowerCase();
        
        // 标题完全匹配：10分
        if (title === lowerKeyword) score += 10;
        // 标题包含：5分
        else if (title.includes(lowerKeyword)) score += 5;
        
        // 关键词匹配：3分
        if (keywords.includes(lowerKeyword)) score += 3;
        
        // 摘要匹配：1分
        if (summary.includes(lowerKeyword)) score += 1;
        
        // 标签匹配：2分
        if (resource.tags && resource.tags.some(tag => tag.toLowerCase().includes(lowerKeyword))) {
            score += 2;
        }
        
        // 最近更新：额外加分
        if (resource.last_updated) {
            const daysSinceUpdate = (new Date() - new Date(resource.last_updated)) / (1000 * 60 * 60 * 24);
            if (daysSinceUpdate < 30) score += 2;
            else if (daysSinceUpdate < 90) score += 1;
        }
        
        return score;
    }

    /**
     * 搜索资源（带智能排序）
     */
    search(filters = {}) {
        const { keyword, category, tags, status } = filters;
        this.currentKeyword = keyword || '';

        this.filteredResources = this.resources.filter(resource => {
            // 关键词匹配
            const matchKeyword = !keyword || 
                (resource.title && resource.title.toLowerCase().includes(keyword.toLowerCase())) ||
                (resource.summary && resource.summary.toLowerCase().includes(keyword.toLowerCase())) ||
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

        // 智能排序：按相关性排序
        if (keyword) {
            this.filteredResources.sort((a, b) => {
                return this.calculateRelevance(b, keyword) - this.calculateRelevance(a, keyword);
            });
        }

        this.currentPage = 0;
        return this.filteredResources;
    }

    getCurrentPage() {
        const start = this.currentPage * this.pageSize;
        const end = start + this.pageSize;
        return this.filteredResources.slice(start, end);
    }

    loadMore() {
        this.currentPage++;
        return this.getCurrentPage();
    }

    hasMore() {
        return (this.currentPage + 1) * this.pageSize < this.filteredResources.length;
    }

    getStats() {
        const stats = {
            total: this.resources.length,
            filtered: this.filteredResources.length,
            categories: {},
            status: {}
        };

        this.filteredResources.forEach(resource => {
            const cat = resource.content_type || '未分类';
            stats.categories[cat] = (stats.categories[cat] || 0) + 1;

            const st = resource.status || 'active';
            stats.status[st] = (stats.status[st] || 0) + 1;
        });

        return stats;
    }
}

// 渲染工具类（增强版）
class ResourceRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentKeyword = '';
    }

    /**
     * 高亮关键词
     */
    highlightKeyword(text, keyword) {
        if (!keyword || !text) return this.escapeHtml(text);
        
        const escapedText = this.escapeHtml(text);
        const regex = new RegExp(`(${keyword})`, 'gi');
        return escapedText.replace(regex, '<mark style="background: #ffeb3b; padding: 2px 4px; border-radius: 2px;">$1</mark>');
    }

    render(resources, keyword = '') {
        if (!this.container) return;

        this.currentKeyword = keyword;
        this.container.innerHTML = '';

        if (resources.length === 0) {
            this.container.innerHTML = '<div class="no-results">😔 未找到匹配的资源，试试其他关键词吧</div>';
            return;
        }

        resources.forEach(resource => {
            const card = this.createCard(resource);
            this.container.appendChild(card);
        });
    }

    createCard(resource) {
        const card = document.createElement('div');
        card.className = 'resource-card';
        
        // 高亮显示标题和摘要中的关键词
        const highlightedTitle = this.highlightKeyword(resource.title, this.currentKeyword);
        const highlightedSummary = this.highlightKeyword(resource.summary.substring(0, 150), this.currentKeyword);
        
        card.innerHTML = `
            <div class="card-header">
                <h3 class="card-title">${highlightedTitle}</h3>
                <span class="card-category">${resource.content_type}</span>
            </div>
            <div class="card-body">
                <p class="card-summary">${highlightedSummary}...</p>
                ${resource.tags && resource.tags.length > 0 ? 
                    `<div class="card-tags">
                        ${resource.tags.slice(0, 5).map(tag => `<span class="tag">${this.escapeHtml(tag)}</span>`).join('')}
                    </div>` : ''}
            </div>
            <div class="card-footer">
                <span class="card-date">📅 ${resource.last_updated || '未知'}</span>
                <a href="${resource.direct_link}" class="card-link" target="_blank" rel="noopener">查看详情 →</a>
            </div>
        `;
        
        // 添加淡入动画
        card.style.animation = 'fadeIn 0.3s ease-out';
        
        return card;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

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
    // 显示加载提示
    const container = document.getElementById('resource-list');
    if (container) {
        container.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">⏳ 正在加载资源...</div>';
    }
    
    searchEngine = new AIResourceSearch();
    renderer = new ResourceRenderer('resource-list');

    // 加载资源（CDN加速）
    await searchEngine.loadResources();

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
        
        // 回车搜索
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    if (categorySelect) {
        categorySelect.addEventListener('change', performSearch);
    }

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            const moreResults = searchEngine.loadMore();
            const currentCards = Array.from(document.querySelectorAll('.resource-card'));
            
            // 追加新结果
            moreResults.forEach(resource => {
                const card = renderer.createCard(resource);
                document.getElementById('resource-list').appendChild(card);
            });

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

    renderer.render(pageResults, keyword);

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
