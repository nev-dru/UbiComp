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
    STEP = 1                #step size for deciding what the next index will be
    INDEX = 0               #current index in buffer
    BUFF_SIZE = 7           #size of buffer
    BUFF=[None] * BUFF_SIZE #buffer initialization
    INCLUDE_TIME = False    #include time-stamp or not
    return


'''
Write:
'''
def write(data):
    global INCLUDE_TIME, WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    if not READING:
        WRITING = True 
        
        if INCLUDE_TIME: 
            BUFF[INDEX] = [time.time(), data]    #include the time-stamp 
        else:
            BUFF[INDEX] = [data]                 #don't include time-stamp
            
        if (INDEX + STEP >= BUFF_SIZE):          #if end of the buffer is reached 
            INDEX = ((INDEX + STEP) % BUFF_SIZE) #reset index         
            STEP = ((STEP)%(BUFF_SIZE))+1        #increment step (no larger than buffer size)
        else:
            INDEX += STEP                        #otherwise increase to next index
       
    WRITING = False                              #done writing
    return

'''
Read: 
read contents of BUFF in order -----NOT DONE
'''
def read():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    if not WRITING:
        READING = True
    
    READING = False
    return

'''
Print Buffer Contents -FOR DEBUG USE ONLY
'''
def printBuff():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    print BUFF
    print 'STEP: ' + str(STEP)
    print 'INDEX: ' + str(INDEX)
    return

'''
Main:
'''
def main():
    global WRITING, READING, STEP, BUFF, INDEX, BUFF_SIZE
    init()
    
    for n in range(0,20):
#        print 'n: ' + str(n)
        write(n)
        printBuff()    
    return



    
if __name__ == "__main__":
    main()
