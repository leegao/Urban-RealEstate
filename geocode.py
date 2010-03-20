import os,urllib
from decorators import memoize

USE_GEOCODER_DOT_US = False

@memoize
def latlonggoogle(addr):
    xml = urllib.urlopen('http://maps.google.com/?q=' + urllib.quote(addr) + '&output=js').read()
    if '<error>' in xml:
        return False
    else:
        lat,lng = 0.0,0.0
        center = xml[xml.find('{center')+10:xml.find('}',xml.find('{center'))]
        center = center.replace('at:','').replace('lat:','').replace('lng:','') #Alternates between
        #print center
        try:
            lat,lng = center.split(',')
        except:
            return
        return (float(lat),float(lng))
    
@memoize
def latlongus(addr):
    reader = urllib.urlopen('http://rpc.geocoder.us/service/csv?address='+urllib.quote(addr)).read()
    if "sorry" in reader: return False
    else: return tuple([float(n) for n in reader.split(",")[0:2]])

latlong = latlonggoogle
if USE_GEOCODER_DOT_US: latlong = latlongus
#print latlongus("Yellowstone Blvd and Scott St, Houston TX")
    
#print latlong("W Holcombe Blvd and Kirby Dr, Houston TX")
