ps aux|grep 'uwsgi'|awk '{print $2}'|xargs kill -9
#ps aux|grep 'python flaskapp.py'|awk '{print $2}'|xargs kill -9
