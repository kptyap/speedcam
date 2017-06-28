from bs4 import BeautifulSoup
import urllib
import tempfile
import re

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

urllib.urlretrieve(pdfurl, 'speedcamDL.pdf')