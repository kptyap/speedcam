# 3. Cleanse CSV format [ ]
# 4. Insert into SQL db to be called by the app [ ]

import csv
import psycopg2
import sys
from datetime import datetime

def main():
    try:
        conn = psycopg2.connect("dbname=speedcams user=ubuntu host=localhost password=Kypw123!")
    except:
        print('Cannot connect to db')
    
    cur = conn.cursor()
    
    # check if this pdf is new
    cur.execute("SELECT got_date FROM speedcamraw LIMIT 1;")
    existing_date = cur.fetchall()
    print existing_date
    
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