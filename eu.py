#! /usr/bin/env python3

import os
import re
import json
import time
import base64

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPDataError

import requests
from bs4 import BeautifulSoup
from base64 import urlsafe_b64decode
from gmail_api import *

dir_name = os.path.dirname(os.path.abspath(__file__)) + os.sep
os.chdir(dir_name)

TG_BOT_TOKEN = '你的TG_BOT_TOKEN'
TG_USER_ID = '你的TG_USER_ID'
TG_API_HOST = 'api.telegram.org'

# 多個帳戶請使用空格隔開
USERNAME = os.environ.get("EUSERV_USERNAME", "你的德雞用戶名")  
PASSWORD = os.environ.get("EUSERV_PASSWORD", "你的德雞密碼") 

TRUECAPTCHA_USERID = os.environ.get("TRUECAPTCHA_USERID", "euextend")
TRUECAPTCHA_APIKEY = os.environ.get("TRUECAPTCHA_APIKEY", "deJhWBaqgd6QDN4BqJGf")

PIN_KEY_WORD = 'EUserv'

# Maximum number of login retry
LOGIN_MAX_RETRY_COUNT = 5


# options: True or False
TRUECAPTCHA_CHECK_USAGE = True


user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/99.0.4844.51 Safari/537.36"
)
desp = ""  # 空值

unixTimeToDate = lambda t: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

def log(info: str):
    print(info)
    global desp
    desp = desp + info + "\n"


def login_retry(*args, **kwargs):
    def wrapper(func):
        def inner(username, password):
            max_retry = kwargs.get("max_retry")
            # default retry 3 times
            if not max_retry:
                max_retry = 3
            number = 0
            while number < max_retry:
                try:
                    number += 1
                    if number > 1:
                        log("[EUserv] Login tried the {}th time".format(number))
                    sess_id, session = func(username, password)
                    if sess_id != "-1":
                        return sess_id, session
                    else:
                        if number == max_retry:
                            return sess_id, session
                except BaseException as e:
                    log(str(e))
            else:
                return None, None
        return inner
    return wrapper


def captcha_solver(captcha_image_url: str, session: requests.session) -> dict:
    """
    TrueCaptcha API doc: https://apitruecaptcha.org/api
    Free to use 100 requests per day.
    """
    response = session.get(captcha_image_url)
    encoded_string = base64.b64encode(response.content).decode()
    url = "https://api.apitruecaptcha.org/one/gettext"

    data = {
        "userid": TRUECAPTCHA_USERID,
        "apikey": TRUECAPTCHA_APIKEY,
        "case": "mixed",
        "mode": "default", #(human | default)
        "data": encoded_string
    }
    r = requests.post(url=url, json=data)
    j = json.loads(r.text)
    return j


def handle_captcha_solved_result(solved: dict) -> str:
    """Since CAPTCHA sometimes appears as a very simple binary arithmetic expression.
    But since recognition sometimes doesn't show the result of the calculation directly,
    that's what this function is for.
    """
    if "result" in solved:
        solved_text = str(solved["result"])
        if "RESULT  IS" in solved_text:
            log("[Captcha Solver] You are using the demo apikey.")
            print("There is no guarantee that demo apikey will work in the future!")
            # because using demo apikey
            text = re.findall(r"RESULT  IS . (.*) .", solved_text)[0]
        else:
            # using your own apikey
            log("[Captcha Solver] You are using your own apikey.")
            text = solved_text
        operators = ["X", "x", "+", "-"]
        if any(x in text for x in operators):
            for operator in operators:
                operator_pos = text.find(operator)
                if operator == "x" or operator == "X":
                    operator = "*"
                if operator_pos != -1:
                    left_part = text[:operator_pos]
                    right_part = text[operator_pos + 1 :]
                    if left_part.isdigit() and right_part.isdigit():
                        return eval(
                            "{left} {operator} {right}".format(
                                left=left_part, operator=operator, right=right_part
                            )
                        )
                    else:
                        # Because these symbols("X", "x", "+", "-") do not appear at the same time,
                        # it just contains an arithmetic symbol.
                        return text
        else:
            return text
    else:
        print(solved)
        raise KeyError("Failed to find parsed results.")


def get_captcha_solver_usage() -> dict:
    url = "https://api.apitruecaptcha.org/one/getusage"

    params = {
        "username": TRUECAPTCHA_USERID,
        "apikey": TRUECAPTCHA_APIKEY,
    }
    r = requests.get(url=url, params=params)
    j = json.loads(r.text)
    return j


@login_retry(max_retry=LOGIN_MAX_RETRY_COUNT)
def login(username: str, password: str) -> (str, requests.session):
    headers = {"user-agent": user_agent, "origin": "https://www.euserv.com"}
    url = "https://support.euserv.com/index.iphp"
    captcha_image_url = "https://support.euserv.com/securimage_show.php"
    session = requests.Session()

    sess = session.get(url, headers=headers)
    sess_id = re.findall("PHPSESSID=(\\w{10,100});", str(sess.headers))[0]
    # visit png
    logo_png_url = "https://support.euserv.com/pic/logo_small.png"
    session.get(logo_png_url, headers=headers)

    login_data = {
        "email": username,
        "password": password,
        "form_selected_language": "en",
        "Submit": "Login",
        "subaction": "login",
        "sess_id": sess_id,
    }
    r = session.post(url, headers=headers, data=login_data)
    r.raise_for_status()

    if (
        r.text.find("Hello") == -1
        and r.text.find("Confirm or change your customer data here") == -1
    ):
        if "To finish the login process please solve the following captcha." in r.text:
            log("[Captcha Solver] 進行驗證碼識別...")
            solved_result = captcha_solver(captcha_image_url, session)
            if not "result" in solved_result:
                print(solved_result)
                raise KeyError("Failed to find parsed results.")
            captcha_code = handle_captcha_solved_result(solved_result)
            log("[Captcha Solver] 識別的驗證碼是: {}".format(captcha_code))

            if TRUECAPTCHA_CHECK_USAGE:
                usage = get_captcha_solver_usage()
                log(
                    "[Captcha Solver] current date {0} api usage count: {1}".format(
                        usage[0]["date"], usage[0]["count"]
                    )
                )

            r = session.post(
                url,
                headers=headers,
                data={
                    "subaction": "login",
                    "sess_id": sess_id,
                    "captcha_code": captcha_code,
                },
            )
            if (
                r.text.find(
                    "To finish the login process please solve the following captcha."
                )
                == -1
            ):
                log("[Captcha Solver] 驗證通過")
                return sess_id, session
            else:
                log("[Captcha Solver] 驗證失敗")
                return "-1", session

        if 'To finish the login process enter the PIN that you receive via email' in r.text:
            request_time = time.time()
            
            c_id_re = re.search('c_id" value="(.*?)"', r.text)
            c_id = c_id_re.group(1) if c_id_re else None
            pin_code = wait_for_email(request_time)

            payload = {
                "pin": pin_code,
                "Submit": "Confirm",
                "subaction": "login",
                "sess_id": sess_id,
                "c_id": c_id,
            }
            r = session.post(url, headers=headers, data=payload)
            if 'Logout</a>' in r.text and 'enter the PIN that you receive via email' not in r.text:
                return sess_id, session
            else:
                return "-1", session
    else:
        return sess_id, session


def get_servers(sess_id: str, session: requests.session) -> {}:
    d = {}
    url = "https://support.euserv.com/index.iphp?sess_id=" + sess_id
    headers = {"user-agent": user_agent, "origin": "https://www.euserv.com"}
    r = session.get(url=url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tr in soup.select(
        "#kc2_order_customer_orders_tab_content_1 .kc2_order_table.kc2_content_table tr"
    ):
        server_id = tr.select(".td-z1-sp1-kc")
        if not len(server_id) == 1:
            continue
        flag = (
            True
            if tr.select(".td-z1-sp2-kc .kc2_order_action_container")[0]
            .get_text()
            .find("Contract extension possible from")
            == -1
            else False
        )
        d[server_id[0].get_text()] = flag
    return d


def get_verification_code(service, email_id, request_time):
    email = service.users().messages().get(userId='me', id=email_id.get('id')).execute()
    internalDate = float(email.get("internalDate")) / 1000

    if internalDate > request_time-8:
        if email.get('payload').get('body').get('size'):
            data = urlsafe_b64decode(email.get('payload').get('body').get('data')).decode()
        else:
            part = email.get('payload').get("parts")[0]
            data = urlsafe_b64decode(part.get('body').get('data')).decode()
        pin_code_re = re.search('PIN:\s+(.+?)\s+', data)
        pin_code = pin_code_re.group(1) if pin_code_re else None
        return pin_code

def wait_for_email(request_time):
    try:
        service = gmail_authenticate(userId=userId)
        # get emails that match the query you specify from the command lines
        while time.time() < request_time + 120: # wait 2 min
            results = search_messages(service, PIN_KEY_WORD)
            print('Email id search result:' , results)
            # for each email matched, read it (output plain/text to console & save HTML and attachments)
            if results:
                pin_code = get_verification_code(service, results[0], request_time)
                if pin_code:
                    log('[Email] pin code:' + pin_code)
                    return pin_code
            time.sleep(5)
        else:
            log('[Email] Did not receive the email in 2 minutes.')
            return False
    except BaseException as e:
        log('[Email] ' + str(e))
        return False

def renew(
    sess_id: str, session: requests.session, password: str, order_id: str
) -> bool:
    url = "https://support.euserv.com/index.iphp"
    headers = {
        "user-agent": user_agent,
        "Host": "support.euserv.com",
        "origin": "https://support.euserv.com",
        "Referer": "https://support.euserv.com/index.iphp",
    }

    r = session.post(url, headers=headers, data={
        "Submit": "Extend contract",
        "sess_id": sess_id,
        "ord_no": order_id,
        "subaction": "choose_order",
        "show_contract_extension": "1",
        "choose_order_subaction": "show_contract_details",
    })

    r = session.post(url, headers=headers, data={
        "sess_id": sess_id,
        "subaction": "kc2_customer_contract_details_get_change_plan_dialog",
        "ord_id": order_id,
        "show_manual_extension_if_available": "1",
    })

    # send pin code
    request_time = time.time()
    log(f'[EUserv] Send pin code to {userId} Time: {unixTimeToDate(request_time)}')
    r = session.post(url, headers=headers, data={
        "sess_id": sess_id,
        "subaction": "show_kc2_security_password_dialog",
        "prefix":	"kc2_customer_contract_details_extend_contract_",
        "type":	"1",
    })
    if 'A PIN has been sent to your email address' in r.text:
        log('[EUserv] A PIN has been sent to your email address')
    else:
        log('[EUserv] Send Email failed !')
        return False
    
    pin_code = wait_for_email(request_time)
    if not pin_code: return False

    r = session.post(url, headers=headers, data={
        "auth": pin_code,
        "sess_id": sess_id,
        "subaction": "kc2_security_password_get_token",
        "prefix": "kc2_customer_contract_details_extend_contract_",
        "type": "1",
        "ident": "kc2_customer_contract_details_extend_contract_" + order_id,
    })
    if not r.json().get("rs") == "success":
        return False
    token = r.json().get('token').get('value')

    r = session.post(url, headers=headers, data={
        "sess_id": sess_id,
        "subaction": "kc2_customer_contract_details_get_extend_contract_confirmation_dialog",
        "token": token,
    })
    r = session.post(url, headers=headers, data={
        "sess_id": sess_id,
        "ord_id": order_id,
        "subaction": "kc2_customer_contract_details_extend_contract_term",
        "token": token,
    })

    time.sleep(5)
    return True


def check(sess_id: str, session: requests.session):
    print("Checking.......")
    d = get_servers(sess_id, session)
    flag = True
    for key, val in d.items():
        if val:
            flag = False
            log("[EUserv] ServerID: %s Renew Failed!" % key)

    if flag:
        log("[EUserv] ALL Work Done! Enjoy~")


def telegram():
    data = (
        ('chat_id', TG_USER_ID),
        ('text', 'EUserv續期日誌\n\n' + desp)
    )
    response = requests.post('https://' + TG_API_HOST + '/bot' + TG_BOT_TOKEN + '/sendMessage', data=data)
    if response.status_code != 200:
        print('Telegram Bot 推送失敗')
    else:
        print('Telegram Bot 推送成功')

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        log("[EUserv] 你沒有新增任何賬戶")
        exit(1)
    user_list = USERNAME.strip().split()
    passwd_list = PASSWORD.strip().split()
    if len(user_list) != len(passwd_list):
        log("[EUserv] The number of usernames and passwords do not match!")
        exit(1)
    for i in range(len(user_list)):
        userId = user_list[i]
        log("*" * 30)
        log("[EUserv] 正在續期第 %d 個帳號 %s" % (i + 1, userId))
        sessid, s = login(user_list[i], passwd_list[i])
        if sessid == "-1":
            log("[EUserv] 第 %d 個帳號登入失敗，請檢查登入訊息" % (i + 1))
            continue
        elif not sessid:
            continue
        SERVERS = get_servers(sessid, s)
        log("[EUserv] 檢測到第 {} 個帳號有 {} 台 VPS，正在嘗試續期".format(i + 1, len(SERVERS)))
        for k, v in SERVERS.items():
            if v:
                if not renew(sessid, s, passwd_list[i], k):
                    log("[EUserv] ServerID: %s 德雞中彈倒地!" % k)
                else:
                    log("[EUserv] ServerID: %s 德雞續期成功!" % k)
            else:
                log("[EUserv] ServerID: %s 不須續期" % k)
        time.sleep(15)
        check(sessid, s)
        time.sleep(5)

    TG_BOT_TOKEN and TG_USER_ID and TG_API_HOST and telegram()
