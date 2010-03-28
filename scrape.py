import urllib, urllib2, re, time, math
from BeautifulSoup import BeautifulSoup
import geocode

class Scrapper:
    def __init__(self, query="Houston, TX"):
        self.base_url = "http://www.fizber.com/home-by-owner/houses-search-result%s.html"
        self.sold_url = "http://www.fizber.com/home-by-owner/houses-search-result%s.html?sell_sold=sold"
        self.values = {
              "csz" : query ,
              "prop_type_ch" : 8 ,
              }
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        referer = "http://www.fizber.com/fsbo-data-base/houston-city-texas-real-estate-fsbo.html"
        self.max = 0
        self.headers = { 'User-Agent' : user_agent , 'Referer':referer }
        self.get(False)
        self.sqft = re.compile("[0-9]+\.0 s")
        self.coords = []
    
    def get(self, n):
        response = ""
        if n != False:
            response = urllib2.urlopen(urllib2.Request(self.sold_url%("-%s"%n), urllib.urlencode({}), self.headers))
        else:
            response = urllib2.urlopen(urllib2.Request(self.base_url%(""), urllib.urlencode(self.values), self.headers))
            self.headers["Cookie"]=response.headers.dict["set-cookie"]
        return response.read()

    def extract(self, html):
        html = html.replace("</scr\";\ns += \"ipt>"," ")
        soup = BeautifulSoup(html)
        self.max = math.ceil(float(soup.html.body.find('div',id='showsearch').contents[2].split()[0])/15)
        trs = soup.html.body.find('div', id="wrap").find("div", id="div_search_res").find("div", id="c_here").find("div", id="div_search_res_list").find("table", id="resultTable").find("tr").findNextSiblings()
        for tr in trs:
            top = tr.td.table.tr.findAll("td")
            
            address = top[0].a.strong.contents[0].strip()
            latlong = geocode.latlong(address)
            if not latlong:
                continue
            price = (top[1].strong.strike.contents[0].strip().replace("$", "").replace(",",""))
            desc = tr.td.findAll("table")[1].tr.findAll("td")[2].span.contents[0].strip().replace("\n","")
            psqft = 0
            try:
                for i in self.sqft.finditer(desc): psqft = float(price)/float(i.group().replace(" s", "")); break
                if psqft:
                    print "\"%s\",%s,%s,%s,%s"%(address,latlong[0],latlong[1], price, psqft)
                    #time.sleep(1)
                    #print int(price)/10000
                    self.coords += [[latlong[0],latlong[1], price,psqft]]
                    #return (address,latlong[0],latlong[1], price, psqft)
            except:
                pass
    def __call__(self, n):
        try:
            return self.extract(self.get(n))
        except:
            time.sleep(5)
            self.get(0)
            try:
                return self.extract(self.get(n))
            except:
                return False
            
import sys, os, math
def batch(zipcode, n=1000, output = True, more= ", TX"):
    scrapper = Scrapper(str(zipcode)+more)
    stdbak = sys.stdout
    _f = stdbak
    if output:
        _f = open("zips/"+str(zipcode).replace(" ", "_")+".csv", "w")
    try:
        for i in range(1, n):
            if scrapper.max: 
                if scrapper.max <= i-1: continue
            sys.stdout = stdbak
            print "\t\tPage "+str(i)
            sys.stdout = _f
            scrapper(i)
            sys.stdout = stdbak
            print "\t\tSleeping for 1 seconds"
            time.sleep(1)
    finally:
        sys.stdout = stdbak
        #_f.close()
    
if __name__ == "__main__":
    batch("Chicago", more=", Il", output = True)
