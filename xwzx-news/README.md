# xwzx-news · 头条新闻前端

基于 Vue 3 + Vite 构建的移动端新闻资讯应用，配套后端为同仓库的 [`toutiao_bachend`](../toutiao_bachend)（FastAPI）。

## 技术栈

- Vue 3.5 + Vite 7
- Vue Router 4、Pinia 3（含 `pinia-plugin-persistedstate` 本地持久化）
- Vant 4 移动端组件库
- vue-i18n 9（中/英双语）、axios、marked + DOMPurify（AI 回答的 Markdown 渲染）

## 目录结构

```
src/
├── components/     # 通用组件（TabBar、NewsItem 等）
├── views/          # 页面：首页、分类、详情、收藏、历史、我的、设置、登录注册、AI 问答
├── store/          # Pinia 状态：user / news / favorite / history / theme / language
├── router/         # 路由表
├── i18n/           # 国际化文案
└── config/api.js   # 后端地址与 AI 接口配置
```

## 快速开始

```bash
npm install
npm run dev
```

浏览器打开终端提示的地址（默认 http://localhost:5173）。

## 环境变量

AI 问答使用 DeepSeek 接口，密钥通过环境变量注入，**不要把真实密钥提交到仓库**：

1. 复制 `.env.example` 为 `.env`
2. 填入自己的密钥：`VITE_DEEPSEEK_API_KEY=sk-...`

未配置时 AI 聊天页会提示 "API Key 未配置"，其他功能不受影响。

## 后端地址

默认指向 `http://127.0.0.1:8000`，在 [`src/config/api.js`](src/config/api.js) 的 `apiConfig.baseURL` 中修改。

## 构建

```bash
npm run build     # 产物输出到 dist/
npm run preview   # 本地预览构建结果
```
