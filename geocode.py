import os,urllib
from decorators import memoize
from geopy import geocoders
import json

USE_GEOCODER_DOT_US = False
USE_DECODER = True

@memoize
def googledec(addr):
    g = geocoders.Google("ABQIAAAATUuAajSTnXcJBeibatQJ7xRV80K6JW8xL5PK-F-L5ZJTyEySmRRIhcftBfvb5EsoW0-XNUtQ_GYYrA")
    return g.geocode(addr)[1]

@memoize
def latlonggoogle(addr):
    xml = urllib.urlopen('http://maps.google.com/?q=' + urllib.quote(addr) + '&output=js&key=ABQIAAAATUuAajSTnXcJBeibatQJ7xRV80K6JW8xL5PK-F-L5ZJTyEySmRRIhcftBfvb5EsoW0-XNUtQ_GYYrA').read()
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
def _lat(addr):
    js = urllib.urlopen("http://maps.google.com/maps/geo?q="+addr+"&output=json&oe=utf8&sensor=true_or_false&key=ABQIAAAATUuAajSTnXcJBeibatQJ7xRV80K6JW8xL5PK-F-L5ZJTyEySmRRIhcftBfvb5EsoW0-XNUtQ_GYYrA").read()
    
    return tuple(json.loads(js)['Placemark'][0]['Point']['coordinates'][:2][::-1])
    

@memoize
def latlongus(addr):
    reader = urllib.urlopen('http://rpc.geocoder.us/service/csv?address='+urllib.quote(addr)).read()
    if "sorry" in reader: return False
    else: return tuple([float(n) for n in reader.split(",")[0:2]])

latlong = latlonggoogle
if USE_GEOCODER_DOT_US: latlong = latlongus
if USE_DECODER: latlong = _lat

@memoize
def get_box(addr):
    js = urllib.urlopen("http://maps.google.com/maps/geo?q="+addr+"&output=json&oe=utf8&sensor=true_or_false&key=ABQIAAAATUuAajSTnXcJBeibatQJ7xRV80K6JW8xL5PK-F-L5ZJTyEySmRRIhcftBfvb5EsoW0-XNUtQ_GYYrA").read()
    box = json.loads(js)["Placemark"][0]["ExtendedData"]["LatLonBox"]
    return ((box["north"],box["west"]),(box["north"],box["east"]),(box["south"],box["east"]),(box["south"],box["west"]))
#print latlongus("Yellowstone Blvd and Scott St, Houston TX")
    
#print _lat("W Holcombe Blvd and Kirby Dr, Houston TX")
#print latlong("W Holcombe Blvd and Kirby Dr, Houston TX")
#getViewbox("Houston, TX")