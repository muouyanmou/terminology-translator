# 🌐 多语言术语翻译器

一键输入术语，批量翻译成 15+ 种语言，直接导出 Excel。**无需本地安装 Python，点开链接即用。**

## 功能
- ✅ 支持 15 种语言
- ✅ 自动检测源语言（中文或英文）
- ✅ 批量翻译
- ✅ 一键导出 Excel
- ✅ 完全免费云端托管

## 快速开始（部署到云端，3 步）

### 1️⃣ 创建 GitHub 仓库
1. 登录 GitHub 账号（没有的话先注册）
2. 创建新仓库：`terminology-translator`
3. 上传以下文件到仓库：
   - `app.py`
   - `requirements.txt`
   - `README.md`

### 2️⃣ 在 Streamlit Cloud 部署
1. 访问 https://share.streamlit.io
2. 点击 **"New app"**
3. 连接 GitHub 账号
4. 填写：
   - Repository: `your-username/terminology-translator`
   - Branch: `main`
   - Main file path: `app.py`
5. 点击 **"Deploy"**

### 3️⃣ 分享链接
部署完成后，你会获得一个公开链接，例如：
```
https://terminology-translator-xxxx.streamlit.app
```

分享这个链接给团队，所有人点开就能用，无需任何安装。

---

## 本地运行（可选）

如果你想本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
streamlit run app.py
```

访问 http://localhost:8501

---

## 使用示例

**输入** → **选择语言** → **翻译** → **下载 Excel**

```
输入术语：
circuit breaker
fuse
relay

选择语言：
☑️ 中文  ☑️ 日文  ☑️ 德文  ☑️ 法文

结果（Excel）：
┌─────────────────┬────────┬──────┬────────┬────────┐
│      术语        │  中文   │ 日文 │  德文  │  法文  │
├─────────────────┼────────┼──────┼────────┼────────┤
│ circuit breaker │  断路器 │ 遮断器 │ ...    │ ...    │
│ fuse            │   保险丝 │ ヒューズ │ ...    │ ...    │
│ relay           │   继电器 │ リレー │ ...    │ ...    │
└─────────────────┴────────┴──────┴────────┴────────┘
```

---

## 常见问题

**Q: 需要付费吗？**
A: 完全免费。Streamlit Cloud 免费额度足够日常使用。

**Q: 支持哪些语言？**
A: 中文、英文、日文、韩文、德文、法文、西班牙文、意大利文、葡萄牙文、荷兰文、俄文、阿拉伯文、泰文、越南文、印度尼西亚文。

**Q: 翻译准确度如何？**
A: 基于 Google Translate，专业术语建议人工审核。

**Q: 能离线使用吗？**
A: 不能，需要网络连接。

---

## 后续改进
- [ ] 接入 DeepL API（更高质量翻译）
- [ ] 支持自定义词库
- [ ] 支持 CSV 导入
- [ ] 翻译历史记录

---

**作者** | **License** MIT
