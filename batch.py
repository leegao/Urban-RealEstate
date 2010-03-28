from subprocess import *
from scrape import batch
import os
from see import see
from re import compile

def search(zip):
    return str(zip)+".csv" in os.listdir("zips/")
def process(arg):
    zip = compile(r"\.+(?=.csv)")
    if zip.search(arg):
        return zip.search(arg).group()
    return arg.replace(".csv","")

SEARCH = True

addrs = [
        ("77005.csv","Bellaire Blvd","Stella Link Rd","Weslayan St","Bissonnet St","Community Dr"),
        ("77021.csv","South Fwy","Yellowstone Blvd","Scott St","Mainer St"),
        ("77401.csv","Beechnut St","S Rice Ave","Bellaire Blvd","W Loop S Fwy"),
        ("77025.csv","Braeswood Blvd","Stella Link Rd","S Loop Fwy","Buffalo Speedway"),
        ("77025.csv","Bellaire Blvd","W Holcombe Blvd","Buffalo Speedway","Braeswood Blvd","Stella Link Rd"),
        ("77005.csv","University Blvd","Kirby Dr","Bissonnet St","Buffalo Speedway"),
        ("77008.csv","N Loop Freeway","North Freeway","Katy Freeway"),
        ("77008.csv","N Shepherd Dr","W 20th St","Yale St","W 11th St"),
        ("77096.csv","Hillcroft St", "Beechnut St", "Chimney Rock Rd", "N Braeswood Blvd"),
        ("77005.csv", "University Blvd", "Kirby Dr", "W Holcombe Blvd", "Buffalo Speedway"),
        ("77005.csv", "University Blvd", "Buffalo Speedway", "W Holcombe Blvd", "Stella Link Rd", "Weslayan St"),
        ("77005.csv", "University Blvd", "Weslayan St", "Bissonnet St", "Buffalo Speedway"),
        ("77005.csv", "University Blvd", "Kirby Dr", "Bissonnet St", "Buffalo Speedway"),
        ("77005.csv", "University Blvd", "Kirby Dr", "Bissonnet St", "Greenbriar St"),
        ("77005.csv", "Bellaire Blvd", "Stella Link Rd", "Weslayan St", "Bissonnet St", "Community Dr"),
        ("77401.csv", "Beechnut St", "S Rice Ave", "Bellaire Blvd", "W Loop S Fwy"),
        ("77096.csv", "Chimney Rock Rd", "S Braeswood Blvd", "S Rice Ave", "Rutherglenn Dr"),
        ("77096.csv", "Chimney Rock Rd", "S Braeswood Blvd", "S Rice Ave", "Rutherglenn Dr"),
        ("77401.csv","Chimney Rock Rd","Gulfton St","S Rice Ave","Bellaire Blvd"),
        ("77081.csv","Renwick Dr","Bellaire Blvd","Chimney Rock Rd","Beechnut St"),
        ("77401.csv","Newcastle St","Bellaire Blvd","Stella Link Rd","Braeswood Blvd", "Beechnut St"),
        ("77401.csv","W Loop Fwy","Bellaire Blvd","Newcastle St","Beechnut St"),
        ("77033.csv","S Loop Fwy","Jutland Rd","Bellfort Ave","Cullen Blvd"),
        ("77087.csv", "S Loop Fwy","Broad St","Long Dr", "Telephone Rd"),
        ("77012.csv", "Canal St","E Navigation Blvd","Harrisburg Blvd", "75th St"),
        ("77012.csv", "Harrisburg Blvd", "75th St", "Lawndale St", "Broadway St"),
        ("77011.csv", "Harrisburg Blvd", "75th St", "Lawndale St", "S Wayside Dr"),
        ("77011.csv", "Harrisburg Blvd", "75th St", "Canal St", "N Wayside Dr"),
        ("77011.csv", "Navigation Blvd", "75th St", "Canal St", "N Wayside Dr"),
        ("77011.csv", "Navigation Blvd", "S Lockwood Dr", "Canal St", "N Wayside Dr"),
        ("77011.csv", "Harrisburg Blvd", "S Lockwood Dr", "Canal St", "N Wayside Dr"),
        ("77011.csv", "Harrisburg Blvd", "S Lockwood Dr", "Polk St", "N Wayside Dr"),
        ("77003.csv", "Navigation Blvd", "Lockwood Dr", "Canal St", "N Milby St"),#
        ("77026.csv","Eastex Freeway Service Rd", "Collingsworth St", "Broyles St", "Liberty Rd"),
        ("77026.csv","Eastex Freeway Service Rd", "Lyons Ave", "Broyles St", "Liberty Rd"),
        ("77026.csv","Eastex Freeway Service Rd", "Lyons Ave", "Waco St", "East Fwy"),
        ("77018.csv","Loop West Freeway Service Rd", "N Shepherd Dr", "W 34th St", "Yale St"),
         ]
addrs = [#("77018.csv","Loop West Freeway Service Rd", "N Shepherd Dr", "W 34th St", "Ella Blvd"),
         #("77008.csv","W Loop N Fwy", "W 18th St", "Ella Blvd", "W 11th St", "Hempstead Rd"), 
         ("Houston.3.csv","Houston"),#
         ("Tulsa.csv", "Tulsa, OK"),
         ("Los_Angeles.csv", "Los angeles, CA"),
         ]

if __name__ == "__main__":
    from see import see
    for arg in addrs:
        print "Analyzing vertices: "+ ", ".join(arg[1:])
        zip = process(arg[0])
        if not search(zip):
            print "\tCould not find zipcode: "+str(zip)
            if SEARCH and zip: print "\tAttempting to datamine housing data"; batch(zip, more = ", CA")
            else: print "\tContinuing"; continue
        print "Arguments: "+'"%s" '*len(arg)%arg
        analyze = Popen(["python", "nomarkanalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE)
        o =  analyze.communicate()
        output = o[0]
        
        if len(output)==3:
            pass #Success
        else:
            print "\tAnalysis Failed"
            if o[1]:
                er = ""
                for i in o[1].split("\n"):
                    print "\t"+i
            pass #Failure
        #Popen(["python", "nomarkanalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        #Popen(["python", "histanalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        #Popen(["python", "contour3danalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        #Popen(["python", "surface3danalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        #Popen(["python", "scatter3danalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        #Popen(["python", "wire3danalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        Popen(["python", "nmcontouranalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
        Popen(["python", "mcontouranalysis.py"]+list(arg), stdout=PIPE, stderr = PIPE).communicate()
    