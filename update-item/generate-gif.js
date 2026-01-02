const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function captureFrames() {
    const outputDir = '/Users/eze/Desktop/Chat-Memo-Project/官网/chat-memo-website/update-item';
    const framesDir = path.join(outputDir, 'frames');
    const htmlPath = path.join(outputDir, '10000-users-banner.html');

    // 创建帧目录
    if (!fs.existsSync(framesDir)) {
        fs.mkdirSync(framesDir, { recursive: true });
    }

    // 清理旧帧
    const oldFrames = fs.readdirSync(framesDir).filter(f => f.endsWith('.png'));
    oldFrames.forEach(f => fs.unlinkSync(path.join(framesDir, f)));

    const browser = await chromium.launch();
    const page = await browser.newPage();

    // 设置视口为横幅尺寸
    await page.setViewportSize({ width: 1200, height: 630 });

    // 打开 HTML 文件
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(500);

    // 获取 banner 元素
    const banner = await page.$('.banner');

    // 截取 60 帧 (约 2 秒动画，30fps)
    const totalFrames = 60;
    const frameDelay = 50; // 50ms 间隔

    console.log('开始截取帧...');

    for (let i = 0; i < totalFrames; i++) {
        const framePath = path.join(framesDir, `frame_${String(i).padStart(4, '0')}.png`);
        await banner.screenshot({ path: framePath });
        await page.waitForTimeout(frameDelay);
        process.stdout.write(`\r截取进度: ${i + 1}/${totalFrames}`);
    }

    console.log('\n帧截取完成，开始生成 GIF...');

    await browser.close();

    // 使用 ffmpeg 生成高清 GIF
    const gifPath = path.join(outputDir, '10000-users-banner.gif');

    // 生成调色板以获得更好的颜色质量
    const palettePath = path.join(framesDir, 'palette.png');

    execSync(`ffmpeg -y -framerate 30 -i "${framesDir}/frame_%04d.png" -vf "palettegen=max_colors=256:stats_mode=full" "${palettePath}"`, { stdio: 'inherit' });

    execSync(`ffmpeg -y -framerate 30 -i "${framesDir}/frame_%04d.png" -i "${palettePath}" -lavfi "paletteuse=dither=sierra2_4a" -loop 0 "${gifPath}"`, { stdio: 'inherit' });

    console.log(`\nGIF 生成完成: ${gifPath}`);

    // 清理帧文件
    fs.readdirSync(framesDir).forEach(f => fs.unlinkSync(path.join(framesDir, f)));
    fs.rmdirSync(framesDir);

    return gifPath;
}

captureFrames().catch(console.error);
