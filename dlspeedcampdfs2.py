# Use Python 2.7
# This script to run once per week the day that the PDFs are updated
# 1. Download latest PDF on the WA Police website
# 2. Convert PDF into CSV
# 3. Cleanse CSV format
# 4. Insert into SQL db to be called by the app

import tabula
import urllib
import urllib2

startdate1 = '24042017'
enddate1 = '30042017'

url = 'https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-locations/MediaLocations-'+startdate1+'-to-'+enddate1+'.pdf'


# download the latest speedcam pdf from WA Police using URLLIB2
# refer to http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/

# optional: specify user-agent
headers = {'User-Agent': 'Mozilla 5.10'}
request = urllib2.Request(url, None, headers)

try:
    response = urllib2.urlopen(url)
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    print e.reason
else:
    file = "speedcamDL.pdf"
    fh = open(file, "w")
    fh.write(response.read())
    fh.close()

    # extract speedcam locations from the pdf into a csv using tabula
    tabula.convert_into("speedcamDL.pdf",
                        "speedcam.csv",
                        pages="all",
                        output_format="csv")




# download the latest speedcam pdf from WA Police using URLLIB
#urllib.urlretrieve(url[, filename[, reporthook[, data]]])
# urllib.urlretrieve(url, 'speedcamDL.pdf')