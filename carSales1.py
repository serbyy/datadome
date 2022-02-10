import random,time,os,sys
import requests, json, re,datetime
from bs4 import BeautifulSoup
import os
from twocaptcha import TwoCaptcha

global path
if os.name == 'nt':
    path=os.path.dirname(sys.argv[0])
if os.name == 'posix':
    path=os.path.dirname(os.path.abspath(__file__))
open(os.path.join(path, "scraped.csv"),'w').write('Title,Imgs,Price,Otometer,Body Type,Trans,Engine\n')

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
text='''

░█████╗░░█████╗░██████╗░░██████╗░█████╗░██╗░░░░░███████╗░██████╗░░░░█████╗░░█████╗░███╗░░░███╗░░░░█████╗░██╗░░░██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░░░░██╔════╝██╔════╝░░░██╔══██╗██╔══██╗████╗░████║░░░██╔══██╗██║░░░██║
██║░░╚═╝███████║██████╔╝╚█████╗░███████║██║░░░░░█████╗░░╚█████╗░░░░██║░░╚═╝██║░░██║██╔████╔██║░░░███████║██║░░░██║
██║░░██╗██╔══██║██╔══██╗░╚═══██╗██╔══██║██║░░░░░██╔══╝░░░╚═══██╗░░░██║░░██╗██║░░██║██║╚██╔╝██║░░░██╔══██║██║░░░██║
╚█████╔╝██║░░██║██║░░██║██████╔╝██║░░██║███████╗███████╗██████╔╝██╗╚█████╔╝╚█████╔╝██║░╚═╝░██║██╗██║░░██║╚██████╔╝
░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═════╝░╚═╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚═╝░╚═════╝░
'''
print(text)
def times():
    today = str(datetime.datetime.today()).split(' ')
    time=today[1].split('.')
    t="["+today[0]+' '+time[0]+']'
    return t

def scrapeData(link,s,nr):
    print(nr,'https://www.carsales.com.au%s'%(link))
    r=s.get('https://www.carsales.com.au%s'%(link))
        # print(r.text)
    soup=BeautifulSoup(r.text, "lxml")
    try:
        title=soup.find('div',class_='details-title').find('h1').text
    except:
        title=''
    try:
        price=soup.find('div',class_='price').text
    except:
        price=''
    try:
        images=soup.find_all('div',class_='thumb-small')
        imgs=""
        for i in images:
            imgs+=i["style"].split(' url(')[1].split('?pxc_method=')[0]+';'
    except:
        imgs=''
    try:
        up_=soup.find_all('div',class_='key-details-item')
        otometer=up_[0].find('div',class_='key-details-item-title').text
        body_type=up_[1].find('div',class_='key-details-item-title').text
        trans=up_[2].find('div',class_='key-details-item-title').text
        engine=up_[3].find('div',class_='key-details-item-title').text
    except:
        up_=otometer=body_type=trans=engine=''
    line='"%s","%s","%s","%s","%s","%s","%s"\n'%(title,imgs,price,otometer,body_type,trans,engine)
    open(os.path.join(path,'scraped.csv'),'a').write(line)
    return 'ok'

cookies2={
    "domain": ".carsales.com.au",
    "max-age": 31536000,
    "hostOnly": False,
    "httpOnly": False,
    "name": "datadome",
    "path": "/",
    "sameSite": "Lax",
    "secure": True,
    "session": False,
    "storeId": "1",
    "value": "XW._B0Wc1JcD8juQ5JKobvAa5p3f.2LwXY-b.4oC2jy3PHb2kAjphk5A~zwxooB0Hujeq0Qk5GhFac11i2JFughm66CCiH4_L71bClwjxCQOXyTJ55LAP__fz6BK-AT",
    "id": 16
}

def getSession():
    headers = {"authority":"www.carsales.com.au","scheme":"https","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-language":"it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7","sec-fetch-dest":"document","sec-fetch-mode":"navigate","sec-fetch-site":"none","sec-fetch-user":"?1","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    url = "https://www.carsales.com.au"
    s = requests.Session()
    r = s.get(url, headers=headers)
    if 'captcha-delivery.com' in r.text:
        print('%s Found DataDome Captcha'%(times()))
        while True:
            headers = {"authority":"www.carsales.com.au","scheme":"https","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-language":"it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7","sec-fetch-dest":"document","sec-fetch-mode":"navigate","sec-fetch-site":"none","sec-fetch-user":"?1","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
            url = "https://www.carsales.com.au"
            datadome_url_ = 'https://www.carsales.com.au'
            s = requests.Session()
            r = s.get(url, headers=headers)
            # print(r.url)
            # print(r.text)
            dd = json.loads(re.search('var dd=([^"]+)</script>', r.text).group(1).replace("'",'"'))
            # print(dd)
            initialCid = dd['cid']
            hsh = dd['hsh']
            t = dd['t']
            host = dd['host']
            s_ = dd['s']
            cid = s.cookies['datadome']
            # print(initialCid)
            # print(hsh)
            # print(t)
            # print(host)
            first_url = 'https://'+host.replace('&#x2d;','-')+'/captcha/?initialCid={}&hash={}&cid={}&t={}'.format(initialCid, hsh, cid,t)
            # print(first_url)
            first_post = s.get(first_url)
            try:
                data = re.search('getRequest([^"]+)ddCaptcha', first_post.text).group(1)
            except:
                pass
            else:
                useragent = "python-requests/2.25.1"
                ip=""
                m_nr = json.loads(requests.get('https://datadome-magic-number-solver.herokuapp.com/datadome?id={}&ua={}'.format(cid, useragent)).text)['id']
                # print(first_post.url)
                initGeetest=first_post.text.split("initGeetest({")[1].split("handlerEmbed);")[0]
                api_server=initGeetest.split("api_server: '")[1].split("',")[0]
                gt=initGeetest.split("gt: '")[1].split("',")[0]
                challenge=initGeetest.split("challenge: '")[1].split("',")[0]
                # print(api_server)
                # print(gt)
                # print(challenge)
                api_key = os.getenv('APIKEY_2CAPTCHA', 'API-KEY')
                solver = TwoCaptcha(api_key)
                print('%s Sending Captcha Challenge to 2CAPTCHA.COM'%(times()))
                while True:
                    try:
                        result = solver.geetest(gt=gt,
                                                apiServer=api_server,
                                                challenge=challenge,
                                                url='https://www.carsales.com.au')
                        break
                    except Exception as e:
                        print(e)
                        print("Trying again...")
                # response=str(result).split('geetest_challenge":"')[1].split('","')[0]
                res1=json.loads(result['code'])["geetest_challenge"]
                res2=json.loads(result['code'])["geetest_validate"]
                res3=json.loads(result['code'])["geetest_seccode"]

                useragent=ip=''
                url_='https://geo.captcha-delivery.com/captcha/check?cid={}&icid={}&ccid=null&geetest-response-challenge={}&geetest-response-validate={}&geetest-response-seccode={}&hash={}&ua={}&referer={}&parent_url={}&x-forwarded-for={}&captchaChallenge={}'.format(cid, initialCid, res1, res2, res3, hsh, useragent, datadome_url_, datadome_url_, ip, m_nr)
                # print(url_)
                second_post = s.get(url_)
                # print(second_post.status_code)
            if second_post.status_code == 200:
                print('%s CAPTCHA SOLVED OK'%(times()))
                break
        cookies={
            "domain": ".carsales.com.au",
            "name": "datadome",
            "path": "/",
            "secure": True,
            "value": second_post.text.split('; Max-Age')[0].split('datadome=')[1],
        }
        s.cookies.set(**cookies)
    return (s)

if __name__=='__main__':
    startTime=float(time.time())
    print('%s Starting App'%(times()))
    s=getSession()
    nr_=nr=1
    print('%s Start Data Scraping'%(times()))
    while True:
        r=s.get("https://www.carsales.com.au/cars/?q=Service.carsales.&offset=%s"%(nr))
        if '<span class="heading">Engine</span>' not in r.text:
            print('[%s] Done! Finished %s cars scraped in %s sec'%(times(),nr_,float(time.time())-startTime))
            break
        else:
            nr+=11
            soupe=BeautifulSoup(r.text, "lxml")
            a_=soupe.find_all('a',class_="btn-primary")
            links=[]
            for a in set(a_):
                try:
                    links.append(a['href'])
                except:
                    pass
            for l in links:
                res=scrapeData(l,s,nr_)
                nr_+=1
