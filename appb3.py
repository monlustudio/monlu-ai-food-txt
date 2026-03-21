import streamlit as st

# --- 頁面配置 ---
st.set_page_config(page_title="夢廬 | AI 視覺導演", layout="wide")

# --- 視覺 CSS 優化 ---
st.markdown("""
    <style>
    /* 全域背景：莫蘭迪墨綠色 */
    .stApp { background-color: #1E2A23; color: #F1F3F2; }
    h1, h2, h3, p, span, label { color: #F1F3F2 !important; }
    
    /* 1. 琥珀古銅色按鈕：琥珀底 + 白色字 */
    div.stButton > button {
        background-color: #C5A47E !important;
        color: #FFFFFF !important;
        border-radius: 6px !important; 
        font-weight: bold !important; 
        border: none !important;
        width: 100% !important; 
        height: 55px !important; 
        font-size: 20px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button:hover {
        background-color: #D6C0A0 !important;
        transform: translateY(-2px) !important;
    }

    /* 2. 輸入框樣式 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stMultiSelect>div>div>div {
        background-color: #26362E !important; 
        color: #F1F3F2 !important;
        border: 1px solid #4B6355 !important;
    }
    ::placeholder { color: #BBBBBB !important; }

    /* 3. 偽裝 st.code：強制改為白底黑字、不分級 */
    .stCodeBlock {
        background-color: #FFFFFF !important;
        border: 3px solid #C5A47E !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stCodeBlock code {
        background-color: #FFFFFF !important;
        color: #000000 !important; /* 強制純黑字 */
        font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif !important;
        font-size: 18px !important;
        font-weight: normal !important;
        white-space: pre-wrap !important;
    }
    /* 修正複製按鈕的圖示顏色，避免在白底看不見 */
    .stCodeBlock button {
        color: #000000 !important;
        background-color: rgba(0,0,0,0.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 密碼驗證 ---
if "auth_v31" not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 100px; color: #C5A47E;'>🏯 夢廬 | 視覺導演系統</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        pwd = st.text_input("授權密碼", type="password", placeholder="請輸入授權碼...")
        if st.button("啟動系統 (Unlock)"):
            if pwd == "11090801":
                st.session_state["auth_v31"] = True
                st.rerun()
            else:
                st.error("密碼錯誤")
    st.stop()

# --- 主程式介面 ---
st.title("🎬 夢廬：AI 視覺導演助手 (V3.1)")
st.caption("已修復複製按鈕相容性。使用官方內建複製組件。")
st.markdown("---")

with st.form("vision_form"):
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.subheader("🏢 品牌與受眾")
        brand_name = st.text_input("餐廳名稱", placeholder="範例：初藏酒")
        cuisine_type = st.text_input("料理類型", placeholder="範例：日式居酒屋")
        target_group = st.text_input("目標客群定位", placeholder="範例：老饕、上班族...")
        age_range = st.slider("目標年齡範圍", 15, 80, (25, 45))
        style_tags = st.multiselect("核心風格調性", 
                                   ["人情味", "手作感", "高級感", "簡約", "文藝", "靜謐", "時尚", "現代", "傳統", "古樸", "奢華", "浮誇", "生活化", "深夜食堂"],
                                   default=["人情味", "深夜食堂"])
    with col2:
        st.subheader("📝 需求筆記")
        chat_notes = st.text_area("直接貼上客戶對話重點", height=320, placeholder="在此輸入筆記細節...")

    submit = st.form_submit_button("🚀 生成視覺提案提詞 (Generate Prompt)")

if submit:
    if not brand_name or not chat_notes:
        st.warning("⚠️ 請填寫必要資訊。")
    else:
        styles_str = "、".join(style_tags)
        
        final_prompt = f"""夢廬視覺提案報告：{brand_name}

品牌資料：
餐廳名稱：{brand_name} ({cuisine_type})
風格調性：{styles_str}
客群受眾：{age_range[0]}至{age_range[1]}歲 ({target_group})

需求核心：
{chat_notes}

----------

方向 A：顯性需求對應
🎨 風格重點：
💡 建議光線：
🌈 主要色彩：
🧱 桌板與背景材質：
🍽️ 餐具器皿選擇：
🌿 背景擺飾與道具：
🧠 為什麼這樣拍：

----------

方向 B：夢廬專業建議
🎨 風格重點：
💡 建議光線：
🌈 主要色彩：
🧱 桌板與背景材質：
🍽️ 餐具器皿選擇：
🌿 背景擺飾與道具：
🧠 為什麼這樣拍：

----------"""

        st.success("✅ 提詞已生成！")
        st.markdown("### 📋 點擊框框右上角圖示即可快速複製：")
        
        # 使用 st.code 並強制改寫 CSS，這是最穩定的方案
        st.code(final_prompt, language="text")