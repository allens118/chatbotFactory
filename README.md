# 🧠 工廠 AI 聊天助理 (Factory AI Chatbot)

這個專案實作了一個混合式 AI 聊天機器人，旨在幫助工廠管理人員分析機台故障紀錄並提供即時的洞察和升級建議。

## ✨ 功能特色

- **前端界面 (Streamlit)**：直觀易用的介面，支援 CSV 檔案上傳和自然語言問答。
- **後端智能 (LangChain + OpenAI)**：整合 LangChain 的 CSV Agent 和 OpenAI 的 GPT 模型進行故障分析和回答。
- **停機時間估算**：根據 AI 分析結果和內建規則估算機台停機時間。
- **自動升級通知**：當預估停機時間超過設定門檻時，自動提示需要升級處理。

## 📂 專案結構

```
chatbot_factory/
├── app.py                 ← Streamlit 主介面
├── factory_agent.py       ← LangChain 整合邏輯與 GPT 回答
├── downtime_model.py      ← 停機時間模型實作
├── example_data.csv       ← 測試資料
├── requirements.txt       ← 專案依賴套件
├── .env                   ← 環境變數 (存放 API 金鑰)
└── README.md              ← 專案說明檔案
```

## 🔧 環境建置與安裝

1.  **複製專案儲存庫**：

    ```bash
    git clone git@github.com:allens118/chatbotFactory.git
    cd chatbotFactory
    ```

2.  **建立並啟用虛擬環境 (建議)**：

    *   Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **安裝所需套件**：

    ```bash
    pip install -r requirements.txt
    ```

4.  **設定 OpenAI API 金鑰**：

    *   複製 `.env.example` (如果存在的話) 或直接創建一個名為 `.env` 的檔案。
    *   在 `.env` 檔案中加入您的 OpenAI API 金鑰：
        ```dotenv
        OPENAI_API_KEY=your_api_key_here
        ```
    *   **請將 `your_api_key_here` 替換為您的實際 OpenAI API 金鑰。**

## ▶️ 如何運行

在專案根目錄下，確保您已經啟用了虛擬環境，然後執行以下指令啟動 Streamlit 應用程式：

```bash
streamlit run app.py
```

應用程式將會在您的預設瀏覽器中開啟 (通常是 `http://localhost:8501`)。

## 🚀 如何使用

1.  開啟 Streamlit 應用程式。
2.  點擊「請上傳機台故障紀錄 (CSV)」按鈕，選擇您的 CSV 檔案。您可以使用 `example_data.csv` 進行測試。
3.  在「請輸入問題：」文字框中輸入您想詢問關於故障紀錄的問題，例如：「機器A昨天為什麼停機？」或「哪些故障類型導致停機時間超過40分鐘？」。
4.  按下 Enter 或等待 AI 分析完成。
5.  應用程式將顯示 AI 的回答、預估的停機時間，以及是否需要升級處理的通知。

## 📉 停機時間估算邏輯

停機時間的估算基於 `downtime_model.py` 中的邏輯：

-   首先檢查 AI 回答中是否包含具體的停機時間數值 (分鐘、小時、天)。
-   如果沒有找到具體時間，則使用一個基本停機時間 (預設 30 分鐘)。
-   根據 AI 回答中包含的特定關鍵字 (如 escalation, waiting, network issue, sensor error, overheat 等) 增加額外的時間。

## ⚠️ 升級通知邏輯

應用程式會檢查 `downtime_model.py` 估算的停機時間。如果停機時間超過 **40 分鐘**，則會在界面上顯示警告訊息，提示需要升級通知主管。

## 📊 範例資料 (example_data.csv)

```csv
Time,Machine,ErrorType,RepairTime,Description
2024-03-20 08:00,MachineA,Overheat,35,機器過熱，需要冷卻
2024-03-20 09:00,MachineB,Network issue,55,網路連線中斷
2024-03-20 10:00,MachineC,Sensor error,25,感測器異常
2024-03-20 11:00,MachineA,Mechanical,45,機械零件磨損
2024-03-20 12:00,MachineB,Electrical,30,電路板故障
2024-03-20 13:00,MachineC,Software,20,軟體更新失敗
2024-03-20 14:00,MachineA,Network issue,40,網路延遲
2024-03-20 15:00,MachineB,Sensor error,35,溫度感測器異常
2024-03-20 16:00,MachineC,Overheat,50,散熱系統故障
```

這個檔案可以用於測試應用程式的功能。

## 🔗 Git 儲存庫

這個專案的程式碼將被上傳到以下 GitHub 儲存庫：

`git@github.com:allens118/chatbotFactory.git` 

## 工廠智能助手

這是一個基於 AI 的工廠智能助手，可以分析機器故障數據並提供智能建議。

## 功能特點

- 分析機器故障數據
- 預估停機時間
- 提供故障原因分析
- 智能問答功能
- 自動化報告生成

## 安裝步驟

1. 克隆專案：
```bash
git clone https://github.com/yourusername/chatBotFactory.git
cd chatBotFactory
```

2. 建立並啟動虛擬環境：
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. 安裝依賴套件：
```bash
pip install -r requirements.txt
```

4. 設定 API Key：
   - 在專案根目錄建立 `api_key.txt` 檔案
   - 將您的 OpenAI API Key 放入檔案中
   - 或設定環境變數：
     ```bash
     # Windows PowerShell
     $env:OPENAI_API_KEY="your-api-key"
     
     # Linux/Mac
     export OPENAI_API_KEY="your-api-key"
     ```

## 使用方式

1. 啟動應用程式：
```bash
streamlit run app.py
```

2. 在瀏覽器中開啟 http://localhost:8501

3. 上傳 CSV 檔案（格式如下）：
```csv
Time,Machine,ErrorType,RepairTime,Description
2024-03-20 08:00,MachineA,Overheat,35,機器過熱，需要冷卻
```

4. 輸入問題，例如：
   - "哪台機器故障次數最多？"
   - "平均修復時間是多少？"
   - "最常見的故障類型是什麼？"

## 注意事項

- 請確保您的 API Key 安全，不要上傳到版本控制系統
- CSV 檔案必須包含必要的欄位：Time, Machine, ErrorType, RepairTime, Description
- 時間格式應為：YYYY-MM-DD HH:MM

## 開發者資訊

- Python 3.9+
- Streamlit 1.32.0
- LangChain 0.0.350
- OpenAI API

## 授權

MIT License 