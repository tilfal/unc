HTMLFILENAME = 'urls.htm'
ROOTURL = '/url'
#http://localhost:5000/url?op=doadd&s=name` a ``url` b ``tags` c ``usr` d ``pwd` e ``memo` f

from datetime import datetime

def dbg(msg):
    print(msg)

def gethtmlframe():
    return """<html><head>
    <title>URL</title>
    </head><body><center>%s</center></body>
    </html>
    """
    
def urltableheader():
    return '<tr><th>ID</th><th>name</th><th>url</th><th>tags</th><th>usr</th><th>pwd</th><th>memo</th><th>visit</th><th>last</th><th>op</th></tr>\n'
    
class MyURL:
    def __init__(self, url, name, tagstr, username, pwd, memo, id, visit=0, lastvisit=''):
        self.url = url.strip()
        self.name = name.strip()
        
        self.settag(tagstr)
                
        self.username = username.strip()
        self.pwd = pwd.strip()
        self.memo = memo.strip()
        
        self.id = id
        self.visit = visit
        self.lastvisit = lastvisit
        
    def settag(self, tagstr):
        self.tags = []
        for x in tagstr.split(','):
            x = x.strip()
            if not x == '':
                self.tags.append(x)
        
    def doVisit(self):
        self.visit += 1
        self.lastvisit = datetime.now().strftime('%y-%m-%d')
    
    def tohtml(self):
        trhtm = '<tr>'
        trhtm += '<td><a href="?op=mod&id=%d">%d</a></td>' % (self.id, self.id)
        
        trhtm += '<td><a href="?op=go&id=%d" onclick="javascript:window.open(\'%s\',\'_blank\');">%s</a></td>' % (self.id, self.url, self.name)
        trhtm += '<td>%s</td>' % (self.url)
        
        gotagurls = []
        for t in self.tags:
            gotagurls.append('<a href="?op=tag&tag=%s">%s</a>' % (t, t))
        trhtm += '<td>%s</td>' % ','.join(gotagurls)
        
        trhtm += '<td>%s</td>' % self.username
        trhtm += '<td>%s</td>' % self.pwd
        trhtm += '<td>%s</td>' % self.memo
        
        trhtm += '<td>%d</td>' % self.visit
        trhtm += '<td>%s</td>' % self.lastvisit
        trhtm += '<td><a href="?op=rmv&id=%d">R</a></td>' % self.id
        
        trhtm += '</tr>\n'
        return trhtm
        
import re
dr = re.compile(r'<[^>]+>',re.S)
import json

class URLS:
    def __init__(self):
        self.urls = {}
        self.maxid = 0
        
    def addurl(self, url):
        self.urls[url.id] = url
        
        self.maxid = max(self.maxid, url.id)
        
    def refreshtags(self):
        tags = {}
        for u in self.urls.values():
            for t in u.tags:
                if t in tags.keys():
                    tags[t] += 1
                else:
                    tags[t] = 1
        return tags
        
    def rmv(self, id):
        self.urls.pop(id)
                
    def trimHtmlTags(self, str):
        dd = dr.sub('',str)
        return dd
        
    def fromhtml(self, htmlfile):
        htmlhandler = open(htmlfile, 'r')
        htmlcontent = htmlhandler.read()
        htmlhandler.close()
        
        tablebegin = htmlcontent.find('<table')
        tablebegin = htmlcontent.find('<table', tablebegin+1)
        trs = htmlcontent[tablebegin:].split('</tr>')
        for tridx in range(1,len(trs)-1):
            tds = trs[tridx].split('</td><td>')
            
            id = int(self.trimHtmlTags(tds[0]))
            name = self.trimHtmlTags(tds[1])
            url = tds[2]
            tags = self.trimHtmlTags(tds[3])
            usr = tds[4]
            pwd = tds[5]
            memo = tds[6]
            visit = int(tds[7])
            last = tds[8]
            
            self.addurl(MyURL(url, name, tags, usr, pwd, memo, id, visit, last))
                
    def tohtml(self, thisUrls=None):
        html = ''
        
        tagstr = '<table border="1" cellspacing="0" width="80%">\n'
        tagstr += '<tr>'
        tagstr += '<td><a href="%s">ALL&nbsp;[%d]</a></td>\n' % (ROOTURL, len(self.urls.keys()))
        tags = self.refreshtags()
        for t in sorted(tags.keys()):
            tagstr += '<td><a href="?op=tag&tag=%s">%s&nbsp;[%d]</a></td>\n' % (t, t, tags[t])
        tagstr += '</tr>'
        tagstr += "</table>\n"
        
        if thisUrls == None:
            thisUrls = self.urls
        tablestr = '<table border="1" cellspacing="0" width="80%">\n'
        tablestr += urltableheader()
        us = sorted(thisUrls.values(), key=lambda x:x.visit, reverse=True)
        for u in us:
            tablestr += u.tohtml()
        tablestr += "</table>\n"
        
        return '<h3>TAGS</h3>' + tagstr + '<h3><a href="%s">URLS</a>&nbsp;&nbsp;<a href="?op=add">A</a></h3>' % ROOTURL + tablestr
                
    def printallurls(self):
        content = gethtmlframe() % self.tohtml()
        f = open(HTMLFILENAME, 'w')
        f.write(content)
        f.close()
        return content
    
allurls = URLS()

def visit(id):
    allurls.urls[id].doVisit()
    return allurls.printallurls()
def rmv(id):
    allurls.rmv(id)
    return allurls.printallurls()
def mod(id):
    u = allurls.urls[id]
    str = 'id`%d``name`%s``url`%s``tags`%s``usr`%s``pwd`%s``memo`%s' % (u.id,u.name,u.url,','.join(u.tags),u.username,u.pwd,u.memo)
    return '''
    <form action="%s" method="get"><input type="hidden" name="op" value="domod"/>
    <input type="text" autofocus="autofocus" size="800" name="s" value="%s"/><input type="submit" value="Submit"/>
    </form>
    ''' % (ROOTURL, str.replace('"', '&quot;'))
def domod(s):
    secs = s.split('``')
    dict = {}
    for sec in secs:
        kv = sec.split('`')
        dict[kv[0]] = kv[1]
    
    u = allurls.urls[int(dict['id'])]
    u.name = dict['name']
    u.url = dict['url']
    u.settag(dict['tags'])
    u.username = dict['usr']
    u.pwd = dict['pwd']
    u.memo = dict['memo']
    
    return allurls.printallurls()
    
def add():
    str = 'name`  ``url`  ``tags`  ``usr`  ``pwd`  ``memo`  '
    return '''
    <form action="%s" method="get"><input type="hidden" name="op" value="doadd"/>
    <input type="text" autofocus="autofocus" size="800" name="s" value="%s"/><input type="submit" value="Submit"/>
    </form>
    ''' % (ROOTURL, str)
def doadd(s):
    secs = s.split('``')
    dict = {}
    for sec in secs:
        kv = sec.split('`')
        dict[kv[0]] = kv[1]
    
    u = MyURL(dict['url'], dict['name'], dict['tags'], dict['usr'], dict['pwd'], dict['memo'], allurls.maxid+1)
    allurls.addurl(u)
    
    return allurls.printallurls()
    
def load():
    
    '''allurls.addurl(MyURL('http://www.baidu.com', "baidu", '1,2', 'u1', 'p1', 'm1', 0))
    allurls.addurl(MyURL('http://www.sina.com.cn', "sina", '1,3', 'u1', 'p2', '', 1, 23, '17-8-12'))
    allurls.addurl(MyURL('http://126.com', "126", '', 'u3', 'p3', 'm3', 2, 34))
    allurls.addurl(MyURL('http://jsform.com', "jsform", '4', '', '', '', 3))'''
    allurls.fromhtml(HTMLFILENAME)
    return gethtmlframe() % allurls.tohtml()
def filter(tag):
    if 'ALL' == tag:
        return gethtmlframe() % allurls.tohtml()
        
    filterUrls = {}
    for u in allurls.urls.values():
        if tag in u.tags:
            filterUrls[u.id] = u
    return gethtmlframe() % allurls.tohtml(filterUrls)
    
    
if __name__ == "__main__":
    #test().printallurls()
    allurls = URLS()
    allurls.fromhtml(HTMLFILENAME)
    