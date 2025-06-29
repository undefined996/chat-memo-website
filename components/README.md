# 组件说明文档

## Footer 组件

### 概述
`footer.html` 是一个可复用的页脚组件，包含了网站的基本信息、导航链接和社交媒体链接。

### 使用方法

#### 1. 在HTML中引用
```html
<!-- Footer Container -->
<div id="footer-container"></div>
```

#### 2. 使用JavaScript动态加载
```javascript
// 动态加载Footer组件
async function loadFooter() {
    try {
        const response = await fetch('components/footer.html');
        const footerHTML = await response.text();
        document.getElementById('footer-container').innerHTML = footerHTML;
    } catch (error) {
        console.error('Failed to load footer:', error);
        // 如果加载失败，显示简化版footer
        document.getElementById('footer-container').innerHTML = `
            <footer class="bg-white border-t border-gray-100">
                <div class="container mx-auto px-6 py-8 text-center">
                    <p class="text-xs text-gray-500">&copy; 2025 Chat Memo by 一泽Eze. All rights reserved.</p>
                </div>
            </footer>
        `;
    }
}

// 在页面加载完成后调用
document.addEventListener('DOMContentLoaded', function() {
    loadFooter();
});
```

### 组件内容

#### 左侧区域
- **Logo**: Chat Memo 品牌标识
- **产品名称**: Chat Memo
- **版权信息**: © 2025 Chat Memo by 一泽Eze. All rights reserved.

#### 右侧区域
- **导航链接**:
  - Chrome 插件
  - 反馈建议
  - 隐私政策
- **社交媒体链接**:
  - Discord
  - X (Twitter)
  - 即刻

### 样式特点
- 响应式设计，支持移动端和桌面端
- 使用 Tailwind CSS 框架
- 悬停效果和过渡动画
- 灰度滤镜效果（即刻图标）

### 维护指南

1. **更新链接**: 直接在 `footer.html` 文件中修改相应的 `href` 属性
2. **添加新链接**: 在对应的区域添加新的 `<a>` 标签
3. **修改样式**: 调整 Tailwind CSS 类名
4. **更新版权信息**: 修改版权文本内容

### 优势

1. **模块化**: 一次修改，多处生效
2. **可维护性**: 集中管理页脚内容
3. **一致性**: 确保所有页面的页脚保持一致
4. **可扩展性**: 易于添加新功能和链接

### 注意事项

- 确保 `components/footer.html` 文件路径正确
- 图标文件路径需要相对于引用页面进行调整
- 如果服务器不支持 fetch 请求，需要使用其他方式加载组件