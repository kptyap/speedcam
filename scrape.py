from bs4 import BeautifulSoup
import requests
import tempfile
import re

def main():
    baseurl = "https://www.police.wa.gov.au"
    url = 'https://www.police.wa.gov.au/Traffic/Cameras/Camera-locations'
    
    # retrieve the html of the page
    pol_html = requests.get(url)
    print (pol_html.status_code)
    
    # open the html document in BS4
    soup = BeautifulSoup(pol_html.content, 'html.parser')
    
    # search using BS4 for the first PDF link
    pdfurl = soup.find(href=re.compile("/~/media/Files"))['href']
    pdfurl = baseurl + str(pdfurl)
    return pdfurl

if __name__ == "__main__":
    main()