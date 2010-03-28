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
            data += [((float(row[1]), float(row[2])), float(row[3]))]
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
                #dists = filter.dist(*point[0])
                #lowest = dists[dists.keys()[0]]
                #for dist in dists:
                #    if dists[dist] < lowest: lowest = dists[dist]
                if point[1] > 1000000: continue
                sink.append(tuple(list(point)))
        return sink
class CoordFilter(object):
    def __init__(self, data, *coords):
        self.data = "zips/"+data
        coords = [v(*c) for c in coords]
        self.coords = coords
        
    def read(self):
        read = csv.reader(open(self.data))
        data = []
        for row in read:
            if row[0] == 'Address': continue
            #Row[3] => Price, Row[4] => Price/sqft
            if int(row[3])>10000000: continue
            if float(row[4])>1000: continue
            data += [((float(row[1]), float(row[2])), float(row[4]))]
        return data
    
    def auto(self):
        #Make sure that this is in correct order
        #intersections = [streets[i]+" and "+streets[i-len(streets)+1]+", "+self.CITY for i in range(len(streets))]
        #self.intersections = intersections
        
        return container.polygon(*self.coords)
    
    def __call__(self, mask=True):
        filter = self.auto()
        if not filter: return []
        data = self.read()
        
        #Outlier Analysis
        mean = float(sum([d[1] for d in data]))/len(data)
        med_ = [p[1] for p in data]
        med_.sort()
        l = len(med_)
        median = float(med_[(l/2-1)]+(med_[l/2] if not l%2 else l/2-1))/(2)
        median = mean
        devs = [float((d[1]-median)**2)/len(data) for d in data]
        stdev = sum(devs)**(0.5)
        
        z = [float(abs(d[1]-median))/stdev for d in data]
        
        
        sink = []
        for point in data:
            if filter.contains(*point[0]):
                point = list(point)
                #if point[1] > 1500000: point[1]=1500000
                if float(abs(point[1]-median))/stdev > 3:
                    pass
                    #print point[1], stdev, median, float(abs(point[1]-median))/stdev, float((3)*stdev+median)
                if float(abs(point[1]-median))/stdev > 3 and mask: point[1] = int((3)*stdev+median)
                sink.append(tuple(list(point)))
        return sink
if __name__ == "__main__":
    filter = Filter("data.csv", "University Blvd", "Kirby Dr", "W Holcombe Blvd", "Buffalo Speedway")
    #print filter()
    cfilter = CoordFilter("Houston.3.csv", *geocode.get_box("Houston, TX"))
    cfilter()