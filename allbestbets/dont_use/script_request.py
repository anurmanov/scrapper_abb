import requests


data = {'auto_update': 'true',
'notification_sound': 'false',
'notification_popup': 'false',
'show_event_arbs': 'true',
'grouped': 'true',
'per_page': '10',
'sort_by': 'percent',
'event_id': '',
'q': '',
'event_arb_types[]': '1',
'event_arb_types[]': '2',
'event_arb_types[]': '3',
'event_arb_types[]': '4',
'event_arb_types[]': '5',
'event_arb_types[]': '6',
'event_arb_types[]': '7',
'is_live': 'true',
'search_filter[]': '25558'}

r = requests.post('https://api-lv.allbestbets.com/api/v1/arbs/pro_search?access_token=', data = data, headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
"""r = requests.get('https://api-lv.allbestbets.com/api/v1/bet_combinations/324?access_token=', headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'max-age=0',
            'content-length': '0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.allbestbets.com',
            'referer': 'https://www.allbestbets.com/users/sign_in',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
)#, data = data)"""
#r = requests.post('https://api-lv.allbestbets.com/api/v1/refresh_token?access_token=', data = {"iv":"OdfroHgDBdxjkI00","v":1,"iter":10000,"ks":128,"ts":64,"mode":"gcm","adata":"","cipher":"aes","salt":"9ua/3L1EvBI=","ct":"qMwgx7DVJRoPRpVJs3VSJ8r/N786SXhyTy2PLUCbBIsZZQetKcVXaWJl83U7JMTj3nuz27A8Hsm+wZ9edDmq3TI9n4/LYEusFNTyDUhCOqM/bBqrsCO+4EMB7pd9x7RNgZJBkkxhrqyXZF5Iy2rBOFKD"})


arbs = r.json()
print(arbs)
#arbs_items = arbs['arbs']
#for item in arbs_items:
#    print(item)
