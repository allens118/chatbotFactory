import streamlit as st
import factory_agent
import pandas as pd
import io

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

# 上傳檔案
uploaded_file = st.file_uploader("請上傳機台故障紀錄 (CSV)", type="csv")

if uploaded_file is not None:
    # 讀取並顯示原始資料
    uploaded_file.seek(0)  # 重置檔案指針
    content = uploaded_file.read().decode('utf-8-sig')
    df = pd.read_csv(io.StringIO(content))
    
    # 顯示資料統計
    st.write("資料統計：")
    st.write(f"總筆數：{len(df)} 筆")
    
    # 顯示資料預覽
    st.write("資料預覽：")
    preview_rows = st.slider("顯示筆數", 5, 50, 10)
    st.dataframe(df.head(preview_rows))
    
    # 問題輸入
    question = st.text_input("請輸入問題：")
    
    if question:
        # 處理問題
        uploaded_file.seek(0)  # 重置檔案指針
        response, downtime = factory_agent.ask_question(uploaded_file, question)
        
        # 顯示回答
        st.write("AI 回答")
        st.write(response)
        
        # 顯示停機時間
        st.write("停機時間分析")
        st.write(f"預估停機時間\n{downtime:.2f} 分鐘")
        
        # 檢查是否需要升級通知
        if downtime > 40:
            st.warning("⚠️ 須升級通知主管 (停機時間超過 40 分鐘)")
            st.info("建議立即聯繫相關主管進行處理")
        
        # 如果是生成新資料的請求，顯示新生成的資料
        if "生成" in question and ("狀態" in question or "資料" in question):
            # 重新讀取檔案以獲取更新後的資料
            uploaded_file.seek(0)  # 重置檔案指針
            content = uploaded_file.read().decode('utf-8-sig')
            updated_df = pd.read_csv(io.StringIO(content))
            
            # 顯示新生成的資料
            st.write("新生成的資料：")
            st.dataframe(updated_df.tail(10))  # 顯示最後10筆資料
            
            # 顯示更新後的資料統計
            st.write("更新後的資料統計：")
            st.write(f"總筆數：{len(updated_df)} 筆")
            
            # 提供下載更新後資料的選項
            csv = updated_df.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="下載更新後的資料",
                data=csv,
                file_name="updated_factory_data.csv",
                mime="text/csv"
            ) 