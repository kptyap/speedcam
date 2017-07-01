# Use Python 2.7
# This script to run once per week the day that the PDFs are updated
# 1. Download latest PDF on the WA Police website [x]
# 2. Convert PDF into CSV [x]

import tabula
import urllib
import os
from datetime import datetime
import csv
import psycopg2
import sys
import urlparse
import tempfile
import re
from bs4 import BeautifulSoup

def main():
    #### Scrape and download latest PDF from website ####
   
    baseurl = "https://www.police.wa.gov.au"
    url = 'https://www.police.wa.gov.au/Traffic/Cameras/Camera-locations'

    # retrieve the html of the page
    urllib.urlretrieve(url,'pol.html')
    
    # open the html document in BS4
    with open ('pol.html', 'r') as p:
        soup = BeautifulSoup(p, 'html.parser')
        
        # search using BS4 for the first PDF link
        pdfurl = soup.find(href=re.compile("/~/media/Files"))['href']
        pdfurl = baseurl + str(pdfurl)
        print(pdfurl)
    
    # download latest PDF
    urllib.urlretrieve(pdfurl, 'speedcamDL.pdf')
    
    #check if pdf downloaded by checking file size
    filesize = os.path.getsize(os.path.join(os.path.curdir, 'speedcamDL.pdf'))
    print filesize

    #if pdf was downloaded correctly then convert info to csv
#    if (filesize > 30000):
#        tabula.convert_into(os.path.join(os.path.curdir, 'speedcamDL.pdf'),
#                                "speedcam.csv",
#                                pages="all",
#                                output_format="csv")
#    else:
#        print ('404 error')
#        sys.exit
    
    #### Add CSV output to temp PSQL db, cleanse, then add to permanent db ####
                                                                         
    #DATABASE_URL = "postgres://xguiubukgruviq:448ab5a6ed85b3b88afa07f95f7a04ff50720b937b710e08a0b033651eb5e6e0@ec2-23-23-234-118.compute-1.amazonaws.com:5432/d7dl5h42bu8d38"
    
    #urlparse.uses_netloc.append("postgres")
    #dburl = urlparse.urlparse(os.environ[DATABASE_URL])
    
    try:
        conn = psycopg2.connect("dbname=speedcams user=ubuntu host=localhost password=Kypw123!")
        #conn = psycopg2.connect(
        #    database=dburl.path[1:],
        #    user=dburl.username,
        #    password=dburl.password,
        #    host=dburl.hostname,
        #    port=dburl.port
        #)
        
    except:
        print('Cannot connect to db')
        sys.exit
    
    cur = conn.cursor()
    
    # obtain date of the most recent pdf inserted into the database
    cur.execute("SELECT got_date FROM speedcamraw LIMIT 1;")
    existing_date = cur.fetchall()
    print existing_date
    
    # obtain date of the pdf just downloaded
    csvfile = os.path.join(os.path.curdir, 'speedcam.csv')
    with open (csvfile, 'rb') as csvfile:
        rows = list(csv.reader(csvfile, delimiter=','))
        new_date = (rows[0][0]).split(' ')
        new_date = new_date[3] +' '+ new_date[2] + ' '+ new_date[1]
        new_date = datetime.strptime(new_date, '%Y %B %d').date()
        print new_date
    
    if (new_date == existing_date):
        sys.exit()
        print 'PDF has already been loaded'
    else:
        # copy pdf csv output into a clean instance of speedcamraw table
        cur.execute("TRUNCATE TABLE speedcamraw;"
                    "ALTER TABLE speedcamraw DROP COLUMN id;"
                    "COPY speedcamraw (street_name, suburb, street_name2, suburb2)"
                    "FROM '/home/ubuntu/workspace/speedcam/speedcam.csv' DELIMITER ',' CSV;"
                    # create an autoincrementing primary key (id) - http://stackoverflow.com/questions/2944499/how-to-add-an-auto-incrementing-primary-key-to-an-existing-table-in-postgresql
                    "ALTER TABLE speedcamraw ADD id SERIAL PRIMARY KEY;")
        
        
        # check if suburb and street_name2 are empty, if so pull the PDF text date
        cur.execute('''SELECT street_name, id FROM speedcamraw 
                    WHERE ((suburb IS NULL)
                    AND (street_name2 IS NULL));''')
        datesfrompdf = cur.fetchall()
        
        for rowdate, rowid in datesfrompdf:
            # delete all 'street name' header rows (ie. date header rows + 1)
            cur.execute("DELETE FROM speedcamraw WHERE id = %s;", (rowid + 1,))
                        
        # Fill down dates based on date headers
        for rowdate, rowid in datesfrompdf:
            cur.execute('''UPDATE speedcamraw SET got_date = %s
                        WHERE ((suburb IS NOT NULL) AND (street_name IS NOT NULL)
                        AND (id > %s));''', (rowdate, rowid))
        
        # Delete date header rows
        cur.execute('''DELETE FROM speedcamraw WHERE
                    ((suburb IS NULL) AND (street_name2 IS NULL)
                    AND (suburb2 IS NULL) AND (got_date IS NULL));''')
        
        
        # Copy date, streetname2 and suburb2
        cur.execute('''INSERT INTO speedcamraw (got_date, suburb, street_name)
                     SELECT got_date, suburb2, street_name2 FROM speedcamraw;''')
        
        # Clean up any blank rows
        cur.execute('''DELETE FROM speedcamraw WHERE
                    ((suburb IS NULL) AND (street_name IS NULL));''')
        
                    
        # Copy date, street_name and suburb into speedcamclean
        cur.execute('''INSERT INTO speedcamclean (date, suburb, street_name)
                    SELECT got_date, street_name, suburb FROM speedcamraw;''')
    
    conn.commit()
    
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    main()