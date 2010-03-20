from subprocess import *
from scrape import batch
import os
from see import see
from re import compile

def search(zip):
    return str(zip)+".csv" in os.listdir("zips/")
def process(arg):
    zip = compile(r"\d+(?=.csv)")
    if zip.search(arg):
        return zip.search(arg).group()
    return 0

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
        ("77005.csv", "Rice Blvd", "S Shepherd Dr", "Bissonnet St", "Greenbriar St"),
        ("77005.csv", "Bellaire Blvd", "Stella Link Rd", "Weslayan St", "Bissonnet St", "Community Dr"),
        ("77401.csv", "Beechnut St", "S Rice Ave", "Bellaire Blvd", "W Loop S Fwy"),
        ("77096.csv", "Chimney Rock Rd", "S Braeswood Blvd", "S Rice Ave", "Rutherglenn Dr"),
        ("77081.csv", "Renwick Dr", "Gulfton Dr", "Chimney Rock Rd", "Bellaire Blvd")
        
        ]

if __name__ == "__main__":
    from see import see
    for arg in addrs:
        print "Analyzing vertices: "+ ", ".join(arg[1:])
        zip = process(arg[0])
        if not search(zip):
            print "\tCould not find zipcode: "+str(zip)
            if SEARCH and zip: print "\tAttempting to datamine housing data"; batch(zip)
            else: print "\tContinuing"; continue
        
        analyze = Popen(["python", "analyze.py"]+list(arg), stdout=PIPE, stderr = PIPE)
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
    