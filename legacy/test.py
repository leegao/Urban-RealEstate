from filter import Filter

filter = Filter("77005.csv", "University Blvd", "Kirby Dr", "W Holcombe Blvd", "Buffalo Speedway")
sink = filter()
points = {}
for point in sink:
    points[point[2]] = point[1]
    
#print points
keys = points.keys()
keys.sort()
#for key in keys: print key#points[key]

filter = Filter("77005.csv", "University Blvd", "Buffalo Speedway", "W Holcombe Blvd", "Stella Link Rd", "Weslayan St")
sink = filter()
#print len(sink), sink

filter = Filter("77005.csv", "University Blvd", "Weslayan St", "Bissonnet St", "Buffalo Speedway")
sink = filter()
points = {}
for point in sink:
    points[point[2]] = point[1]
    
#print points
keys = points.keys()
keys.sort()
#for key in keys: print points[key]

filter = Filter("77005.csv", "University Blvd", "Kirby Dr", "Bissonnet St", "Buffalo Speedway")
sink = filter()
points = {}
for point in sink:
    points[point[2]] = point[1]
    
#print points
keys = points.keys()
keys.sort()
#for key in keys: print points[key]

#filter = Filter("77005.csv", "University Blvd", "Kirby Dr", "Bissonnet St", "Greenbriar St")


#filter = Filter("77005.csv", "Rice Blvd", "S Shepherd Dr", "Bissonnet St", "Greenbriar St")
#sink = filter()
#points = {}
#for point in sink:
#    points[point[2]] = point[1]
#    
##print points
#keys = points.keys()
#keys.sort()
#for key in keys: print points[key]

filter = Filter("77005.csv", "Bellaire Blvd", "Stella Link Rd", "Weslayan St", "Bissonnet St", "Community Dr")
sink = filter()


filter = Filter("77021.csv", "South Fwy", "Yellowstone Blvd", "Scott St", "Mainer St")
#sink = filter()
#points = {}
#for point in sink:
#    points[point[2]] = point[1]
#    
##print points
#keys = points.keys()
#keys.sort()
for key in keys: print key#points[key]

filter = Filter("77401.csv", "Beechnut St", "S Rice Ave", "Bellaire Blvd", "W Loop S Fwy")
sink = filter()
#print len(sink), sink
points = {}
for point in sink:
    points[point[2]] = point[1]
    
#print points
keys = points.keys()
keys.sort()
#for key in keys: print key#points[key]

