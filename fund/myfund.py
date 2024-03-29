from urllib.request import urlopen
from myconst import HTMLTABLE

class Fund:
    def __init__(self, fundNo, buyPrice=0, newBasePrice = 0, buyCount=0, isRMB="", buyDate='', buyTotal=0):
        self.fundNo = fundNo
        self.buyPrice = buyPrice
        self.newBasePrice = newBasePrice
        self.buyCount = buyCount
        self.isRMB = isRMB
        self.buyDate = buyDate
        self.name = ''
        self.buyTotal = buyTotal
        
    def getNewPrice(self):
        '''
        req = urlopen('http://stocks.sina.cn/fund/his?vt=4&code='+self.fundNo)
        pageInfo = req.read().decode('utf-8')
        bodyInfo = pageInfo.split('<body>')[1]
        currLine = bodyInfo.split('<br')[2]
        currLine = currLine.replace('/>','').replace('\\r','').replace('\\n','').replace(' ', '')
        value = list(map(lambda x:x.strip(), currLine.split('&nbsp;')))[:2]    
        nameLineStart = bodyInfo.find(self.fundNo)+8
        nameLine = bodyInfo[nameLineStart:nameLineStart+6]
        
        self.name = nameLine
        self.nowDate = value[0][2:]
        self.nowPrice = value[1]
        '''
        
        #var hq_str_f_002402="NFMY(QDII)AXH,0.1651,0.1651,0.1651,2017-07-28,27.2441";
        req = urlopen('http://hq.sinajs.cn/list=f_'+self.fundNo)
        pageInfo = req.read().decode('gbk')
        bodyInfo = pageInfo[21:-3]#NFMY(QDII)AXH,0.1651,0.1651,0.1651,2017-07-28,27.2441
        value = bodyInfo.split(',')
        
        self.name = value[0]
        self.name6 = self.name[:6]
        self.nowDate = value[4][2:]
        self.nowPrice = value[1]
        
    def newPrice2Tr(self):
        newPriceFloat = float(self.nowPrice)
        ret = '<tr>\n'
        ret += '<td><a target="_blank" href="http://fund.eastmoney.com/' + self.fundNo + '.html">' + self.name6 + '</a></td>\n'
        ret += '<td>' + '%.2f' % ((newPriceFloat-self.buyPrice)/self.buyPrice*100) +'%' + '</td>\n'
        if self.newBasePrice == 0:
            ret += '<td></td>\n'
        else:
            ret += '<td>' + '%.2f' % ((newPriceFloat-self.buyPrice*self.newBasePrice)/(self.buyPrice*self.newBasePrice)*100) +'%' + '</td>\n'
        ret += '<td>' + self.nowDate[3:] + '</td>\n'
        ret += '<td>' + self.isRMB + '%.2f' % ((newPriceFloat-self.buyPrice)*self.buyCount) + '</td>\n'
        ret += '<td>' + str(self.nowPrice) + '</td>\n'
        ret += '<td>%.4f</td>\n' % self.buyPrice
        ret += '<td>%.1f</td>\n' % (1.0*self.buyTotal/10000)
        ret += '<td>' + self.buyDate[3:] + '</td>\n'
        ret += '</tr>\n'
        return ret
        
from datetime import datetime
        
class DoneFund:
    def __init__(self, info):
        self.id = info[0]
        self.start = info[1]
        self.end = info[2]
        self.total = info[3]
        self.bonus = info[4]
        self.rmb = info[5]
        self.platform = info[6]
        
        self.rate = self.bonus*100.0/self.total
        self.rateofyear = self.rate*365/((datetime.strptime(self.end, '%y-%m-%d')-datetime.strptime(self.start, '%y-%m-%d')).days)
        
    def tr(self):
        ret = '<tr>'
        ret += '<td>%s</td>' % self.id
        ret += '<td>%s</td>' % self.start[3:]
        ret += '<td>%s</td>' % self.end[3:]
        ret += '<td>%d</td>' % self.total
        ret += '<td>%d</td>' % self.bonus
        ret += '<td>%.2f</td>' % self.rate
        ret += '<td>%.2f</td>' % self.rateofyear
        ret += '<td>%s</td>' % self.rmb
        ret += '<td>%s</td>' % self.platform        
        ret += '</tr>\n'
        return ret
        
import json

def getmyfund():
    fundconffile = open('myfund.json', 'r')
    fundconf = fundconffile.read()
    fundconffile.close()
    fundconf = json.loads(fundconf)
    currfundconf = fundconf['0']
    
    donefundconf = fundconf['2']
    donefunds = []
    for adonefundconf in donefundconf:
        donefunds.append(DoneFund(adonefundconf))

    funds = []
    for afundconf in currfundconf:
        funds.append(Fund(afundconf[0], float(afundconf[1])/afundconf[3], afundconf[2], afundconf[3], afundconf[4], afundconf[5], afundconf[1]))
    '''
    funds.append(Fund('002402', 0.162, 0, 30867, '$', '16-10-18'))
    funds.append(Fund('003721', 0.1614, 0, 278731, '$', '17-05-12'))
    funds.append(Fund('164906', 1.2432, 1.1, 329790, '', '17-05-22'))
    '''
    for f in funds:
        f.getNewPrice()
        
    ret = '<html><title>fund</title>%s\n' % HTMLTABLE
    ret += '''<meta name="viewport" content="width=device-width,user-scalable=no,maximum-scale=1"/>
        <style>
        @media screen and (max-width:800px) {*{font-size:15px;}}
        @media (min-width:800px) and (max-width:1024px) {*{font-size:19px;}}
        @media (min-width:1024px) and (max-width:2048px) {*{font-size:23px;}}
        </style>'''
    ret += '<tr><td>name</td><td>%</td><td>%%</td><td>update</td><td>$</td><td>Now$</td><td>Buy$</td><td>total</td><td>start</td></tr>'
    for f in funds:
        ret += f.newPrice2Tr()
    ret += '</table>\n'
    ret += '<hr/>\n'
    
    ret += HTMLTABLE + '\n'
    ret += '<tr><td>id</td><td>start</td><td>end</td><td>total</td><td>return</td><td>%</td><td>%%</td><td>rmb</td><td>platform</td></tr>\n'
    for adonefund in donefunds:
        ret += adonefund.tr()
    ret += '</table>\n'
    
    ret += '<hr/>Fixed investment, 160716, 200/day, jd<br>\n'
    ret += 'ver:170828-1'
    ret += '</html>'
    return ret

if __name__ == '__main__':
    print(getmyfund())
        
'''
def getFund(fundNo):
    req = urlopen('http://stocks.sina.cn/fund/his?vt=4&code='+fundNo)
    pageInfo = req.read().decode('utf-8')
    bodyInfo = pageInfo.split('<body>')[1]
    currLine = bodyInfo.split('<br')[2]
    currLine = currLine.replace('/>','').replace('\\r','').replace('\\n','').replace(' ', '')
    value = list(map(lambda x:x.strip(), currLine.split('&nbsp;')))[:2]
    
    nameLineStart = bodyInfo.find(fundNo)+8
    nameLine = bodyInfo[nameLineStart:nameLineStart+6]
    return nameLine,value
    
def init():
    funds = {'002402': ['0.162', '30867', '$', '16-10-18'],
        '003721': ['0.1614', '278731', '$', '17-05-12'],
        '164906': ['1.2432', '329790', '', '17-05-22']}

    prt = [['name', 'date', '%', '$', 'Now$', 'Buy$', 'count', 'start']]
    for k in funds.keys():
        v = funds[k]
        curr = getFund(k)
        #f1 = str(round((float(curr[1][1])-float(v[0]))/float(v[0])*100, 2))+'%'
        f1 = '%.2f' % ((float(curr[1][1])-float(v[0]))/float(v[0])*100) +'%'
        #f2 = v[2] + str(round((float(curr[1][1])-float(v[0]))*float(v[1]), 2))
        f2 = v[2] + '%.2f' % ((float(curr[1][1])-float(v[0]))*float(v[1]))
        prt.append([curr[0], curr[1][0][2:], f1, f2, curr[1][1], v[0], v[1], v[3]])
        
    return prt
    
def grid2html(grid):
    ret = '<table border="1" cellspacing="0" cellpadding="0">\n'
    for row in grid:
        ret += '<tr>\n'
        for cell in row:
            ret += '<td>' + cell + '</td>\n'
        ret += '</tr>\n'
    ret += '</table>'
    return ret
'''
