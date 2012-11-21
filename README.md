UbiComp
=======
The server project involves python code that 
reads data from a file (testData.txt), 
and stores the data in RRDTool (client.py), 
then takes the data out of RRDTool and sends the data  in json format to a server (server.py) 
then unpacks the json data and 
writes it to a new file (serverData.txt) 

The PyRRdb project implements a circular buffer for data logging 