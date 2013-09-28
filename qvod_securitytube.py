#===============================================================================
# Id :phpdisk.y
# Author:Yaseng
#===============================================================================
import   sys, urllib2, os, Queue, msvcrt, threading, re, cookielib, argparse
 
 

 
def yalogo():
    print '''
  ___  ___  ____  ____  ____  __      __   _  _ 
 / __)/ _ \(  _ \( ___)(  _ \(  )    /__\ ( \/ )
( (__( (_) ))(_) ))__)  )___/ )(__  /(__)\ \  / 
 \___)\___/(____/(____)(__)  (____)(__)(__)(__) 
Name:securitytube  av exploit [only vimeo.com]
Author:Yaseng [yaseng@uauc.net]
 '''
# show message
def msg(text, type=0):
    if type == 0: 
       str_def = "[*]" 
    elif  type == 1: 
       str_def = "[+]"
    else:
       str_def = "[-]";
    print str_def + text;
    
def find_text(text, start, end):
    regex = '%s(.*?)%s' % (start, end)
    text_re = re.search(regex, text)
    if text_re  is None :
        return -1
    return text_re.group(1)
def find_text2(text, start, end):
    regex = '%s([\s\S]*?)%s' % (start, end)
    text_re = re.search(regex, text)
    if text_re  is None :
        return -1
    return text_re.group(1)

 

# get url data     
def get(url):
    try:
      r = urllib2.urlopen(url, timeout=30)
      return r.read()
    except :
     return 0   

def fetch_qvod_count(data):
    qvod_re = re.compile('<td><a href="(.*)" target="_blank"><img width="130"')
    try:
       rq = qvod_re.findall(data)  # match
       for qvod in rq :
        print qvod
        qvod_queue.put(qvod)
       return len(rq)
    except :
        return -1

class Qvoder(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
        while 1:
         if qvod_queue.empty() == True:
             break
         data=get(qvod_url+qvod_queue.get());
         vimeo_url=find_text(data,'vimeo.com/moogaloop.swf\?clip_id=','&amp;server=')
         if not vimeo_url is None:
              #url=find_text(get("downloadvimeo.com/generate?url=http://vimeo.com/"+vimeo_url),'<cmd quality=\"hd\">','<\/cmd>')
              print  "http://downloadvimeo.com/generate?url=http://vimeo.com/"+vimeo_url
         else:
              msg('not vimei video',2)
 
 
parser = argparse.ArgumentParser(usage="qvod_securitytube.py  -g group -t [100] -c [1000]", description="securitytube  av exploit 1.0")
parser.add_argument("-g", "--groupid", help="securitytube.com group")
parser.add_argument("-t", "--thread", help="working thread")
parser.add_argument("-c", "--count", help="data count")
parser.add_argument("-f", "--file", help="log file")
params = parser.parse_args()

 
if __name__ == '__main__':
     yalogo()
     if not params.groupid is None:
        global qvod_url
        global  qvod_queue
        qvod_queue = Queue.Queue()
        qvod_url = "http://www.securitytube.net/"
        count = 1000 if params.count is None else params.count
        data=get("%s/groups?operation=view&groupId=%s" % (qvod_url, params.groupid))
        title=find_text(data,'<h3><b>','</b></h3>');
        file = title + ".txt" if params.file is None else params.file
        len = fetch_qvod_count(data)
        thread = len if params.thread is None else params.thread
        qvodlist = open(file, 'a')
        msg("Exploit target %s group:%s  title:%s trread:%s count:%s" % (qvod_url, params.groupid,title,thread, len)) 
        msg("fetch data count:%d" % len)
        for i in range(int(thread)):
          Qvoder().start() 
         
     else :
        parser.print_help()
        msg("Missing param groupid", 2)
        
     
     
     
     
     
     
     
     
 