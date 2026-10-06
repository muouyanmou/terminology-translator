
import streamlit as st
import pandas as pd
import time
import requests
from urllib.parse import quote

# 页面配置
st.set_page_config(page_title="多语言术语翻译器", layout="wide", initial_sidebar_state="collapsed")

st.title("🌐 多语言术语翻译器")
st.caption("输入术语 → 批量翻译 → 导出 Excel")

# 语言配置和代码映射
LANGUAGES = {
    "中文（简体）": "zh-CN",
    "中文（繁体）": "zh-TW",
    "英文": "en",
    "日文": "ja",
    "韩文": "ko",
    "德文": "de",
    "法文": "fr",
    "西班牙文": "es",
    "意大利文": "it",
    "葡萄牙文": "pt",
    "俄文": "ru",
    "荷兰文": "nl",
}

# API 语言代码映射
GOOGLE_LANG_MAP = {
    "中文（简体）": "zh-CN",
    "中文（繁体）": "zh-TW",
    "英文": "en",
    "日文": "ja",
    "韩文": "ko",
    "德文": "de",
    "法文": "fr",
    "西班牙文": "es",
    "意大利文": "it",
    "葡萄牙文": "pt",
    "俄文": "ru",
    "荷兰文": "nl",
}

def translate_google_api(text, source_lang, target_lang):
    """使用 Google Translate API（免费）翻译"""
    try:
        # 使用 Google Translate 的免费 API 端点
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={quote(text)}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        if result and result[0]:
            translations = [item[0] for item in result[0] if item[0]]
            if translations:
                return "".join(translations)
        
        return text
    except Exception as e:
        st.warning(f"翻译出错（{target_lang}）：{str(e)}")
        return text

# 初始化 Session State
if "terms_list" not in st.session_state:
    st.session_state.terms_list = ["circuit breaker", "fuse", "relay"]
if "selected_langs" not in st.session_state:
    st.session_state.selected_langs = ["中文（简体）", "日文"]
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "英文"

# ────────────────────────────────────────────────────────────────────────────
# 0. 选择源语言
# ────────────────────────────────────────────────────────────────────────────
st.subheader("🔤 步骤 0：选择源语言")
st.write("⚠️ **重要**：请根据你输入术语的语言选择。如果输入的是英文术语，请选择**英文**；如果是中文术语，请选择**中文**。")

source_lang = st.radio(
    "输入术语的语言是？",
    ["英文", "中文（简体）", "中文（繁体）", "日文", "德文", "法文"],
    horizontal=True
)
st.session_state.source_lang = source_lang

# ────────────────────────────────────────────────────────────────────────────
# 1. 输入术语
# ────────────────────────────────────────────────────────────────────────────
st.subheader("📝 步骤 1：输入术语")

terms_text = st.text_area(
    f"输入术语（{source_lang}，每行一个）",
    value="\n".join(st.session_state.terms_list),
    height=120,
    placeholder="circuit breaker\nfuse\nrelay\ncontactor"
)

terms = [t.strip() for t in terms_text.split("\n") if t.strip()]

if terms:
    st.session_state.terms_list = terms
    st.info(f"✅ 已识别 {len(terms)} 个术语")

# ────────────────────────────────────────────────────────────────────────────
# 2. 选择目标语言
# ────────────────────────────────────────────────────────────────────────────
st.subheader("🌍 步骤 2：选择目标语言")

target_options = [l for l in LANGUAGES.keys() if l != source_lang]

cols = st.columns(4)
selected_langs = []
for i, lang in enumerate(target_options):
    with cols[i % 4]:
        if st.checkbox(lang, value=lang in st.session_state.selected_langs, key=f"lang_{lang}"):
            selected_langs.append(lang)

if selected_langs:
    st.session_state.selected_langs = selected_langs

# ────────────────────────────────────────────────────────────────────────────
# 3. 翻译
# ────────────────────────────────────────────────────────────────────────────
st.subheader("⚙️ 步骤 3：批量翻译")

if st.button("🚀 开始翻译", type="primary", use_container_width=True):
    if not terms:
        st.error("❌ 请先输入术语")
    elif not selected_langs:
        st.error("❌ 请至少选择一个目标语言")
    else:
        # 创建结果表
        result_df = pd.DataFrame({"术语": terms})
        
        # 显示进度
        progress_container = st.container()
        
        source_code = GOOGLE_LANG_MAP[source_lang]
        total_tasks = len(terms) * len(selected_langs)
        completed = 0
        
        # 逐个语言翻译
        for target_lang in selected_langs:
            target_code = GOOGLE_LANG_MAP[target_lang]
            translations = []
            
            for term in terms:
                try:
                    # 调用翻译 API
                    translated = translate_google_api(term, source_code, target_code)
                    translations.append(translated)
                except Exception as e:
                    translations.append(term)
                
                completed += 1
                progress = min(completed / total_tasks, 1.0)
                
                with progress_container:
                    st.progress(progress, text=f"翻译进度：{completed}/{total_tasks}")
                
                time.sleep(0.2)  # 避免请求过快
        
            result_df[target_lang] = translations
        
        progress_container.empty()
        
        # 显示结果
        st.success("✅ 翻译完成！")
        st.dataframe(result_df, use_container_width=True, hide_index=True)
        
        # 导出 Excel
        st.subheader("📥 导出结果")
        
        try:
            # 创建 Excel
            output_file = "术语翻译表.xlsx"
            result_df.to_excel(output_file, index=False, sheet_name="术语", engine="openpyxl")
            
            # 美化 Excel
            from openpyxl import load_workbook
            from openpyxl.styles import Font, PatternFill
            
            wb = load_workbook(output_file)
            ws = wb.active
            
            # 设置列宽和表头样式
            for col_idx, col in enumerate(ws.columns, 1):
                max_len = 0
                for cell in col:
                    max_len = max(max_len, len(str(cell.value)))
                ws.column_dimensions[chr(64 + col_idx)].width = min(max_len + 3, 60)
                
                # 表头加粗 + 红色背景
                if col_idx > 0:
                    ws.cell(row=1, column=col_idx).font = Font(bold=True, color="FFFFFF")
                    ws.cell(row=1, column=col_idx).fill = PatternFill(start_color="FF000F", end_color="FF000F", fill_type="solid")
            
            wb.save(output_file)
            
            with open(output_file, "rb") as f:
                st.download_button(
                    label="⬇️ 下载 Excel",
                    data=f.read(),
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"导出 Excel 失败：{e}")

st.divider()
st.caption("💡 提示：翻译基于 Google Translate 免费 API。网络连接稳定最佳。")
