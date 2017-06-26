from bs4 import BeautifulSoup
import urllib
import tempfile

url = 'https://www.police.wa.gov.au/~/media/Files/Police/Traffic/Cameras/Camera-locations'
print url

with tempfile.NamedTemporaryFile() as temp:
    urllib.urlretrieve(url, temp.name)

    soup = BeautifulSoup(temp.name, 'html.parser')
    
    print(soup.prettify())
