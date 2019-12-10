import re
#import io
import sys
import time
#import asyncio
import requests
import sqlite3
from bs4 import BeautifulSoup as BS
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from selenium.webdriver import Chrome
from settings import anticaptcha_key, login, fetching_url, profile_path, auth_url


proxies = {

}

def authenticate(driver):
    #autentifocation
    window_handle = driver.window_handles[0]
    time.sleep(1)
    allow_cookies_btn = driver.find_element_by_css_selector('.cc-btn.cc-allow')
    if allow_cookies_btn:
        allow_cookies_btn.click()
    time.sleep(1)
    auth_form =  driver.find_element_by_id('new_allbestbets_user')
    sign_in_url = auth_form.get_attribute('action')
    print(sign_in_url)
    """print(hiddens)
    csrf_token = soup.find('meta', {'name': 'csrf-token'})
    if csrf_token:
        csrf_token = csrf_token.get('content')
        print(csrf_token)"""
    div_recaptcha = auth_form.find_element_by_css_selector('div.g-recaptcha')
    print(div_recaptcha)
    site_key = div_recaptcha.get_attribute('data-sitekey')
    print(site_key)
    recaptcha_url = div_recaptcha.find_element_by_xpath('preceding-sibling::script').get_attribute('src')
    print(recaptcha_url)
    time.sleep(1)
    submit_btn = auth_form.find_element_by_css_selector('button.button-clear')
    auth_form.find_element_by_id('allbestbets_user_email').send_keys(login['user'])
    time.sleep(1)
    auth_form.find_element_by_id('allbestbets_user_password').send_keys(login['pass'])
    time.sleep(1)
    solution = ''
    while not solution:
        try:
            client = AnticaptchaClient(anticaptcha_key)
            task = NoCaptchaTaskProxylessTask(recaptcha_url, site_key)
            job = client.createTask(task)
            job.join()
            solution = job.get_solution_response()
            print(solution)
        except Exception as exc:
            print(exc)    
            time.sleep(1)
    

    driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{solution}';")
    #recaptcha_textarea = auth_form.find_element_by_id('g-recaptcha-response')
    #recaptcha_textarea.send_keys(solution)

    recaptcha_frame = div_recaptcha.find_element_by_tag_name('iframe')
    driver.switch_to.frame(recaptcha_frame) 
    driver.execute_script("document.getElementById('recaptcha-anchor').classList.remove('recaptcha-checkbox-unchecked');document.getElementById('recaptcha-anchor').classList.add('recaptcha-checkbox-checked');")

    #recaptcha_checkbox = driver.find_element_by_css_selector('div.recaptcha-checkbox-border')
    #recaptcha_checkbox.click()

    time.sleep(1)
    driver.switch_to.window(window_handle)
    submit_btn.click()
    """else:
        data = {}
        auth = {}
        auth[auth_form.find_element_by_id('allbestbets_user_email').get_attribute('name')] = login['user']
        auth[auth_form.find_element_by_id('allbestbets_user_password').get_attribute('name')] = login['pass']
        hidden_inputs = auth_form.find_elements_by_css_selector('input[type="hidden"]')
        if hidden_inputs:
            hiddens = {}
            for h in hidden_inputs:
                if h.get_attribute('name') != 'allbestbets_user[remember_me]':
                    hiddens[h.get_attributeet('name')] = h.get_attribute('value')    
        data.update(hiddens)
        data.update(auth)
        data.update({'g-recaptcha-response': solution})
        data['allbestbets_user[remember_me]'] = '0'
        print(data)
        additional_cookies = {'pf_vid': '52ba0f37-8c36-41d8-bdd8-f159f96c8d37',
             '_fbp': 'fb.1.1575486627016.1308162168', 
             '_ga': 'GA1.2.1335301825.1575486626', 
             '_gid': 'GA1.2.2100382945.1575486627', 
             'time_zone_offset': '6', 
             'tooltipViewed': 'true'
        }
        cookies.update(additional_cookies)
        cookies['visitor_type'] = 'free_account'
        print(f'cookies = {cookies}')
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'max-age=0',
            'content-length': '824',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.allbestbets.com',
            'referer': 'https://www.allbestbets.com/users/sign_in',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        r = requests.post(fetching_url + sign_in_url, data = data, cookies = cookies, headers = headers)
        print('---------------------------------')
        print(r.url)"""

def init_db():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute('create table login(login text, pass text,  proxy text)')
    cur.execute('create table vilki(event text, left numeric, right numeric)')
    cur.execute('create table work_parser(date_work text, left numeric, right numeric)')
    cur.close()

def q():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    #cur.execute(f'insert into login(login, pass, proxy) values("{login["login']}", "{login['pass']}", "{login['proxy']}")')
    cur.execute('create table vilki(event text, left numeric, right numeric)')
    cur.execute('create table work_parser(event text, left numeric, right numeric)')
    cur.close()


if __name__ == '__main__':
    #init_db()
    #sys.exit()
    driver = Chrome()
    time.sleep(1)
    driver.get(fetching_url + profile_path)
    time.sleep(1)
    print(dir(driver))
    #print(driver.current_url)
    m = re.search(auth_url, driver.current_url, flags=re.I)
    if m:
        authenticate(driver)
    input('Press any key to exit')
    driver.close()
