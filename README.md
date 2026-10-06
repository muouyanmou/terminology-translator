# 🌐 多语言术语翻译器

一键输入术语，批量翻译成 16+ 种语言，直接导出 Excel。**无需本地安装 Python，点开链接即用。**

## 功能
- ✅ 支持 16 种语言
- ✅ 精准翻译（自动重试机制）
- ✅ 批量翻译
- ✅ 一键导出 Excel
- ✅ 完全免费云端托管

## 快速开始

### 1️⃣ 上传到 GitHub
1. 登录 GitHub 账号
2. 创建新仓库：`terminology-translator`
3. 上传文件：`app.py`、`requirements.txt`、`README.md`

### 2️⃣ 部署到 Streamlit Cloud
1. 访问 https://share.streamlit.io
2. 点 **"New app"**
3. 选择仓库 → main 分支 → app.py
4. 点 **"Deploy"**（等 1-2 分钟）

### 3️⃣ 分享链接
部署完成后自动生成公开链接：
```
https://terminology-translator-xxxx.streamlit.app
```

---

## 使用示例

### 英文 → 中文、日文、德文

**输入**
```
circuit breaker
fuse
relay
```

**选择**
- 源语言：英文
- 目标语言：中文（简体）、日文、德文

**结果（Excel）**
```
术语           │ 中文   │ 日文   │ 德文
─────────────────┼────────┼────────┼──────────────
circuit breaker │ 断路器 │ 遮断器 │ Leistungsschalter
fuse            │ 保险丝 │ ヒューズ │ Sicherung
relay           │ 继电器 │ リレー │ Relais
```

---

## 支持的语言

中文（简体）、中文（繁体）、英文、日文、韩文、德文、法文、西班牙文、意大利文、葡萄牙文、俄文、荷兰文、瑞典文、丹麦文、芬兰文、波兰文

---

## 常见问题

**Q: 翻译出现错误怎么办？**
A: 检查网络连接，刷新页面重试。如果仍然出现问题，可能是 Google API 限流，稍候再试。

**Q: 支持离线使用吗？**
A: 不支持，需要网络连接。

**Q: 翻译准确度如何？**
A: 基于 Google Translate，技术术语一般准确，建议人工审核。

---

**License** MIT
