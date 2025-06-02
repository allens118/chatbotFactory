import streamlit as st
import factory_agent
from downtime_model import estimate_downtime

st.set_page_config(
    page_title="工廠 AI 聊天助理",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 工廠 AI 聊天助理")

# 側邊欄說明
with st.sidebar:
    st.header("使用說明")
    st.markdown("""
    1. 上傳機台故障紀錄 CSV 檔案
    2. 輸入您想詢問的問題
    3. 系統會自動分析並提供回答
    4. 若停機時間超過 40 分鐘，系統會自動發出升級通知
    """)

# 檔案上傳區
uploaded_file = st.file_uploader("請上傳機台故障紀錄 (CSV)", type="csv")

if uploaded_file:
    # 問題輸入區
    user_question = st.text_input("請輸入問題：", placeholder="例如：這台機器為什麼昨天停機？")
    
    if user_question:
        with st.spinner("AI 正在分析中..."):
            answer, downtime = factory_agent.ask_question(uploaded_file, user_question)
            
            # 顯示回答
            st.markdown("### AI 回答")
            st.markdown(f"{answer}")
            
            # 顯示停機時間
            st.markdown("### 停機時間分析")
            st.metric("預估停機時間", f"{downtime:.2f} 分鐘")
            
            # 升級通知判斷
            if downtime > 40:
                st.warning("⚠️ 須升級通知主管 (停機時間超過 40 分鐘)")
                st.info("建議立即聯繫相關主管進行處理") 