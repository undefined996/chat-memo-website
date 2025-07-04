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

## 部署到 Cloudflare Pages

### 方法一：通过 Git 仓库部署（推荐）

1. **准备 Git 仓库**
   - 在 GitHub/GitLab 创建新仓库
   - 将项目代码推送到仓库

2. **连接 Cloudflare Pages**
   - 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - 进入 "Pages" 部分
   - 点击 "Create a project"
   - 选择 "Connect to Git"

3. **配置项目**
   - 选择你的 Git 仓库
   - 设置构建配置：
     - Framework preset: `None`
     - Build command: 留空
     - Build output directory: `/`
     - Root directory: `/`

4. **部署**
   - 点击 "Save and Deploy"
   - 等待部署完成

### 方法二：直接上传文件

1. **准备文件**
   - 确保所有文件都在项目根目录
   - 检查文件路径引用是否正确

2. **上传到 Cloudflare Pages**
   - 登录 Cloudflare Dashboard
   - 进入 "Pages" 部分
   - 点击 "Create a project"
   - 选择 "Upload assets"
   - 拖拽整个项目文件夹或选择文件上传

3. **配置域名**
   - 部署完成后会获得一个 `.pages.dev` 域名
   - 可以在设置中添加自定义域名

### 部署注意事项

- ✅ 所有资源文件路径已规范化到 `resource/` 目录
- ✅ 使用相对路径，确保在任何域名下都能正常访问
- ✅ 视频文件已优化，支持自动播放和循环
- ✅ 图片已压缩，加载速度优化

### 自定义域名设置

1. 在 Cloudflare Pages 项目设置中添加自定义域名
2. 根据提示配置 DNS 记录
3. 等待 SSL 证书自动配置完成

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