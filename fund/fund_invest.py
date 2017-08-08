
import sqlite3
from myconst import DBPATH
from datetime import datetime, date
from myutils import str2date, incday, date2str
from myutils import xirr

DBGTAG = 'policy'

def dbg(msg, tag=''):
    if tag == DBGTAG:
        print(msg)
def log(msg):
    print(msg)

def getvalues(fundid):
    conn = sqlite3.connect(DBPATH)
    cursor = conn.execute('select * from funds where fundid = "%s"' % fundid)
    rows = cursor.fetchall()
    fundvalues = {}
    for row in rows:
        fundvalues[str2date(row[1])] = float(row[2])
        
    return fundvalues
    
def getValueOfdays(fundvalues, beginDateStr, endDateStr, day):
    beginDate = str2date(beginDateStr)
    endDate = str2date(endDateStr)
    currDate = beginDate
    ret = {}
    
    while (currDate < endDate and currDate < datetime.now()):
        if (currDate.strftime("%a") == day or currDate.day == day or day == 0):
            if (not currDate in fundvalues.keys()):
                dbg(date2str(currDate))
                currDate = incday(currDate)
                while(not currDate in fundvalues.keys()):
                    dbg(date2str(currDate))
                    currDate = incday(currDate)
            ret[currDate] = fundvalues[currDate]
        
        currDate = incday(currDate)
            
    return ret

    
def getReturnOfInvest(fundid, rate, beginDateStr, endDateStr, day, investEveryTime=1):
    fv = getvalues(fundid)
    days = getValueOfdays(fv, beginDateStr, endDateStr, day)
    ret = {}
    allinvest = 0
    allshare = 0
    
    alldays = list(days.keys())
    for day in alldays[:-1]:
        allinvest += investEveryTime
        share = investEveryTime * (1-rate) / days[day]
        allshare += share
        allreturn = allshare * days[day]
        ret[day] = [investEveryTime, allinvest, share, allshare, allreturn, fv[day]]
    ret[alldays[-1]] = [0, allinvest, 0, allshare, allshare*days[alldays[-1]], fv[alldays[-1]]]
    
    return ret
    
def addPolicy(fv, detailInfo, more, rate, threshold=-0.01):
    days = list(detailInfo.keys())
    added = {}
    
    for i in range(1, len(days) - 2):
        #latestinfo = detailInfo[days[i]]
        #preinfo = detailInfo[days[i-1]]
        if (fv[days[i]] - fv[days[i-1]])/fv[days[i-1]] < threshold:#1%
            #nextinfo = detailInfo[days[i+2]]
            moreshare = more * (1-rate)/fv[days[i+2]]
            added[days[i+2]] = [more, moreshare]
            #detailInfo[days[i + 2]] = [nextinfo[0]+more, nextinfo[1]+more, nextinfo[2]+moreshare, nextinfo[3]+moreshare, detailInfo[days[i + 2]][-1]]
            #detailInfo[days[-1]] = [0, detailInfo[days[-1]][1]+more, detailInfo[days[-1]][2]+moreshare, detailInfo[days[-1]][3]+moreshare, (detailInfo[days[-1]][3]+moreshare)*]
            
            log('Today: [%s], Mkt: %f; Preday: [%s], Mkt: %f. [%s] Add: %f, Share: %f' \
                % (date2str(days[i]), fv[days[i]], date2str(days[i-1]), fv[days[i-1]], \
                date2str(days[i+2]), more, moreshare))
        elif (fv[days[i]] - fv[days[i-1]])/fv[days[i-1]] > -threshold:
            moreshare = more * (1-rate)/fv[days[i+2]]
            added[days[i+2]] = [-more, -moreshare]
                
    return added

def getSummary(detailInfo, fv, added={}):
    days = list(detailInfo.keys())
    values = []
    totaladdedShare = 0
    totaladdMoney = 0
    for day in days[:-1]:
        if day in added.keys():
            values.append(-detailInfo[day][0]-added[day][0])
            totaladdedShare += added[day][1]
            totaladdMoney += added[day][0]
        else:
            values.append(-detailInfo[day][0])
            
    values.append(detailInfo[days[-1]][-2] + fv[days[-1]]*totaladdedShare)
    xirrvalue = xirr(values, days) * 100
    
    return detailInfo[days[-1]][1]+totaladdMoney, round(values[-1], 4), round(xirrvalue, 2)
    
fv = getvalues('160716')
#days = getValueOfDays(fv, '2016-8-19', '2017-2-24', 'Tue')
'''
for i in range(1, 28):
    days = getReturnOfInvest('160716', 0.0012, '2015-7-12', '2017-7-12', i)
    print(i, getSummary(days))
'''
fixday = 0#'Tue'

days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2017-7-12', fixday)    
print(getSummary(days, fv))
print('---')
added = addPolicy(fv, days, 1, 0.0012)
print(getSummary(days, fv, added))
print('---')
'''
days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2013-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2014-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2015-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2016-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2012-7-12', '2017-7-12', fixday)    
print(getSummary(days))

days = getReturnOfInvest('160716', 0.0012, '2013-7-12', '2014-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2013-7-12', '2015-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2013-7-12', '2016-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2013-7-12', '2017-7-12', fixday)    
print(getSummary(days))

days = getReturnOfInvest('160716', 0.0012, '2014-7-12', '2015-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2014-7-12', '2016-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2014-7-12', '2017-7-12', fixday)    
print(getSummary(days))

days = getReturnOfInvest('160716', 0.0012, '2015-7-12', '2016-7-12', fixday)    
print(getSummary(days))
days = getReturnOfInvest('160716', 0.0012, '2015-7-12', '2017-7-12', fixday)    
print(getSummary(days))

days = getReturnOfInvest('160716', 0.0012, '2016-7-12', '2017-7-12', fixday)    
print(getSummary(days))
'''
'''
for day in days.keys():
    print(day.strftime("%a %Y-%m-%d"), days[day])
'''

'''

def getEveryBuyDateOfWeekly(beginDateStr, endDateStr, weekday):
    beginDate = str2date(beginDateStr)
    endDate = str2date(endDateStr)
    currDate = beginDate
    ret = []
    while (currDate < endDate):
        if (currDate.strftime("%a") == weekday):
            ret.append(currDate)
            
        currDate = incday(currDate)
        
    return ret
'''    
    
'''
def genFixedIncome(investEachTime, timesPerYear, incomePerYear):#compound per year
    sumInvest = 0
    sumInvestNewYear = 0
    sumIncome = 0
    incomeEachTime = 1.0 * incomePerYear / timesPerYear
    
    i = 0
    j = 0
    while i < len(investEachTime):
        sumInvest += investEachTime[i]
        if j < timesPerYear:
            j += 1
        else:
            j = 1
        print(sumInvest, j)
        i += 1
'''
'''
import sys
print(sys.argv[1])
print(len(sys.argv) != 2)
'''