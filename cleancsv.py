# 3. Cleanse CSV format [ ]
# 4. Insert into SQL db to be called by the app [ ]

import csv

search_for = ['Street Name', 'Brookton Highway']

with open('KY.csv', 'rb') as fileObj:
    readerObj = csv.reader (fileObj, delimiter=',')
    for row in readerObj:
    #    if row[0] in search_for:
    #        print('Found: {}'.format(row))
            
    #check number of columns?   
        for column in row[0]:
            print column[0]
            
        
        #skip rows starting with 'Street Name,'
        
        
        #format should be Street Name, Suburb
        
        
    
