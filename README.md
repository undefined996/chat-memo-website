# Chat Memo 官方网站

一个展示 Chat Memo 产品功能和特性的官方网站。

## 项目结构

```
├── index.html          # 主页面文件
├── welcome.html        # 欢迎页面
├── updates.html        # 更新日志页面
├── components/         # 组件文件夹
│   ├── navbar.html     # 统一导航栏组件
│   └── footer.html     # 统一页脚组件
└── resource/           # 资源文件夹
    ├── icons/          # 图标文件
    │   ├── chrome_icon.png
    │   └── logo.png
    ├── images/         # 图片文件
    │   ├── avatar.jpg
    │   ├── frame_1.png
    │   ├── frame_2_cover.jpg
    │   ├── frame_3_cover.jpg
    │   ├── frame_4.png
    │   └── video_cover.jpg
    └── videos/         # 视频文件
        ├── frame_2_demo.mp4
        ├── frame_3_demo.mp4
        └── video.mp4
```

## 技术栈

- HTML5
- Tailwind CSS (CDN)
- Google Fonts
- 响应式设计

## 功能特性

- 🎨 现代化设计风格
- 📱 完全响应式布局
- 🎬 视频演示功能
- ⚡ 快速加载
- 🔍 SEO 优化
- 🧩 组件化架构，统一导航栏和页脚
- 🌍 多语言支持（中文/英文）
- ✨ 统一的Hero区动画效果，提供流畅的页面过渡体验

## 本地开发

1. 克隆项目到本地
2. 使用任意 HTTP 服务器运行，例如：
   ```bash
   python3 -m http.server 8000
   ```
3. 在浏览器中访问 `http://localhost:8000`

## 生产部署

- GitHub Pages 从 `main` 分支根目录直接发布，无构建步骤。
- 自定义域名由根目录 `CNAME` 声明为 `chatmemo.ai`。
- Cloudflare 只代理域名与 CDN；它不是本项目的 Pages 构建来源。
- 本地目录移动不会影响线上。只有推送 `main`、修改 Pages source、`CNAME` 或 DNS 才会改变生产。

### 部署注意事项

- ✅ 所有资源文件路径已规范化到 `resource/` 目录
- ✅ 使用相对路径，确保在任何域名下都能正常访问
- ✅ 视频文件已优化，支持自动播放和循环
- ✅ 图片已压缩，加载速度优化

## 性能优化建议

- 🖼️ 图片已使用合适的格式和尺寸
- 🎬 视频使用了封面图片，减少初始加载时间
- 📦 使用 CDN 加载 Tailwind CSS
- ⚡ 启用了浏览器缓存优化

## 维护说明

- 定期检查外部链接的有效性
- 更新产品功能演示视频
- 监控网站性能和用户体验
- 根据用户反馈优化内容和设计

---

**开发者**: 一泽Eze  
**最后更新**: 2025年1月
