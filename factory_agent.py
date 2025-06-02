from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from downtime_model import estimate_downtime
import pandas as pd
import tempfile
import os
from pathlib import Path
import logging

# 設定日誌
logger = logging.getLogger(__name__)

def get_api_key():
    """
    從環境變數或檔案讀取 API Key
    """
    # 優先從環境變數讀取
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 其次從檔案讀取
    api_key_file = Path(__file__).parent / "api_key.txt"
    if api_key_file.exists():
        with open(api_key_file, "r") as f:
            return f.read().strip()

    raise ValueError(
        "找不到 OpenAI API Key。請選擇以下其中一種方式設定：\n"
        "1. 設定環境變數 OPENAI_API_KEY\n"
        "2. 在專案根目錄建立 api_key.txt 檔案並放入 API Key"
    )

class FactoryAgent:
    """工廠代理類別，用於處理工廠相關的查詢"""
    
    def __init__(self):
        self.api_key = get_api_key()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            api_key=self.api_key
        )

    def ask_question(self, csv_file, question: str) -> tuple[str, float]:
        """
        處理使用者的問題並返回回答

        Args:
            csv_file: 上傳的 CSV 檔案
            question: 使用者的問題

        Returns:
            tuple[str, float]: (回答, 預估停機時間)

        Raises:
            ValueError: 當 API Key 無效時
            Exception: 其他錯誤
        """
        tmp_path = None
        try:
            # 將上傳的檔案暫存
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                tmp.write(csv_file.read())
                tmp_path = tmp.name

            # 建立 LangChain agent
            agent = create_csv_agent(
                self.llm,
                tmp_path,
                verbose=False
            )
            
            # 執行問題
            logger.info(f"處理問題: {question}")
            response = agent.run(question)
            
            # 計算停機時間
            downtime = estimate_downtime(response)
            logger.info(f"預估停機時間: {downtime} 分鐘")
            
            return response, downtime
            
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                logger.error("API Key 驗證失敗")
                raise ValueError(
                    "API Key 驗證失敗。請確認：\n"
                    "1. API Key 是否正確\n"
                    "2. API Key 是否已啟用\n"
                    "3. 是否有足夠的額度"
                ) from e
            logger.error(f"處理問題時發生錯誤: {e}")
            raise
            
        finally:
            # 清理暫存檔案
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    logger.warning(f"清理暫存檔案時發生錯誤: {e}")

# 建立全域實例
factory_agent = FactoryAgent()

# 提供便捷的存取方法
def ask_question(csv_file, question: str) -> tuple[str, float]:
    """處理問題的便捷方法"""
    return factory_agent.ask_question(csv_file, question)

def ask_question_old(csv_file, question):
    """
    使用 LangChain 和 OpenAI 處理問題並返回回答
    """
    # 取得 API Key
    api_key = get_api_key()

    # 將上傳的檔案暫存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(csv_file.read())
        tmp_path = tmp.name

    try:
        # 建立 LangChain agent
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=api_key
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