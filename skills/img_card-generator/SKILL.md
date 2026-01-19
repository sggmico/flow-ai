---
name: img_card-generator
description: Use when generating social media card images (Xiaohongshu/Instagram/etc), creating SVG graphics for content marketing, or need visually appealing carousel cards with code blocks, checklists, or infographics.
---

# Card Image Generator

Generate professional social media card images (SVG format) for platforms like Xiaohongshu, Instagram, Twitter, etc.

## Overview

This skill provides **standardized prompts and templates** for generating high-quality card images using AI models. Works with Claude, GPT-4, Gemini, and other capable models.

**Output**: SVG format (vector, scalable, editable)
**Platforms**: Xiaohongshu (1080×1440), Instagram (1080×1350), Twitter (1200×675)

## Quick Start

### Universal Prompt Template

```
Generate an SVG card image with the following specifications:

【Basic Info】
- Dimensions: {width}×{height}px (e.g., 1080×1440 for Xiaohongshu)
- Style: {style_name} (see Style Guide below)
- Language: {Chinese/English}

【Content Structure】
- Card Number: {number} / {total} (e.g., 02/08)
- Tag: {tag_text} (e.g., "痛点自测", "实操步骤")
- Title: {main_title}
- Subtitle: {subtitle} (optional)
- Body Content: {content_description}
- Footer: {watermark_text} (e.g., "@YourID")

【Design Requirements】
- Background: {gradient/solid/pattern}
- Accent Color: {hex_color}
- Include decorative elements: {yes/no}
- Code block style: {if applicable}

Output clean SVG code with proper Chinese font fallbacks.
```

## Platform Dimensions

| Platform | Size (px) | Aspect Ratio | Use Case |
|----------|-----------|--------------|----------|
| Xiaohongshu | 1080×1440 | 3:4 | Carousel cards |
| Instagram Post | 1080×1350 | 4:5 | Feed posts |
| Instagram Story | 1080×1920 | 9:16 | Stories |
| Twitter/X | 1200×675 | 16:9 | Tweet images |
| WeChat Article | 900×500 | 9:5 | Article covers |

## Style Guide

### Style 1: Tech Dark (科技暗黑)
```
Background: linear-gradient(180deg, #1a1a2e → #16213e → #0f3460)
Accent: #667eea (purple-blue), #fbbf24 (gold highlight)
Text: white with rgba(255,255,255,0.7) secondary
Cards: rgba(255,255,255,0.08) with blur backdrop
Best for: Programming tutorials, tech content
```

### Style 2: Gradient Vibrant (渐变活力)
```
Background: linear-gradient(135deg, #667eea → #764ba2 → #f093fb)
Accent: #fbbf24 (gold), #10b981 (green)
Text: white with text-shadow
Cards: rgba(0,0,0,0.2) or rgba(255,255,255,0.2)
Best for: Covers, announcements, eye-catching content
```

### Style 3: Clean Minimal (简约清新)
```
Background: #f8fafc or #ffffff
Accent: #3b82f6 (blue), #10b981 (green)
Text: #1e293b (dark) with #64748b secondary
Cards: white with subtle shadow
Best for: Professional content, documentation
```

### Style 4: Warm Gradient (暖色渐变)
```
Background: linear-gradient(135deg, #ff9a9e → #fecfef → #fecfef)
Accent: #ec4899 (pink), #f59e0b (orange)
Text: #1e293b or white depending on section
Best for: Lifestyle, design, creative content
```

## Card Types & Templates

### Type A: Cover Card (封面卡)
```
Elements:
├── Top badge (trending tag)
├── Main title (largest, bold)
├── Subtitle (secondary)
├── Visual element (phone mockup, illustration)
├── Feature tags (3-6 tags around visual)
├── CTA text ("左滑看教程")
└── Watermark
```

### Type B: Checklist Card (清单卡)
```
Elements:
├── Card number tag
├── Title with emoji/icon
├── Subtitle (optional)
├── Checklist items (3-5 items)
│   ├── Emoji prefix
│   └── Text content
├── Conclusion box (highlighted)
└── Watermark
```

### Type C: Code Tutorial Card (代码教程卡)
```
Elements:
├── Card number tag
├── Title (with code filename)
├── Code block
│   ├── Window chrome (red/yellow/green dots)
│   ├── Filename tab
│   ├── Syntax-highlighted code
│   └── Highlighted line (key point)
├── Explanation box
│   ├── Icon (💡)
│   └── Plain-language explanation
├── Tip/Note (optional)
└── Watermark
```

### Type D: Comparison Card (对比卡)
```
Elements:
├── Card number tag
├── Title
├── Two-column layout
│   ├── Left: ❌ Wrong way
│   └── Right: ✅ Right way
├── Summary point
└── Watermark
```

### Type E: Summary Card (总结卡)
```
Elements:
├── Card number tag
├── Title ("恭喜解锁新技能!")
├── Achievement checklist (✅ items)
├── CTA box
├── Social follow prompt
└── Watermark
```

## SVG Code Structure

### Basic Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Gradients -->
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{color1}"/>
      <stop offset="100%" style="stop-color:{color2}"/>
    </linearGradient>

    <!-- Shadows -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="15" flood-color="rgba(0,0,0,0.3)"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" rx="40" fill="url(#bgGradient)"/>

  <!-- Decorative elements -->
  <ellipse cx="..." cy="..." rx="..." ry="..." fill="..." opacity="0.1"/>

  <!-- Content sections -->
  <!-- ... -->

  <!-- Watermark -->
  <text x="{width/2}" y="{height-40}" text-anchor="middle"
        font-family="system-ui, -apple-system, sans-serif"
        font-size="26" fill="rgba(255,255,255,0.5)">
    @YourID
  </text>
</svg>
```

### Font Stack (Cross-platform)

```xml
font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif"
```

For code blocks:
```xml
font-family="'SF Mono', Monaco, 'Cascadia Code', Consolas, 'Courier New', monospace"
```

### Code Block Component

```xml
<!-- Code block container -->
<g filter="url(#codeShadow)">
  <!-- Background -->
  <rect x="60" y="330" width="960" height="400" rx="20" fill="#1e1e3f"/>

  <!-- Window chrome -->
  <rect x="60" y="330" width="960" height="50" rx="20" fill="#1a1a35"/>
  <circle cx="100" cy="355" r="8" fill="#ff5f56"/>
  <circle cx="130" cy="355" r="8" fill="#ffbd2e"/>
  <circle cx="160" cy="355" r="8" fill="#27ca40"/>

  <!-- Filename -->
  <text x="500" y="362" font-family="monospace" font-size="16"
        fill="rgba(255,255,255,0.5)" text-anchor="middle">filename.js</text>

  <!-- Code lines -->
  <text x="90" y="420" font-family="monospace" font-size="24" fill="#9cdcfe">const</text>
  <!-- ... more code lines ... -->

  <!-- Highlighted line -->
  <rect x="80" y="460" width="920" height="40" rx="8" fill="rgba(251,191,36,0.15)"/>
  <rect x="80" y="460" width="4" height="40" fill="#fbbf24"/>
</g>
```

### Checklist Item Component

```xml
<g>
  <rect x="60" y="480" width="960" height="120" rx="24"
        fill="rgba(255,255,255,0.08)"
        stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <text x="100" y="555" font-size="48">🤔</text>
  <text x="170" y="550" font-family="system-ui" font-size="32"
        font-weight="500" fill="white">Your checklist text here</text>
</g>
```

### Tag/Badge Component

```xml
<g filter="url(#shadow)">
  <rect x="60" y="80" width="200" height="55" rx="27" fill="url(#accentGradient)"/>
  <text x="90" y="118" font-family="system-ui" font-size="22"
        fill="white" opacity="0.8">01</text>
  <text x="125" y="118" font-family="system-ui" font-size="24"
        font-weight="700" fill="white">标签文字</text>
</g>
```

## Color Palettes

### Tech Theme
| Role | Color | Usage |
|------|-------|-------|
| Primary | #667eea | Accents, links |
| Secondary | #764ba2 | Gradients |
| Highlight | #fbbf24 | Important, gold |
| Success | #10b981 | Checkmarks, positive |
| Error | #ef4444 | Warnings, negative |
| Code keyword | #9cdcfe | Syntax highlight |
| Code string | #ce9178 | Syntax highlight |
| Code bracket | #7c7cba | Syntax highlight |

### Vibrant Theme
| Role | Color | Usage |
|------|-------|-------|
| Pink | #ec4899 | Tags, accents |
| Orange | #f97316 | Highlights |
| Blue | #3b82f6 | Info, links |
| Green | #10b981 | Success |
| Purple | #8b5cf6 | Special |

## Prompt Examples

### Example 1: Tutorial Cover

```
Generate an SVG card (1080×1440px) for Xiaohongshu:

【Content】
- Style: Gradient Vibrant (紫粉渐变)
- Title: "前端工程师简历加分项 ✨"
- Subtitle: "3步让你的网页秒变APP"
- Visual: Phone mockup showing app icons, one highlighted as "PWA"
- Tags around phone: "✅可安装", "📴可离线", "⚡秒开加载"
- Top badge: "🔥 2024前端必学技能"
- CTA: "👆 左滑看保姆级教程"
- Watermark: "@Sggmico"

【Design】
- Background: purple to pink gradient (#667eea → #764ba2 → #f093fb)
- Decorative circles with low opacity
- Gold highlight for "PWA" text
- Phone with shadow effect
```

### Example 2: Code Tutorial

```
Generate an SVG card (1080×1440px) for Xiaohongshu:

【Content】
- Card: 04/08
- Tag: "保姆级实操 ①" (orange)
- Title: "创建 manifest.json"
- Subtitle: "给你的网页办一张「身份证」"

【Code Block】
{
  "name": "我的PWA应用",
  "display": "standalone",  ← HIGHLIGHT THIS LINE
  "theme_color": "#667eea"
}

【Explanation Box】
💡 大白话解释:
display: "standalone" 的意思是让应用像独立 App 一样打开，没有浏览器的地址栏！

【Footer】
📝 记得把这个文件放到项目根目录
Watermark: @Sggmico
```

### Example 3: Checklist Card

```
Generate an SVG card (1080×1440px) for Xiaohongshu:

【Content】
- Card: 02/08
- Tag: "痛点自测" (pink)
- Title: "你的项目真的需要PWA吗？"
- Subtitle: "快速判断是否值得投入"

【Checklist Items】
🤔 用户是否常在弱网/离线环境？
🤔 想提升留存，又不想上架应用商店？
🤔 网页体验很好，就差离线和安装？

【Conclusion Box】(green background)
✨ 命中2条以上，PWA就是你的菜！✨

【Footer】
Watermark: @Sggmico
```

## Tips for Best Results

### For All Models

1. **Be specific about dimensions** - Always state exact pixel size
2. **Provide color codes** - Use hex colors, not names
3. **Describe layout clearly** - Top/middle/bottom, left/right
4. **Specify font sizes** - Give approximate sizes (e.g., title 72px, body 32px)
5. **Request "clean SVG code"** - Helps avoid extra markup

### Model-Specific Tips

**Claude (Sonnet/Opus)**
- Handles complex SVG well
- Good with Chinese text
- Can iterate on designs

**GPT-4**
- May need simpler structures
- Sometimes adds extra XML namespaces
- Good with visual descriptions

**Gemini**
- Works well with structured prompts
- May need explicit font-family declarations
- Good with gradient definitions

### Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Chinese text not rendering | Use system font stack with Chinese fallbacks |
| Emoji not showing | Use text element with proper font-size |
| Gradient not working | Check gradient ID matches fill="url(#id)" |
| Elements overlapping | Adjust y coordinates, check element order |
| Shadow cut off | Increase filter x/y/width/height percentages |

## File Naming Convention

```
card-{number}-{name}.svg

Examples:
card-01-封面.svg
card-02-痛点自测.svg
card-03-核心科普.svg
card-04-实操步骤1.svg
```

## Workflow

```
1. Define content outline (8 cards for tutorial series)
2. Choose platform & dimensions
3. Select style theme
4. Generate cards using prompts above
5. Save as SVG files
6. (Optional) Convert to PNG for upload
```

## Converting SVG to PNG

```bash
# Using Inkscape (CLI)
inkscape input.svg --export-filename=output.png --export-width=1080

# Using ImageMagick
convert -density 300 input.svg output.png

# Using Chrome DevTools
# Open SVG in browser → Right-click → Save as PNG

# Using Figma
# Import SVG → Export as PNG @2x
```

---

**Author**: Sggmico
**Version**: 1.0.0
**Last Updated**: 2025-01
