'''
Created on Nov 17, 2012

@author: andrew
'''
#import numpy
import time
'''
Initialize Data logger
'''
def init():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE, INCLUDE_TIME
    WRITING = False
    READING = False
    STEP = 1
    INDEX = 0
    BUFF_SIZE = 7
    BUFF=[None] * BUFF_SIZE
    INCLUDE_TIME = False
    return


'''
Write:
'''
def write(time, data):
    global INCLUDE_TIME, WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    if not READING:
        WRITING = True 
        #include the time-stamp or not in the list
        if INCLUDE_TIME: 
            BUFF[INDEX] = [time, data]
        else:
            BUFF[INDEX] = [data]
            
        if (INDEX + STEP >= BUFF_SIZE):
            INDEX = ((INDEX + STEP) % BUFF_SIZE)           
            STEP = ((STEP)%(BUFF_SIZE))+1
        else:
            INDEX += STEP
       
    WRITING = False
    return

'''
Read: 
read contents of BUFF in order
'''
def read():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    if not WRITING:
        READING = True
    
    READING = False
    return

def test(numl):
    numl.append(8)
    print numl


'''
Check if buffer is full:
'''
def buffCheck():
    return


'''
Print Buffer Contents
'''
def printBuff():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    print BUFF
    print 'STEP: ' + str(STEP)
    print 'INDEX: ' + str(INDEX)
    return

#'''
#Main:
#'''
def main():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    init()
    
    for n in range(0,20):
#        print 'n: ' + str(n)
        write(n,n)
        printBuff()    
    return



    
if __name__ == "__main__":
    main()
