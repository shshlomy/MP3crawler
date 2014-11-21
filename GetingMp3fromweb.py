__author__ = 'shepss'
import urllib2
from bs4 import BeautifulSoup


html = "http://www.notesinspanish.com/category/advanced/page/2/"
#<a href="http://media.libsyn.com/media/intnotesinspanish/nis36_comer_fuera2.mp3">Download MP3</a>
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request(html, headers=hdr)
u = urllib2.urlopen(req)
soup = BeautifulSoup(u)
mp3list = soup.find_all("a")
finalmp3list = []
for tag in mp3list:
    if "mp3" in str(tag.contents):
        finalmp3list.append(str(tag.contents))


for mp3file in finalmp3list:
    file_name = mp3file.split('/')[-1]
    file_name = file_name[:-2]
    print ("mp3file:", mp3file[3:-2])
    print ("filename",file_name)
    req1 = urllib2.Request(mp3file[3:-2], headers=hdr)
    u = urllib2.urlopen(req1)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
