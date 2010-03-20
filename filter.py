import csv, container, geocode
v = container.vector

class Filter(object):
    CITY = "Houston TX"
    def __init__(self, data, *streets):
        self.data = "zips/"+data
        self.streets = streets
        
    def read(self):
        read = csv.reader(open(self.data))
        data = []
        for row in read:
            if row[0] == 'Address': continue
            #Row[3] => Price, Row[4] => Price/sqft
            #print row
            data += [((float(row[1]), float(row[2])), float(row[4]))]
        return data
    
    def auto(self, *streets):
        #Make sure that this is in correct order
        intersections = [streets[i]+" and "+streets[i-len(streets)+1]+", "+self.CITY for i in range(len(streets))]
        self.intersections = intersections
        try:
            coords = [v(*geocode.latlong(intersection)) for intersection in intersections]
        except:
            return None
        self.coords = coords
        return container.polygon(*coords)
    
    def __call__(self, *streets):
        if not streets: streets = self.streets
        filter = self.auto(*streets)
        if not filter: return []
        data = self.read()
        sink = []
        for point in data:
            if filter.contains(*point[0]):
                dists = filter.dist(*point[0])
                lowest = dists[dists.keys()[0]]
                for dist in dists:
                    if dists[dist] < lowest: lowest = dists[dist]
                sink.append(tuple(list(point)+[lowest]))
        return sink

if __name__ == "__main__":
    filter = Filter("data.csv", "University Blvd", "Kirby Dr", "W Holcombe Blvd", "Buffalo Speedway")
    print filter()