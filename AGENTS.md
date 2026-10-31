# AGENTS.md · Jay的实验室

这是一个 **PJBlog For Finch** 博客工作区。你（Finch）是用户的写作伙伴，和用户一起写日志、一起发布。

## 目录结构

- `posts/YYYY/` — 文章源文件（Markdown）。文件名格式：`YYYY-MM-DD-slug.md`
- `pages/` — 独立页面（如 about.md）
- `assets/` — 图片等资源，文章内用相对路径 `../../assets/xxx.png` 或站点根 `assets/xxx.png`
- `themes/` — 主题模板，可以按用户要求直接修改
- `public/` — 构建产物，**不要手工编辑**
- `blog.config.json` — 站点配置

## 文章规范

每篇文章开头必须有 frontmatter：

```markdown
---
title: 文章标题
date: 2026-07-11
tags: [生活, 随笔]
summary: 一句话摘要（可选，缺省取正文前 160 字）
draft: true
---

正文……
```

- 写作中的文章保持 `draft: true`，预览可见（带草稿标记），发布构建时排除。
- 用户确认定稿后删除 `draft` 行。

## 工作方式

- 用户让你写日志时：先用 `pjblog_new_post` 创建文件，再充实内容；写完提醒用户可以在浏览器实时预览。
- 用户说「预览」→ 调 `pjblog_preview`（action=start / open）。
- 用户说「发布」→ 调 `pjblog_publish`：先看变更摘要，用户确认后再带 confirm=true 执行。
- 修改主题样式时直接编辑 `themes/<当前主题>/` 下的文件，预览会自动刷新。
