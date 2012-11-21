'''
Created on Nov 17, 2012

@author: andrew
'''
import time
from rrBuffer import *

'''
Main:
'''
def main():
    # new round robin buffer with parameters [bufferSize, measureTime, fName='readBuffer.txt']
    p = rrBuffer(20,True,'readBuffer.txt') #-->includes time
   
    #simulated data
    for n in range(1,202):
        p.dbWrite(n)
        
    p.dbRead() #--> sends data to output file   
    p.disp(False) #-->displays everything
    return

if __name__ == "__main__":
    main()
