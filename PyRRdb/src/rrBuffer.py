'''
Created on Nov 17, 2012
@author: Andrew Neville

This class implements a round robin data buffer with the option of including a time stamp
Currently this class will write all data in reverse chronological order to a file when
the dbRead method is called. 

Every time the buffer is filled the step size for the next index to write increases by 1

If the step size increases to the size of the data buffer 
it resets to a step size of 1 at the current index.  

'''
import time 

class rrBuffer:

    def __init__(self, bufferSize=8, measureTime=False, fName='readBuffer.txt'):
        self.BUFF_SIZE = bufferSize           #size of buffer
        self.SIZE = self.BUFF_SIZE - 1        #index at zero is always empty
        self.BUFF=[None] * self.BUFF_SIZE     #buffer initialization
        self.INCLUDE_TIME = measureTime       #include time-stamp or not in buffer
        self.FILE_NAME = fName                #file name to store buffer after reading
        self.WRITING = False 
        self.READING = False
        self.STEP = 1                         #step size for deciding what the next index will be
        self.INDEX = 1                        #current index in buffer
        self.LAST = 0;                        #Last index filled when step size reaches buffer size
        self.FILLED = False                   #If buffer has not been filled -
                                              #-at least once self.FILLED is false
        
        #index always zero  BUFF[index:0:-step] gets all values
        
    '''
    Display:
        -Displays all parameters for debugging purposes 
        -if dataOnly is True then we only see the data point in 
         the buffer, no time-stamp or read value 
        ~O(n) 
    '''
    def disp(self,dataOnly=True):
        if dataOnly:
            data = ''
            for i in range(1,self.BUFF_SIZE):                
                x = self.BUFF[i]
                if x:
                    data = data +  str(x[1]) + ' '
            print 'Buffer: [ ' + data + ']'
            print 'Index: ' + str(self.INDEX)
            print 'Step: ' + str(self.STEP)
            print '\n'
        else:  
            print 'Buffer: ' + str(self.BUFF)
            print 'Index: ' + str(self.INDEX)
            print 'Step: ' + str(self.STEP)  
            print 'Buffer size: ' + str(self.BUFF_SIZE)
            print 'Include time in measurement: ' + str(self.INCLUDE_TIME)
            print 'Currently reading: ' + str(self.READING)
            print 'Currently writing: ' + str(self.WRITING) 
            print 'LAST index value: ' + str(self.LAST)
            print 'SIZE parameter value: ' + str(self.SIZE) 
            print 'Filled: ' + str(self.FILLED)
            print 'File name: ' + self.FILE_NAME
            print '\n' 
    
    '''
    Write:
        -Takes data and if self.INCLUDE_TIME is true will store data and time-stamp in the buffer
        -Each data point in the buffer also has a 1 stored at index 0:
        -Data point in buffer --> [1, data value, time-stamp] 
        -The 1 is for reading the values in reverse chronological order in dbRead()
        -This method also updates index and step accordingly
        ~O(1) runtime
    '''
    def dbWrite(self,data):
        if not self.READING:
            self.WRITING = True 
            
            # write to database [1,data,time] the 1 is for reading later
            if self.INCLUDE_TIME: 
                self.BUFF[self.INDEX] = [1, data, time.time()] #include the time-stamp 
            else:
                self.BUFF[self.INDEX] = [1, data]              #don't include time-stamp
                
            #update index and step
            if (self.INDEX + self.STEP > self.SIZE):           #if end of the buffer is reached 
                self.FILLED = True
                self.INDEX = self.INDEX + self.STEP - self.SIZE
                self.STEP += 1
                if self.STEP > self.SIZE:
                    self.STEP = 1
                    self.LAST = self.INDEX
                    self.INDEX += 1
            else:
                self.INDEX = self.INDEX + self.STEP
                
        self.WRITING = False  #done writing
    '''
    set read index to False  1->0  ~O(1) runtime
    '''
    def readCorrect(self, ind):
        data = self.BUFF[ind]
        if data: #if not None
            data[0] = 0 #we have read this data point
            self.BUFF[ind] = data
    '''
    reset all read indices to 1  0->1  ~O(n) runtime
    '''
    def readReset(self):
        for i in range(1,self.BUFF_SIZE):
            data = self.BUFF[i]
            if data:
                data[0] = 1
                self.BUFF[i] = data
    '''
    check if an index has been read already  ~O(1) runtime
    '''
    def checkIfRead(self,ind):
        data = self.BUFF[ind]
        if data: #if not None
            return data[0] # returns 0 or 1
    
    '''
    Read:
        -Reads contents of buffer in reverse chronological order
        -Appends ordered data to a file
        ~O(n+) runtime
    '''
    def dbRead(self):
        if not self.WRITING:
            self.READING = True
            
            # create local variables
            step = self.STEP
            ind = self.INDEX

            #open file                    
            fo = open(self.FILE_NAME,'a') # write values to file for now
            i=0
            #update index and step
            while i < self.SIZE:
                #if not filled step must be 1 and index - step <= 0 is end of data
                if (ind - step <= 0 and not self.FILLED):
                    break
                
                # set index and step
                if(ind-step <=0):
                    ind = ind - step + self.SIZE + 1
                    step -= 1
                    if step < 1:
                        ind = self.LAST
                        step = self.SIZE
                elif(step==1 and (ind-step <= self.LAST)):
                        step = self.SIZE
                        ind -= 1
                else:
                    ind = ind - step
                    
                #if this index has not been read already 
                if self.checkIfRead(ind):    
                    #write to file --->for now 
                    data = self.BUFF[ind]
                    if self.INCLUDE_TIME:
                        fo.write(str(data[1:]) + ' ')
                    else:
                        fo.write(str(data[1]) + ' ')
                    #set read to False 1->0
                    self.readCorrect(ind)
                    i += 1 #successfully written new data point
            #close file
            fo.write('\n')
            fo.close() 
        #reset all read indices to 1 for future dbRead's          
        self.readReset() 
        #its ok to write to the buffer now
        self.READING = False 
    
    '''
    Reset:
        -resets all values to initial conditions and clears the buffer
        ~O(1) runtime
    ''' 
    def reset(self, bufferSize=8, measureTime=False, fName='readBuffer.txt'):
        self.BUFF_SIZE = bufferSize           #size of buffer
        self.SIZE = self.BUFF_SIZE - 1        #index at zero is always empty
        self.BUFF=[None] * self.BUFF_SIZE     #buffer initialization
        self.INCLUDE_TIME = measureTime       #include time-stamp or not in buffer
        self.FILE_NAME = fName                #file name to store buffer after reading
        self.WRITING = False 
        self.READING = False
        self.STEP = 1                         #step size for deciding what the next index will be
        self.INDEX = 1                        #current index in buffer
        self.LAST = 0;                        #Last index filled when step size reaches buffer size
        self.FILLED = False                   #If buffer has not been filled -
                                              #-at least once self.FILLED is false
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    