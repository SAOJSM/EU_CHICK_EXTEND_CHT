### 德雞續期專用腳本，實現自動續期，需自有VPS、德雞信箱要是GMAIL  
### 僅支援TGBOT通知  
### 5分鐘設定  
### 輕鬆完成德雞續期  
  
  
# TRUECAPTCHA限額  
### 下面兩項因TRUECAPTCHA每日100次觸發限額，建議修改為自己的
    TRUECAPTCHA_USERID = os.environ.get("TRUECAPTCHA_USERID", "euextend")
    TRUECAPTCHA_APIKEY = os.environ.get("TRUECAPTCHA_APIKEY", "deJhWBaqgd6QDN4BqJGf")
    
# 需要修改項目  
### 下面四項需要修改為自己的
TG_BOT_TOKEN = '你的TG_BOT_TOKEN'
TG_USER_ID = '你的TG_USER_ID'

USERNAME = os.environ.get("EUSERV_USERNAME", "你的德雞用戶名")  
PASSWORD = os.environ.get("EUSERV_PASSWORD", "你的德雞密碼") 
  
  
# 前置工作  
### 請到Telegram找Bot Father申請一個機器人  
### [Bot Father] https://t.me/BotFather 並複製Bot Token  
### [複製Telegram ID] https://t.me/userinfobot

## 步驟1  
### [取得Gmail API] https://console.cloud.google.com/  
### 1-1 登入接收德雞PIN CODE的帳戶  
### 1-2 新建應用程式(建議名稱設定為Gmail比較好找)  
### 1-3 搜尋 Gmail API 並啟用  

## 步驟2  
### 2-1 點擊OAuth 同意畫面  
### 2-2 設定名稱為GMAIL VERIFY  
### 2-3 填寫使用者支援電子郵件、開發人員聯絡資訊(填自己的EMAIL)  
### 2-4 之後一直點繼續直到摘要  
### 2-5 點擊ADD USER  
### 2-6 填入自己的EMAIL  
## 因自己要用，所以沒必要發布  

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
    wget https://raw.githubusercontent.com/SAOJSM/EU_CHICK_EXTEND_CHT/main/gmail_api.py
    wget https://raw.githubusercontent.com/SAOJSM/EU_CHICK_EXTEND_CHT/main/eu.py
### 一般為/root，若非root用戶主目錄為/home   
### 4-3  首次執行請使用windows，第二次執行再使用vps輸入以下指令
    pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4 requests pysocks 
### 備註:Windows同樣要有eu.py、gmail_api.py、credential.json
### 4-4 首次執行安裝完成依賴項輸入以下指令 並黏貼網址到瀏覽器同意授權  
    python3 gmail_api.py 你的email  
### 4-5 授權完成後取得"token_你的email.json"
### 4-6 輸入 python3 eu.py  
### 4-7 等待程式完成，TG機器人會通知  
  
## 步驟5  
### 5-1 成功執行程式後 將"token_你的email.json"複製回vps 並將eu.py排入定時任務  
     crontab -e  
  
     0 1 * * * /usr/bin/python3 /root/eu.py  
**0 1 * * * 定義為每天0點1分執行，可自行修改為對應時間，/root/eu.py請改為eu.py所在路徑**  
  
### 依序按下Ctrl+X、Y、Enter  

    crontab -l  
    
**crontab -l是為了查看是否有成功設定crontab**  
  
### 續期成功
![image](https://github.com/SAOJSM/EU_CHICK_EXTEND_CHT/blob/main/%E7%BA%8C%E6%9C%9F%E6%88%90%E5%8A%9FTG%E9%80%9A%E7%9F%A5.png)
  
### 歡迎多多STAR我的項目  
### 若是執行上有什麼問題  
### 請透過issue提出

### 錯誤解決
當出現下方圖片錯誤，代表gmail token過期了，只要重新執行4-4獲取token並替換舊token即可
![image](https://github.com/SAOJSM/EU_CHICK_EXTEND_CHT/blob/main/%E7%99%BB%E5%85%A5%E5%A4%B1%E6%95%97.jpg)
