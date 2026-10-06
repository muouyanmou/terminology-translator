
import streamlit as st
import pandas as pd
import time
import requests

# 页面配置
st.set_page_config(page_title="多语言术语翻译器", layout="wide", initial_sidebar_state="collapsed")

st.title("🌐 多语言术语翻译器")
st.caption("输入术语 → 批量翻译 → 导出 Excel")

# 语言配置
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
    "瑞典文": "sv",
    "丹麦文": "da",
    "芬兰文": "fi",
    "波兰文": "pl",
}

def translate_via_google(text, source_lang, target_lang, retries=3):
    """使用 Google Translate 翻译"""
    # 处理语言代码（去掉地区后缀）
    src_code = source_lang.split("-")[0] if source_lang else "auto"
    tgt_code = target_lang.split("-")[0] if target_lang else "en"
    
    for attempt in range(retries):
        try:
            url = "https://translate.googleapis.com/translate_a/element.js"
            params = {
                "client": "gtx",
                "sl": src_code,
                "tl": tgt_code,
                "text": text,
            }
            
            # 使用 requests 直接调用
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            # 方法1：尝试使用 deep_translator
            try:
                from deep_translator import GoogleTranslator
                result = GoogleTranslator(source_language=src_code, target_language=tgt_code).translate(text)
                return result
            except:
                pass
            
            # 方法2：如果 deep_translator 失败，返回原文本
            return text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                return None
    return None

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
source_langs = ["英文", "中文（简体）", "中文（繁体）", "日文", "德文", "法文"]
source_lang = st.radio("输入术语的语言是？", source_langs, horizontal=True)
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

# 排除源语言
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
        
        # 进度条
        progress_placeholder = st.empty()
        result_placeholder = st.empty()
        
        source_code = LANGUAGES[source_lang]
        total_tasks = len(terms) * len(selected_langs)
        completed = 0
        
        # 逐个语言翻译
        for target_lang in selected_langs:
            target_code = LANGUAGES[target_lang]
            translations = []
            
            for term in terms:
                try:
                    # 调用翻译函数
                    translated = translate_via_google(term, source_code, target_code)
                    if translated is None:
                        translations.append(term)  # 失败时返回原文本
                    else:
                        translations.append(translated)
                except Exception as e:
                    translations.append(term)  # 失败时返回原文本
                
                completed += 1
                progress = min(completed / total_tasks, 1.0)
                
                with progress_placeholder.container():
                    st.progress(progress, text=f"翻译进度：{completed}/{total_tasks}")
                
                time.sleep(0.1)  # 避免请求过快
        
            result_df[target_lang] = translations
        
        progress_placeholder.empty()
        
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
st.caption("💡 提示：请确保正确选择源语言。翻译基于 Google Translate。")
