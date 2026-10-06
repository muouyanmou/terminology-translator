
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# 页面配置
st.set_page_config(page_title="多语言术语翻译器", layout="wide", initial_sidebar_state="collapsed")

st.title("🌐 多语言术语翻译器")
st.caption("输入术语 → 批量翻译 → 导出 Excel")

# 语言配置
LANGUAGES = {
    "中文": "zh-CN",
    "英文": "en",
    "日文": "ja",
    "韩文": "ko",
    "德文": "de",
    "法文": "fr",
    "西班牙文": "es",
    "意大利文": "it",
    "葡萄牙文": "pt",
    "荷兰文": "nl",
    "俄文": "ru",
    "阿拉伯文": "ar",
    "泰文": "th",
    "越南文": "vi",
    "印度尼西亚文": "id",
}

# 初始化 Session State
if "terms_list" not in st.session_state:
    st.session_state.terms_list = ["circuit breaker", "fuse", "relay"]
if "selected_langs" not in st.session_state:
    st.session_state.selected_langs = ["中文", "德文", "法文", "日文"]

# ────────────────────────────────────────────────────────────────────────────
# 1. 输入术语
# ────────────────────────────────────────────────────────────────────────────
st.subheader("📝 步骤 1：输入术语")
input_method = st.radio("选择输入方式", ["手工输入", "粘贴列表"], horizontal=True)

if input_method == "手工输入":
    terms_text = st.text_area(
        "输入术语（每行一个）",
        value="\n".join(st.session_state.terms_list),
        height=150,
        placeholder="circuit breaker\nfuse\nrelay\ncontactor"
    )
    terms = [t.strip() for t in terms_text.split("\n") if t.strip()]
else:
    terms_text = st.text_area(
        "粘贴术语列表（Excel/CSV 直接粘贴）",
        height=150,
        placeholder="也支持制表符分隔的格式"
    )
    # 处理制表符或逗号分隔
    lines = terms_text.split("\n")
    terms = []
    for line in lines:
        # 提取第一列（无论是制表符还是逗号分隔）
        cells = line.replace(",", "\t").split("\t")
        if cells[0].strip():
            terms.append(cells[0].strip())

if terms:
    st.session_state.terms_list = terms
    st.success(f"✅ 已识别 {len(terms)} 个术语")

# ────────────────────────────────────────────────────────────────────────────
# 2. 选择目标语言
# ────────────────────────────────────────────────────────────────────────────
st.subheader("🌍 步骤 2：选择目标语言")
cols = st.columns(4)
selected_langs = []
for i, (lang, code) in enumerate(LANGUAGES.items()):
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
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_tasks = len(terms) * len(selected_langs)
        completed = 0
        
        for target_lang in selected_langs:
            target_code = LANGUAGES[target_lang]
            translations = []
            
            for term in terms:
                try:
                    # 自动检测源语言
                    translated = GoogleTranslator(source="auto", target=target_code).translate(term)
                    translations.append(translated)
                except Exception as e:
                    translations.append(f"[错误]")
                
                completed += 1
                progress = completed / total_tasks
                progress_bar.progress(progress)
                status_text.text(f"翻译进度：{completed}/{total_tasks}")
        
            result_df[target_lang] = translations
        
        progress_bar.empty()
        status_text.empty()
        
        # 显示结果
        st.success("✅ 翻译完成！")
        st.dataframe(result_df, use_container_width=True, hide_index=True)
        
        # 导出 Excel
        st.subheader("📥 导出结果")
        
        # 创建 Excel
        output_file = "术语翻译表.xlsx"
        result_df.to_excel(output_file, index=False, sheet_name="术语", engine="openpyxl")
        
        # 美化 Excel（可选，需要 openpyxl）
        from openpyxl import load_workbook
        wb = load_workbook(output_file)
        ws = wb.active
        for col in ws.columns:
            max_len = 0
            for cell in col:
                max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 50)
        wb.save(output_file)
        
        with open(output_file, "rb") as f:
            st.download_button(
                label="⬇️ 下载 Excel",
                data=f.read(),
                file_name=output_file,
                mime="application/vnd.ms-excel",
                use_container_width=True
            )

st.divider()
st.caption("💡 提示：支持自动检测源语言，无需手动选择。翻译基于 Google Translate。")
