import re
import time
import asyncio
import requests
import aiomysql
import aiohttp
from bs4 import BeautifulSoup as BS
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from .settings import anticaptcha_key, fetching_interval_in_seconds, login, \
fetching_url, profile_path, auth_url, arbs_live, abb_db_host, abb_db_user, \
abb_db_port, abb_db_password, abb_db, abb_request_headers, abb_post_request_data

work_statuses = {
    'working': {'status': 1, 'description': 'the scrapper process is working...'},
    'paused': {'status': 2, 'description': 'the scrapping process was interrupted...'},
    'restarting': {'status': 3, 'description': 'the scrapping process must be restarted...'},
    'stoped': {'status': 4, 'description': 'the scrapping process was stoped...'}
}

async def authenticate():
    await update_status_work('authenticating')    
    session = await aiohttp.ClientSession()
    resp = await session.get(fetching_url + profile_path)
    cookies = dict(session.cookie_jar)
    #print(f'cookies={dict(cookies)}')
    page = await resp.text()
    m = re.search(auth_url, resp.url, flags=re.I)
    if m:
        soup = BS(page, 'html.parser')
        auth_form =  soup.find(id = 'new_allbestbets_user')
        sign_in_url = auth_form.get('action')
        csrf_token = soup.find('meta', {'name': 'csrf-token'})
        if csrf_token:
            csrf_token = csrf_token.get('content')
            print(f'csrf_token={csrf_token}')
        div_recaptcha = auth_form.find('div', {'class': 'g-recaptcha'})
        print(div_recaptcha)
        site_key = div_recaptcha.get('data-sitekey')
        print(site_key)
        recaptcha_url = div_recaptcha.parent.script.get('src')
        print(recaptcha_url)

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

        data = {}
        auth = {}
        auth[auth_form.find(id = 'allbestbets_user_email').get('name')] = login['user']
        auth[auth_form.find(id = 'allbestbets_user_password').get('name')] = login['pass']
        hidden_inputs = auth_form.find_all('input', {'type': 'hidden'})
        if hidden_inputs:
            hiddens = {}
            for h in hidden_inputs:
                if h.get('name') != 'allbestbets_user[remember_me]':
                    hiddens[h.get('name')] = h.get('value')    
        data.update(hiddens)
        data.update(auth)
        data.update({'g-recaptcha-response': solution})
        data['authenticity_token'] = csrf_token
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
        session = aiohttp.ClientSession(cookies = cookies, headers = abb_request_headers)
        resp = await session.post(fetching_url + sign_in_url, data = data)
    return session
    """page = await resp.text()
    print('---------------------------------')
    print(f'url={resp.url}, status={str(resp.status)}')
    print(page)
    resp = await session.get(fetching_url + profile_path)
    print('---------------------------------')
    print(f'url={resp.url}, status={str(resp.status)}')"""

async def update_vilki(arbs):
    """Updating vilki table by new list of bet-information"""
    await update_status_work('started updating vilki table...')
    async with aiomysql.connect(host=abb_db_host, port=abb_db_port, db=abb_db, user=abb_db_user, password=abb_db_password) as conn:
        cur = await conn.cursor()
        await cur.execute('delete from vilki;')
        for arb in arbs:
            await cur.execute("""insert into vilki(percent, min_koef, max_koef, initiator, event_name, team1_name, team2_name, league, sport_id, country_id) values(%s,%s, %s, %s,'%s','%s','%s','%s', %s, %s); commit;""" % (arb['percent'], arb['min_koef'], arb['max_koef'], arb['initiator'], arb['event_name'], arb['team1_name'], arb['team2_name'], arb['league'], arb['sport_id'], arb['country_id']))
        await cur.close()
    await update_status_work('finished updating vilki table...')

async def update_status_work(description, status = None):
    """Updating status of work_parser table"""
    async with aiomysql.connect(host=abb_db_host, port=abb_db_port, db=abb_db, user=abb_db_user, password=abb_db_password) as conn:
        cur = await conn.cursor()
        print(description)
        if status:
            await cur.execute(f"update work_parser set status_work = '{description}', status = {status}; commit;")
        else:
            await cur.execute(f"update work_parser set status_work = '{description}'; commit;")
        await cur.close()


async def check_status():
    """Checking work_parser status and demand of the re-authetication"""
    status = None
    async with aiomysql.connect(host=abb_db_host, port=abb_db_port, db=abb_db, user=abb_db_user, password=abb_db_password) as conn:
        cur = await conn.cursor()
        await cur.execute('select status from work_parser;')
        row = await cur.fetchone()
        if row:
            status = row[0]
        else:
            await cur.execute("insert into work_parser(date_work, status_work, status) values(now(), '%s', %d); commit;"% (work_statuses['working']['description'], work_statuses['working']['status']))
            status = work_statuses['working']['status']
        #check credentials
        await cur.execute('select login, pass, proxy from login;')
        r = await cur.fetchone()
        if r:
            #if login, password or proxy have been changed then we must reauthenticate
            if r[0] != login['user'] or r[1] != login['pass'] or r[2] != login['proxy']:
                login['user']=r[0]
                login['pass']=r[1]
                login['proxy']=r[2]
                #status = 3 - parst must reauthenticate
                await cur.execute('update work_parser set = 3; commit;')
                status = 3
        else:
            await cur.execute("insert into login(login, pass, proxy) values('%s', '%s', '%s'); commit;" % (login['user'], login['pass'], login['proxy']))
        await cur.close()
    return status

async def parse(status):
    """Parsing /arbs/live page"""
    session = None
    try:
        #status = 2 - parser must be paused
        if status == 2:
            await update_status_work('paused parsing...')
            return
        """
        #status = 3 - parst must reauthenticate
        #temporary unavailable feature
        elif status == 3:
            session = await authenticate()"""
        session = aiohttp.ClientSession(headers = abb_request_headers)
        await update_status_work('started parsing...')
        async with session.post(fetching_url, data = abb_post_request_data) as resp:
            arbs_json  = await resp.json()
            arbs = []
            arbs_items = arbs_json['arbs']
            for item in arbs_items:
                d = {}
                d['percent'] = item['percent']
                d['min_koef'] = item['min_koef']
                d['max_koef'] = item['max_koef']
                d['initiator'] = item['initiator']
                d['event_name'] = item['event_name']
                d['team1_name'] = item['team1_name']
                d['team2_name'] = item['team2_name']
                d['league'] = item['league']
                d['sport_id'] = item['sport_id']
                d['country_id'] = item['country_id']
                arbs.append(d)
            await update_vilki(arbs)
        await update_status_work('finished parsing...')
    except Exception as exc:
        print(exc)
        await update_status_work(f'Error occured: {exc}', 4)
    finally:
        if session:
            await session.close()

async def parse_periodic():
    """Periodic parsing and checking work_parser status"""
    while True:
        status = await check_status()
        #status = 4 - parser must be stoped
        if status == 4:
            break
        await parse(status)
        await asyncio.sleep(fetching_interval_in_seconds)
