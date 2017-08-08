import sqlite3
from urllib.request import urlopen, Request
from myconst import DBPATH

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
url1 = 'http://jingzhi.funds.hexun.com/database/openjjgk.aspx?fundcode=%s'
url2 = 'http://jingzhi.funds.hexun.com/fundsbuy/%s.shtml'

def getPageInfo(url):
    req = Request(url=url,headers=headers)
    text = urlopen(req).read().decode('gbk')
    table = text[text.find('<table'):text.find('</table>')+8]
    tds = table.split('</td>')
    ret = []
    for td in tds:
        s = td.replace('<br>', '\n')
        s = s[s.rfind('>')+1:]
        ret.append(s)
    return ret

def getSummary(fundid):
    return getPageInfo(url1 % fundid)
            
def getBuyInfo(fundid):
    return getPageInfo(url2 % fundid)
    
def getFundInfo(fundid):
    ret = []
    s = getSummary(fundid)
    ret.append(s[1])#name
    ret.append(s[3])#id
    ret.append(s[5])#index
    ret.append(s[7])#stock
    ret.append(s[9])#first size
    ret.append(s[11])#current size
    ret.append(s[13])#found date
    ret.append(s[15])#manager
    ret.append(s[17])#
    ret.append(s[19])#company
    ret.append(s[25])#aim
    ret.append(s[27])#rule
    b = getBuyInfo(fundid)
    ret.append(b[5])#buy fee
    ret.append(b[7])#sale fee
    ret.append(b[9])#manage fee
    ret.append(b[11])#status
    ret.append(b[13])#current value
    ret.append(b[15])#sum value
    
    return ret
    
    
db_path = DBPATH
conn = sqlite3.connect(db_path)

#conn.execute('create table fund_info (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30)')

for i in range(487022, 1000000):
    fundid = str(i).zfill(6)
    try:
        fundinfo = getFundInfo(fundid)
        conn.execute('insert into fund_info (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % tuple(fundinfo))
        conn.commit()
        print(fundid)
    except:
        print('ERR '+fundid)
    
conn.close()

#print(getFundInfo('003721'))
    