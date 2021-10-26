#!/bin/bash

red(){
    echo -e "\033[31m\033[01m$1\033[0m"
}
green(){
    echo -e "\033[32m\033[01m$1\033[0m"
}
yellow(){
    echo -e "\033[33m\033[01m$1\033[0m"
}
blue(){
    echo -e "\033[36m\033[01m$1\033[0m"
}

if [[ -f /etc/redhat-release ]]; then
		release="Centos"
	elif cat /etc/issue | grep -q -E -i "debian"; then
		release="Debian"
	elif cat /etc/issue | grep -q -E -i "ubuntu"; then
		release="Ubuntu"
	elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
		release="Centos"
	elif cat /proc/version | grep -q -E -i "debian"; then
		release="Debian"
	elif cat /proc/version | grep -q -E -i "ubuntu"; then
		release="Ubuntu"
	elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
		release="Centos"
    fi

if [ $release = "Centos" ]
	then
            red " 不支持Centos系統，請更換最新Debian系統或Ubuntu系統 "
      exit 1
	   fi



function ins(){
function dj(){
echo -e nameserver 2a01:4f8:221:2d08::213 > /etc/resolv.conf
apt update -y
apt install python3 python3-pip -y
pip3 install requests beautifulsoup4
apt-get install cron 

wget https://raw.githubusercontent.com/SAOJSM/DEU_CHICK_EXTEND_CHT/main/ac.py
chmod +x ac.py

read -p "德雞登錄用戶名:" USERNAME
sed -i "10 s/^/USERNAME = '$USERNAME'\n/" ac.py

read -p "德雞登錄密碼:" PASSWORD
sed -i "11 s/^/PASSWORD = '$PASSWORD'\n/" ac.py

read -p "TG機器人TOKEN:" TG_BOT_TOKEN
sed -i "12 s/^/TG_BOT_TOKEN = '$TG_BOT_TOKEN'\n/" ac.py

read -p "TG用戶ID:" TG_USER_ID
sed -i "13 s/^/TG_USER_ID = '$TG_USER_ID'\n/" ac.py


ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sed -i '/ac.py/d' /var/spool/cron/crontabs/root >/dev/null 2>&1
echo "0 5 * * * /usr/bin/python3 /root/ac.py >/dev/null 2>&1" >> /var/spool/cron/crontabs/root
chmod 777 /var/spool/cron/crontabs/root
crontab /var/spool/cron/crontabs/root
service cron restart

python3 ac.py
}

function vps(){
#rm -f ac.py* deck.sh*
apt update -y
apt install python3 python3-pip -y
pip3 install requests beautifulsoup4
apt-get install cron 

wget https://raw.githubusercontent.com/SAOJSM/DEU_CHICK_EXTEND_CHT/main/ac.py
chmod +x ac.py

read -p "德雞登錄用戶名:" USERNAME
sed -i "10 s/^/USERNAME = '$USERNAME'\n/" ac.py

read -p "德雞登錄密碼:" PASSWORD
sed -i "11 s/^/PASSWORD = '$PASSWORD'\n/" ac.py

read -p "TG機器人TOKEN:" TG_BOT_TOKEN
sed -i "12 s/^/TG_BOT_TOKEN = '$TG_BOT_TOKEN'\n/" ac.py

read -p "TG用戶ID:" TG_USER_ID
sed -i "13 s/^/TG_USER_ID = '$TG_USER_ID'\n/" ac.py


ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime
sed -i '/ac.py/d' /var/spool/cron/crontabs/root >/dev/null 2>&1
echo "0 5 * * * /usr/bin/python3 /root/ac.py >/dev/null 2>&1" >> /var/spool/cron/crontabs/root
chmod 777 /var/spool/cron/crontabs/root
crontab /var/spool/cron/crontabs/root
service cron restart

python3 ac.py
}

function menu(){
    clear
    yellow "================================================================"
    red "   注意，別手滑！！"
    yellow "================================================================="
    blue " 1.(純IPV6)德雞自己給自己續期  "    
    blue " 2.(非純IPV6)其他VPS給德雞續期 "
    red " 0. 返回上層 "
    echo
    read -p "請輸入數字:" menuNumberInput
    case "$menuNumberInput" in   
     1 )
        dj
     ;;
     2 )
        vps
     ;;
     0 )
       start_menu
     ;;
      esac
}
menu 
}

function corn(){
crontab -e
}

function sj(){
rm -f deck.sh*
wget https://raw.githubusercontent.com/SAOJSM/DEU_CHICK_EXTEND_CHT/main/deck.sh && chmod +x deck.sh && ./deck.sh
}

function re(){
rm -f ac.py*
wget https://raw.githubusercontent.com/SAOJSM/DEU_CHICK_EXTEND_CHT/main/ac.py
chmod +x ac.py

read -p "德雞登錄用戶名:" USERNAME
sed -i "10 s/^/USERNAME = '$USERNAME'\n/" ac.py

read -p "德雞登錄密碼:" PASSWORD
sed -i "11 s/^/PASSWORD = '$PASSWORD'\n/" ac.py

read -p "TG機器人TOKEN:" TG_BOT_TOKEN
sed -i "12 s/^/TG_BOT_TOKEN = '$TG_BOT_TOKEN'\n/" ac.py

read -p "TG用戶ID:" TG_USER_ID
sed -i "13 s/^/TG_USER_ID = '$TG_USER_ID'\n/" ac.py


sed -i '/ac.py/d' /var/spool/cron/crontabs/root >/dev/null 2>&1
echo "0 5 * * * /usr/bin/python3 /root/ac.py >/dev/null 2>&1" >> /var/spool/cron/crontabs/root
service cron restart

python3 ac.py

}


function xz(){
rm -f ac.py* sjxq.sh* deck.sh*
sed -i '/ac.py/d' /var/spool/cron/crontabs/root >/dev/null 2>&1
green "卸載完成"
}


function start_menu(){
    clear
    yellow "================================================================"
    echo "環境要求：支持Ubuntu與Debain，目前不兼容WARP"   
    echo "項目地址：https://github.com/SAOJSM/DEU_CHICK_EXTEND_CHT"
    yellow "================================================================="
    blue " 1. 首次安裝選擇哪類VPS續期，安裝腳本依賴 "    
    blue " 2. 自定義定時執行續期 "
    blue " 3. 時間段內（上午3-5點）隨機執行續期 "
    blue " 4. 重置：續期賬號、推送設置、續期時間 "
    blue " 5. 卸載續期腳本 "
    red " 0. 退出腳本 "
    echo
    read -p "請輸入數字:" menuNumberInput
    case "$menuNumberInput" in   
     1 )
        ins
     ;;
     2 )
        corn
     ;;
     3 )
        sj
     ;;
     4 )
        re
     ;; 
     5 )
        xz
     ;; 
     0 )
       exit 1
     ;;
      esac
}

start_menu "first"  
