from flask import Flask, request
from myfund import getmyfund
from top_of_eastmoney import getfileslink, save
from urls import load, visit, filter, rmv, ROOTURL, mod, domod, add, doadd
        
app = Flask(__name__)

@app.route('/<filename>')
def downfile(filename):
    return None
    
@app.route('/myfund')
def fund():
    return getmyfund()
    
@app.route('/eastmoney')
def down():
    files = getfileslink()
    refresh = '\n<li></li>\n<li><a href="/geteastmoney" target="_blank">refresh</a></li>'
    return files + refresh
    
@app.route('/geteastmoney')
def getfromeastmoney():
    return save()    
    
########  URLS

@app.route(ROOTURL)
def urlapp():
    allargs = request.args
    if len(allargs) == 0:
        return load()
    elif allargs.get('op') == 'tag':
        return filter(allargs.get('tag'))
        
    elif allargs.get('op') == 'go':
        return visit(int(allargs.get('id')))
    elif allargs.get('op') == 'rmv':
        return rmv(int(allargs.get('id')))
    elif allargs.get('op') == 'mod':
        return mod(int(allargs.get('id')))
    elif allargs.get('op') == 'domod':
        return domod(allargs.get('s'))
    elif allargs.get('op') == 'add':
        return add()
    elif allargs.get('op') == 'doadd':
        return doadd(allargs.get('s'))

########  MAP

@app.route('/map')
def map():
    f = open('map.htm', encoding='gbk')
    htm = f.read()
    f.close()
    return htm
    
@app.route('/map1710')
def map1710():
    f = open('map1710.htm', encoding='gbk')
    htm = f.read()
    f.close()
    return htm

'''
@app.route('/')
def hello_world():
    return "hello tillfall"
    
@app.route('/buy')
def buy():
    f = open('fund_buy.htm', encoding='gbk')
    htm = f.read()
    f.close()
    return htm
    
@app.route('/doBuy', methods=['GET', 'POST'])
def dobuy():
    if request.method == 'POST':
        return request.form['fundid']
    else:
        return request.args['fundid']
        
@app.route('/test')
def test():
    return '<img src="%s"/>' % 'http://api.map.baidu.com/staticimage/v2?ak=601263224020a7291f88e9dcc94c6810&width=400&height=600&zoom=8&center=86.814,47.429&labels=85.74,46.14|86.873,47.707|86.790,48.699|86.709,48.530|87.439,48.574|86.681,47.846&labelStyles=A%E4%B8%96%E7%95%8C%E9%AD%94%E9%AC%BC%E5%9F%8E,1,14,0xffffff,0x000fff,1|B%E5%B8%83%E5%B0%94%E6%B4%A5,1,14,0xffffff,0x000fff,1|C%E5%96%80%E7%BA%B3%E6%96%AF,1,14,0xffffff,0x000fff,1|D%E7%99%BD%E5%93%88%E5%B7%B4%E6%9D%91,1,14,0xffffff,0x000fff,1|E%E7%A6%BE%E6%9C%A8,1,14,0xffffff,0x000fff,1|F%E4%BA%94%E5%BD%A9%E6%BB%A9,1,14,0xffffff,0x000fff,1'
''' 
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')# listen all ip address