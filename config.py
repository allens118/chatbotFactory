"""
設定檔，用於管理應用程式的設定
"""
import os
from pathlib import Path
from typing import Optional
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """應用程式設定類別"""
    
    def __init__(self):
        self.ROOT_DIR = Path(__file__).parent
        self.API_KEY_FILE = self.ROOT_DIR / "api_key.txt"
        self._api_key: Optional[str] = None

    def get_api_key(self) -> str:
        """
        取得 OpenAI API Key
        
        Returns:
            str: API Key
            
        Raises:
            ValueError: 當找不到有效的 API Key 時
        """
        if self._api_key:
            return self._api_key

        # 優先從環境變數讀取
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            logger.info("從環境變數讀取 API Key")
            self._api_key = api_key
            return api_key

        # 其次從檔案讀取
        if self.API_KEY_FILE.exists():
            try:
                with open(self.API_KEY_FILE, "r") as f:
                    api_key = f.read().strip()
                if api_key:
                    logger.info("從檔案讀取 API Key")
                    self._api_key = api_key
                    return api_key
            except Exception as e:
                logger.error(f"讀取 API Key 檔案時發生錯誤: {e}")

        # 如果都找不到，提供詳細的錯誤訊息
        error_msg = (
            "無法找到有效的 OpenAI API Key。\n\n"
            "請選擇以下其中一種方式設定：\n"
            "1. 設定環境變數：\n"
            "   Windows PowerShell:\n"
            "   $env:OPENAI_API_KEY='your-api-key'\n\n"
            "2. 建立設定檔：\n"
            f"   在 {self.ROOT_DIR} 目錄下建立 api_key.txt 檔案\n"
            "   並將 API Key 放入檔案中\n\n"
            "注意：API Key 格式應為 'sk-' 開頭的字串"
        )
        raise ValueError(error_msg)

# 建立全域設定實例
config = Config()

# 提供便捷的存取方法
def get_api_key() -> str:
    """取得 API Key 的便捷方法"""
    return config.get_api_key() 