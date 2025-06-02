import re
from datetime import datetime

def estimate_downtime(response_text):
    """
    根據 AI 回答內容估算停機時間
    使用關鍵字和時間模式來判斷
    """
    # 基本停機時間
    base_time = 30
    
    # 檢查是否包含具體時間
    time_patterns = [
        r"\b(\d+)\s*(分鐘|min|分鐘)\b",
        r"\b(\d+)\s*(小時|hr|小時)\b",
        r"\b(\d+)\s*(天|day|天)\b"
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, response_text.lower())
        if match:
            value = int(match.group(1))
            if "小時" in pattern or "hr" in pattern:
                return value * 60
            elif "天" in pattern or "day" in pattern:
                return value * 24 * 60
            return value
    
    # 根據關鍵字調整停機時間
    keywords = {
        "escalation": 10,
        "waiting": 5,
        "network issue": 5,
        "sensor error": 15,
        "overheat": 20,
        "mechanical": 25,
        "electrical": 15,
        "software": 10
    }
    
    for keyword, additional_time in keywords.items():
        if keyword in response_text.lower():
            base_time += additional_time
    
    return base_time 