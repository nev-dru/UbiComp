'''
Created on Nov 6, 2012

@author: andrew
'''
import requests, time, rrdtool,json

url = 'http://localhost:8080/'
urlPost = 'http://localhost:8080/' #defined to change later

ext = ''
name = 'testRRD.rrd'
dataName1 = 'Var1'
VAR1 = 0
startTime = time.time()


def getRequest():
    cookies = dict(cookies_are='working')
    r = requests.get(url,cookies=cookies)
    print r.content

def sendData(data):
    print 'Data sending:'
    r = requests.post(urlPost,json.dumps(data))
    print 'Data sent:\n'
    print r.content
    

def rrdInit():
    print 'RRD Initializing'

    #initialization
    step = 1    # seconds between RRD computing CDP from PDP's
    rrPDP = 1   # how many PDP's per CDP
    CDPs = 8    # how many CDP's get stored per RRA
    DSu = 10000 # heartbeat - max allowable PDP's between samples before CDP is "unknown"

    dsList = ['DS:%s:GAUGE:%d:U:U' % (dataName1, DSu)]

    rraList = ['RRA:AVERAGE:0.5:%d:%d' % (rrPDP, CDPs),
               'RRA:MIN:0.5:%d:%d' % (rrPDP, CDPs),
               'RRA:MAX:0.5:%d:%d' % (rrPDP, CDPs),
               'RRA:LAST:0.5:%d:%d' % (rrPDP, CDPs)]

    rrdtool.create(name, '--start', '%d' %startTime, '--step', '%d' % (step), dsList, rraList)
    print 'RRD Initialized..sleeping\n'
    time.sleep(1)
    
    
    
def getStoreData():
    fi = open('testData.txt','r')
    for line in fi:
        #generate data
        VAR1 = float(line)
        #see what we generated to determine if rrd data is correct
        print dataName1 + ': %f\n' % VAR1
        #update rrd 
        ret = rrdtool.update(name, "%d:%f" %(time.time(),VAR1))
        
        #Error message. Error if time stamp is wrong
        if ret:
            print 'ERROR: ' + rrdtool.error()
        
        #set endtime for fetching data from rrd
        lastTimeStamp = rrdtool.last(name)
        
        #send data from RRDTool to server
        #CURRENTLY SENDS ALL CONTENTS OF RRD - to change replace startTime with 1 second ago...
        sendData(rrdtool.fetch(name, 'LAST', '--start', "%d" % (startTime) , '--end', '%d' % (lastTimeStamp)))
        
        
        #let me know if everything worked
        print 'client sleeping...\n'
        
        #sleep for 1 second
        time.sleep(1)
    
    fi.close()
 
      
def main():
    rrdInit()
    getStoreData()
    
    getRequest()
    
    
if __name__ == "__main__":
    main()
