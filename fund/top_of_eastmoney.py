from selenium import webdriver
import pandas as pd
import time
from datetime import datetime

def getPct(str):
    try:
        return float(str[:-1])
    except:
        return 0
        
drv = webdriver.PhantomJS()
drv.get('http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;szzf;pn50;ddesc;qsd20160821;qed20170821;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb')
tbl = drv.find_element_by_id('dbtable')
trs = tbl.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

data = pd.DataFrame(columns=["1",
                     "sn","id","name","date","net","all-net",
                     "%","%7","%30","%90","%180","%360","%720",
                    "%3y","%y","%all","%u",
                    "fee","2"])
                    
for tr in trs:
    tds = tr.find_elements_by_tag_name('td')
    rec = {"1":tds[0].text, "sn":tds[1].text, "id":tds[2].text, "name":tds[3].text, "date":tds[4].text, "net":float(tds[5].text), "all-net":float(tds[6].text),
          "%":getPct(tds[7].text),"%7":getPct(tds[8].text),"%30":getPct(tds[9].text),"%90":getPct(tds[10].text),
           "%180":getPct(tds[11].text),"%360":getPct(tds[12].text),"%720":getPct(tds[13].text),
          "%3y":getPct(tds[14].text),"%y":getPct(tds[15].text),"%all":getPct(tds[16].text),"%u":getPct(tds[17].text),
          "fee":getPct(tds[18].text),"2":tds[19].text,}
    data = data.append(rec,ignore_index=True)
    
data['%sort'] = data.apply(lambda x: (x['%7']*96*3 + x['%30']*24*5 + x['%90']*8*2 + x['%180']*4 + x['%360']*2 + x['%720'])/100, axis=1)
data = data.sort_values(by='%sort', ascending=False)

data.to_csv('top_of_eastmoney/funds'+datetime.strftime(datetime.now(), '%y-%m-%d')+'.csv',encoding='utf_8_sig')

drv.quit()