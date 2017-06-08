# Use Python 2.7
# This script to run once per week the day that the PDFs are updated
# 1. Download latest PDF on the WA Police website [x]
# 2. Convert PDF into CSV [x]

import tabula
import urllib
import os
import datetime
import csv
import psycopg2
import sys

def main():
    #### Initialise time and download latest PDF from website ####
    
    # set start date as the closest Monday prior, enddate as friday
    d = datetime.datetime.today().weekday()
    sd1 = datetime.date.today() - datetime.timedelta(days=d)
    ed1 = sd1 + datetime.timedelta(days=6)
    startdate1 = sd1.strftime('%d%m%Y')
    enddate1 = ed1.strftime('%d%m%Y')
    
    # Manually set the date here:
    #startdate1 = '24042017'
    #enddate1 = '30042017'
    
    url = 'https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-locations/MediaLocations-'+startdate1+'-to-'+enddate1+'.pdf'
    print url
    
    #urllib.urlretrieve(url[, filename[, reporthook[, data]]])
    urllib.urlretrieve(url, 'speedcamDL.pdf')
    
    #check if pdf downloaded by checking file size
    filesize = os.path.getsize('speedcamDL.pdf')
    
    #if pdf was downloaded correctly then convert info to csv
    if (filesize > 30000):
        tabula.convert_into("speedcamDL.pdf",
                                "speedcam.csv",
                                pages="all",
                                output_format="csv")
    else:
        print ('404 error')
        sys.exit
    
    #### Take CSV output, add to a temp PSQL db, cleanse, then add to permanent db ####
    
    try:
        conn = psycopg2.connect("dbname=speedcams user=ubuntu host=localhost password=Kypw123!")
    except:
        print('Cannot connect to db')
        sys.exit
    
    cur = conn.cursor()
    
    # check if this pdf is new
    cur.execute("SELECT got_date FROM speedcamraw LIMIT 1;")
    existing_date = cur.fetchall()
    print existing_date
    
    csvfile = '/home/ubuntu/workspace/speedcam/KY.csv'
    with open (csvfile, 'rb') as csvfile:
        rows = list(csv.reader(csvfile, delimiter=','))
        new_date = rows[0][0]
        datetime.datetime.strptime(new_date, '%Y-%m-%d')
    
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
        # http://stackoverflow.com/questions/23766084/best-way-to-check-for-empty-or-null-value
        cur.execute('''SELECT street_name, id FROM speedcamraw 
                    WHERE (((suburb IS NOT NULL) 
                    AND ((street_name2 IS NOT NULL));''')
                    
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