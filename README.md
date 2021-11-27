**# 德雞續期專用腳本，實現自動續期，需自有VPS、德雞信箱要是GMAIL  
# 僅支援TGBOT通知  
# 5分鐘設定  
# 輕鬆完成德雞續期**  

**前置工作  
請到Telegram找Bot Father申請一個機器人 [Bot Father] https://t.me/BotFather 並複製Bot Token  
[複製Telegram ID] https://t.me/userinfobot**  

## 步驟1  
**[取得Gmail API] https://console.cloud.google.com/**  
### 1-1 登入接收德雞的帳戶  
### 1-2 新建應用程式(建議名稱設定為Gmail比較好找)  
### 1-3 搜尋 Gmail API 並啟用  

## 步驟2  
### 2-1 點擊OAuth 同意畫面  
### 2-2 設定名稱為GMAIL VERIFY  
### 2-3 填寫使用者支援電子郵件、開發人員聯絡資訊(填自己的EMAIL)  
### 2-4 之後一直點繼續直到摘要  
### 2-5 點擊ADD USER  
### 2-6 填入自己的EMAIL  
**因自己要用，所以沒必要發布**  

## 步驟3  
### 3-1 點擊憑證  
### 3-2 建立憑證→OAuth 2.0 用戶端 ID  
### 3-3 名稱:GMAIL  
### 3-4 已授權的重新導向 URI:http://localhost:36666/  
### 3-5 點擊儲存  
### 3-6 下載JSON，並改名為credentials.json  

## 步驟4  
### 4-1 打開VPS  
### 4-2 把credentials.json及本專案的eu.py、gmail_api.py放入vps主目錄  
**一般為/root，若非root用戶主目錄為/home**  
### 4-3 輸入 pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4 requests pysocks  
### 4-4 安裝完成依賴項輸入 python3 gmail_api.py 你的email 並黏貼網址到瀏覽器同意授權  
**範例:若email為 abc@gmail.com 就輸入 python3 gmail_api.py abc@gmail.com**  
### 4-5 授權完成後回到vps 按下Ctrl+C  
### 4-6 修改eu.py的這4個項目項目，修改完儲存  
  
    TG_BOT_TOKEN = '你的TG BOT TOKEN'  
    TG_USER_ID = '你的TG USER ID'  
    USERNAME = os.environ.get("EUSERV_USERNAME", "你的EUSERV USERNAME")    
    PASSWORD = os.environ.get("EUSERV_PASSWORD", "你的EUSERV PASSWORD")   
  
### 4-7 輸入 python3 eu.py  
### 4-8 等待程式完成，TG機器人會通知  
  
## 步驟5  
### 5-1 成功執行程式後 將其排入定時任務  
    輸入 crontab -e  
    輸入 0 1 * * * /usr/bin/python3 /root/eu.py  
**0 1 * * * 定義為每天0點1分執行，可自行修改為對應時間，/root/eu.py請改為eu.py所在路徑**  
依序按下Ctrl+X、Y、Enter  

    輸入 crontab -l  
    
**crontab -l是為了查看是否有成功設定crontab**  
  
**歡迎多多STAR我的項目  
若是執行上有什麼問題  
請透過issue提出**  
