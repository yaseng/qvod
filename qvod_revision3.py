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
Name:revision3  qvod exploit
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

class ThreadGetKey(threading.Thread):
    def run(self):
        try:           
            chr = msvcrt.getch()
            if chr == 'q':
                print "stopped by your action ( q )"
                os._exit(1)
        except:
            os._exit(1)  

# get url data     
def get(url):
    try:
      r = urllib2.urlopen(url, timeout=30)
      return r.read()
    except :
     return 0   

def fetch_qvod_count(data):
    qvod_re = re.compile('<li class="Grid3 Card" data-element="slide">([\s\S]*?)</li>')
    try:
       rq = qvod_re.findall(data)  # match
       msg("fetch data count:%d" % len(rq))
       for qvod in rq :
        qvod_queue.put(qvod_url + find_text(qvod, '<a href="', '">'))
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

         url = find_text(get(qvod_queue.get()), 'class="sizename" href="', '" target')
         msg(url, 1)
         qvodlist.write(url + "\n")
 
parser = argparse.ArgumentParser(usage="qvod_revision3.py  -u username -t [100] -c [1000]", description="revision3  qvod exploit 1.0")
parser.add_argument("-u", "--user", help="revision3.com user")
parser.add_argument("-t", "--thread", help="working thread")
parser.add_argument("-c", "--count", help="data count")
parser.add_argument("-f", "--file", help="log file")
params = parser.parse_args()

 
if __name__ == '__main__':
     yalogo()
     if not params.user is None:
        global qvod_url
        global  qvod_queue
        qvod_queue = Queue.Queue()
        qvod_url = "http://revision3.com/"
        
        count = 1000 if params.count is None else params.count
        file = params.user + ".txt" if params.file is None else params.file
        len = fetch_qvod_count(get("%s/%s/episodePage?limit=%s" % (qvod_url, params.user, count)))
        thread = len if params.thread is None else params.thread
        qvodlist = open(file, 'a')
        msg("Exploit target %s user:%s  trread:%s count:%s" % (qvod_url, params.user, thread, count)) 
        for i in range(int(thread)):
          Qvoder().start() 
        msg("Fetch %s  files  succeed!!!" % count,1)
         
     else :
        parser.print_help()
        msg("Missing param user", 2)
        
     
     
     
     
     
     
     
     
 
