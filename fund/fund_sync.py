import sqlite3
from urllib.request import urlopen
from myconst import DBPATH
import sys

def log(msg):
    print(msg)

class FundDb:
    def __init__(self):
        self.db_path = DBPATH
        self.conn = sqlite3.connect(self.db_path)
        
    def createFundTbl(self):
        self.conn.execute('create table funds (fundid, date, value)')
        
    def close(self):
        self.conn.close()
        
    def insert(self, fundid, data):
        sql = 'insert into funds (fundid, date, value) values (?,?,?)'
        values = []
        
        i = 0
        for k in data.keys():
            cursor = self.conn.execute('select * from funds where fundid="%s" and date="%s"' % (fundid, k))
            if 0 == len(cursor.fetchall()):
                values.append((fundid, k, data[k]))
                i+=1
        
        self.conn.cursor().executemany(sql, values)
        self.conn.commit()
        
        log('insert %d in %d of %s' % (i, len(data), fundid))
        
    def select(self, fundid):
        sql = 'select * from funds where fundid = "%s"' % fundid
        cursor = self.conn.execute(sql)
        ret = {}
        for row in cursor.fetchall():
            ret[row[1]] = row[2]
            
        log('total %d records of %s' % (len(ret), fundid))
        return ret
        
    def info(self, fundid):
        datas = self.select(fundid)
        beginDate = min(datas.keys())
        endDate = max(datas.keys())
        print('from %s to %s' % (beginDate, endDate))
        
class GetFundInfo:
    def __init__(self, fundid):
        self.fundid = fundid
        
    def getFundInfoFromEastmoney(self):
        req = urlopen('http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&page=1&per=3650&code=' + self.fundid)
        pageInfo = req.read().decode('utf-8')
        
        fundInfo = {}
        trs = pageInfo.split('</tr><tr>')
        for trStr in trs:
            tds = trStr.split("</td><td class='tor bold'>")
            dateStr = tds[0]
            begin = dateStr.find('<td>')
            dateStr = dateStr[begin+4:]
            valueStr = tds[1]
            
            fundInfo[dateStr] = valueStr
        
        return fundInfo
        
def sync(fundid, funddb):
    d = GetFundInfo(fundid).getFundInfoFromEastmoney()
    funddb.insert(fundid, d)
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("input fund id")
    else:
        funddb = FundDb()
        
        '''
        sync('003721', funddb)
        sync('164906', funddb)
        sync('002402', funddb)
        
        datas = funddb.select('003721')
        print(datas)
        '''
        sync(sys.argv[1], funddb)
        #funddb.info('160716')
        funddb.close()
    