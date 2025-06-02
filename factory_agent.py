from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from downtime_model import estimate_downtime
import pandas as pd
import tempfile
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def ask_question(csv_file, question):
    """
    使用 LangChain 和 OpenAI 處理問題並返回回答
    """
    # 確保有設定 OpenAI API 金鑰
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("請設定 OPENAI_API_KEY 環境變數")

    # 將上傳的檔案暫存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(csv_file.read())
        tmp_path = tmp.name

    try:
        # 建立 LangChain agent
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        agent = create_csv_agent(
            llm,
            tmp_path,
            verbose=False
        )
        
        # 執行問題
        response = agent.run(question)
        
        # 計算停機時間
        downtime = estimate_downtime(response)
        
        return response, downtime
        
    finally:
        # 清理暫存檔案
        if os.path.exists(tmp_path):
            os.unlink(tmp_path) 