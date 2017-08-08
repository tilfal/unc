ps aux|grep 'python flaskapp.py'|awk '{print $2}'|xargs kill -9
