import streamlit as st
from openai import OpenAI

# --- 1. 頁面配置 ---
st.set_page_config(page_title="夢廬 | AI 視覺導演", layout="wide")

# --- 2. 經典莫蘭迪墨綠古銅配色 CSS ---
st.markdown("""
    <style>
    /* 全域背景：莫蘭迪墨綠色 */
    .stApp { background-color: #1E2A23; color: #F1F3F2; }
    h1, h2, h3, p, span, label { color: #F1F3F2 !important; }
    
    /* 琥珀古銅色按鈕：琥珀底 + 白色字 */
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

    /* 輸入框與滑桿樣式 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stMultiSelect>div>div>div {
        background-color: #26362E !important; 
        color: #F1F3F2 !important;
        border: 1px solid #4B6355 !important;
    }
    ::placeholder { color: #8A9A91 !important; }
    .stSlider > div > div > div > div { background-color: #C5A47E !important; }

    /* 偽裝 st.code：純白底、純黑字、不分級 */
    .stCodeBlock {
        background-color: #FFFFFF !important;
        border: 3px solid #C5A47E !important;
        border-radius: 10px !important;
    }
    .stCodeBlock code {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif !important;
        font-size: 18px !important;
        font-weight: normal !important;
        white-space: pre-wrap !important;
    }
    /* 修正複製按鈕顏色 */
    .stCodeBlock button { color: #000000 !important; background-color: rgba(0,0,0,0.05) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. OpenAI API 設定 ---
client = OpenAI(api_key="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")

# --- 4. 密碼驗證 ---
if "auth_v33" not in st.session_state:
    st.markdown("<h1 style='text-align: center; margin-top: 100px; color: #C5A47E;'>🏯 夢廬 | 視覺導演系統</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        pwd = st.text_input("授權密碼", type="password", placeholder="請輸入 8 位數授權碼...")
        if st.button("啟動系統 (Unlock)"):
            if pwd == "11090801":
                st.session_state["auth_v33"] = True
                st.rerun()
            else:
                st.error("密碼錯誤")
    st.stop()

# --- 5. 主程式介面 ---
st.title("🎬 夢廬：AI 視覺導演助手 (V3.3)")
st.caption("OpenAI 引擎已驅動。琥珀按鈕與純白報告框準備就緒。")
st.markdown("---")

with st.form("vision_form"):
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.subheader("🏢 品牌與受眾")
        brand_name = st.text_input("餐廳名稱", placeholder="範例：初藏酒")
        cuisine_type = st.text_input("料理類型", placeholder="範例：日式居酒屋")
        target_group = st.text_input("目標客群", placeholder="範例：商務人士、老饕...")
        age_range = st.slider("目標年齡範圍", 15, 80, (25, 45))
        style_tags = st.multiselect("核心風格調性", 
                                   ["人情味", "手作感", "高級感", "簡約", "文藝", "靜謐", "時尚", "現代", "傳統", "古樸", "奢華", "浮誇", "生活化", "深夜食堂"],
                                   default=["人情味", "深夜食堂"])
    with col2:
        st.subheader("📝 需求筆記")
        chat_notes = st.text_area("直接貼上對話重點", height=320, placeholder="在此輸入筆記細節...")

    submit = st.form_submit_button("🚀 生成視覺提案報告 (Generate Report)")

# --- 6. 執行生成 ---
if submit:
    if not brand_name or not chat_notes:
        st.warning("⚠️ 資訊不完整。")
    else:
        with st.spinner("夢廬 AI 導演正在運用 GPT-4o 構思提案..."):
            try:
                styles_str = "、".join(style_tags)
                
                prompt_content = f"""
                你是一位專業美食攝影導演，隸屬「夢廬攝影工作室」。
                請產出 A、B 兩套精簡報告。嚴禁使用 #、* 或任何 Markdown 標點語法。
                
                報告標題：夢廬視覺提案報告 - {brand_name}
                
                【品牌基本資料】
                餐廳名稱：{brand_name} ({cuisine_type})
                風格調性：{styles_str}
                客群受眾：{age_range[0]}至{age_range[1]}歲 ({target_group})
                
                【需求核心】
                {chat_notes}
                
                請嚴格依照以下格式輸出純文字：
                ----------
                方向 A：顯性需求對應
                🎨 風格重點：
                💡 建議光線：
                🌈 主要色彩：
                🧱 桌板與背景材質：
                🍽️ 餐具器皿選擇：
                🌿 背景擺飾與道具：
                🧠 執行邏輯：
                ----------
                方向 B：夢廬專業建議
                🎨 風格重點：
                💡 建議光線：
                🌈 主要色彩：
                🧱 桌板與背景材質：
                🍽️ 餐具器皿選擇：
                🌿 背景擺飾與道具：
                🧠 執行邏輯：
                ----------
                """

                # 呼叫 OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt_content}]
                )
                
                result_text = response.choices[0].message.content
                
                st.success("✅ 視覺提案已生成！")
                st.markdown("### 📋 點擊右上方圖示快速複製報告內容：")
                
                # 顯示結果
                st.code(result_text, language="text")
                
            except Exception as e:
                st.error(f"生成失敗：{e}")