from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from downtime_model import estimate_downtime
import pandas as pd
import tempfile
import os
from pathlib import Path
import logging
import random
from datetime import datetime, timedelta
import io

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

def generate_mock_data(num_records=10):
    """
    生成模擬的機台故障資料
    """
    error_types = [
        "Overheat", "Network issue", "Sensor error", "Mechanical",
        "Electrical", "Software", "Hydraulic", "Pneumatic",
        "Control system", "Power supply"
    ]
    
    machines = [f"Machine{chr(65+i)}" for i in range(5)]  # MachineA to MachineE
    
    descriptions = {
        "Overheat": ["機器過熱，需要冷卻", "溫度過高，自動停機", "散熱系統故障"],
        "Network issue": ["網路連線中斷", "網路延遲", "通訊模組故障"],
        "Sensor error": ["感測器異常", "溫度感測器故障", "壓力感測器讀數異常"],
        "Mechanical": ["機械零件磨損", "軸承故障", "皮帶斷裂"],
        "Electrical": ["電路板故障", "電源供應不穩", "馬達過載"],
        "Software": ["軟體更新失敗", "程式執行錯誤", "系統當機"],
        "Hydraulic": ["液壓系統洩漏", "油壓不足", "液壓泵故障"],
        "Pneumatic": ["氣壓系統故障", "氣閥阻塞", "氣壓不足"],
        "Control system": ["控制系統異常", "PLC故障", "程式邏輯錯誤"],
        "Power supply": ["電源供應中斷", "電壓不穩", "保險絲燒斷"]
    }
    
    # 生成起始時間
    start_time = datetime.now() - timedelta(days=7)
    
    data = []
    for _ in range(num_records):
        error_type = random.choice(error_types)
        machine = random.choice(machines)
        repair_time = random.randint(15, 120)  # 15-120分鐘
        description = random.choice(descriptions[error_type])
        
        # 生成時間，確保按順序
        time = start_time + timedelta(hours=random.randint(1, 24))
        start_time = time
        
        data.append({
            "Time": time.strftime("%Y-%m-%d %H:%M"),
            "Machine": machine,
            "ErrorType": error_type,
            "RepairTime": repair_time,
            "Description": description
        })
    
    return pd.DataFrame(data)

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
            # 檢查是否要求生成新資料
            if "生成" in question and ("狀態" in question or "資料" in question):
                # 讀取原始資料
                csv_file.seek(0)
                content = csv_file.read().decode('utf-8-sig')
                original_data = pd.read_csv(io.StringIO(content))
                
                # 生成新的模擬資料
                new_data = generate_mock_data(10)
                
                # 合併資料
                combined_data = pd.concat([original_data, new_data], ignore_index=True)
                
                # 將合併後的資料寫入檔案
                csv_file.seek(0)
                csv_file.truncate()
                output = combined_data.to_csv(index=False, encoding='utf-8-sig')
                csv_file.write(output.encode('utf-8-sig'))
                csv_file.seek(0)
                
                # 生成回答
                response = "已成功生成新的模擬資料！\n\n"
                response += "新增資料摘要：\n"
                response += f"- 新增筆數：10 筆\n"
                response += f"- 故障類型：{', '.join(new_data['ErrorType'].unique())}\n"
                response += f"- 平均修復時間：{new_data['RepairTime'].mean():.1f} 分鐘\n"
                response += f"- 最短修復時間：{new_data['RepairTime'].min()} 分鐘\n"
                response += f"- 最長修復時間：{new_data['RepairTime'].max()} 分鐘\n\n"
                response += f"更新後總資料筆數：{len(combined_data)} 筆"
                
                # 計算平均停機時間
                downtime = new_data["RepairTime"].mean()
                
                return response, downtime

            # 一般問題處理
            csv_file.seek(0)
            content = csv_file.read().decode('utf-8-sig')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding='utf-8-sig') as tmp:
                tmp.write(content)
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