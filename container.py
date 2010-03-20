class point(object):
    def __init__(self, *args):
        self.points = args
    def __getitem__(self, key):
        return float(self.points[key])
    def __len__(self):
        return len(self.points)
    def __repr__(self):
        return "(%s, %s)"%self.points
    def __iter__(self):
        return iter(self.points)
class vector(object):
    def __init__(self, *dir):
        if isinstance(dir, (tuple, list)):
            dir = dir
        self.dir = dir
    def magnitude(self):
        _ret = 0
        for n in self.dir:
            _ret += n**2
        return _ret**(0.5)
    def __getitem__(self, key):
        return float(self.dir[key])
    def __repr__(self):
        return "<%s, %s>"%(self.dir[0],self.dir[1])
    def __add__(self, o):
        return vector(self[0]+o[0],self[1]+o[1])
    def __radd__(self, o):
        return vector(self[0]+o[0],self[1]+o[1])
    def __sub__(self, o):
        return vector(self[0]-o[0],self[1]-o[1])
    def __rsub__(self, o):
        return vector(o[0]-self[0],o[1]-self[1])
    def __mul__(self, k):
        return vector(self[0]*k, self[1]*k)
    def __rmul__(self, k):
        return vector(self[0]*k, self[1]*k)
    def __len__(self):
        return len(self.dir)
class ray(vector):
    def __init__(self, start, dir):
        if not isinstance(start, vector): start = vector(start)
        if not isinstance(dir, vector): dir = vector(dir)
        self.start = start
        self.dir = dir
    def __repr__(self):
        return "%s + n*%s"%(repr(self.start),repr(self.dir))
    def intersect(self, other):
        assert isinstance(other, ray)
        try:
            mu = ((self.start[1]-other.start[1])+self.dir[1]/self.dir[0]*(other.start[0]-self.start[0]))/(other.dir[1]-self.dir[1]*(other.dir[0]/self.dir[0]))
            if isinstance(other, segment):
                if not other.contains(mu*other.dir + other.start):
                    return None
            return mu*other.dir + other.start
        except ZeroDivisionError:
            if self.dir[0] == 0 and other.dir[0] != 0:
                return other.intersect(self)
            else:
                return None
class segment(ray):
    def __init__(self, start, end):
        if not isinstance(start, vector): start = vector(start)
        if not isinstance(end, vector): end = vector(end)
        self.start = start
        self.end = end
        self.dir = end-start
    def __repr__(self):
        return "%s + n*%s = %s"%(repr(self.start),repr(self.dir), repr(self.end))
    def contains(self, *point):
        if not len(point)>1: point = point[0]
        try:
            nparam = (self.end[0]-self.start[0])/self.dir[0]
            parameters = [round((point[n]-self.start[n])/self.dir[n], 7) for n in range(len(point))]
        except ZeroDivisionError:
            n = -1
            for i in range(len(self.dir)):
                p = self.dir[i]
                if not p:
                    if point[i]-self.start[i]: return False
                n = i
            if n < 0: return False
            for i in range(len(self.dir)):
                if i != n:
                    x = point[i]
                    s = self.start[i]
                    e = self.end[i]
                    if self.dir[i] < 0: s = self.end[i];e = self.start[i]
                    if not (x>=s and x<=e): return False
            return True
        for param in parameters:
            if param != parameters[0] or param < 0: return False
        parameters = [p<=nparam for p in parameters]
        return not (False in parameters)
    def intersect(self, other):
        assert isinstance(other, (segment, ray))
        try:
            mu = ((self.start[1]-other.start[1])+self.dir[1]/self.dir[0]*(other.start[0]-self.start[0]))/(other.dir[1]-self.dir[1]*(other.dir[0]/self.dir[0]))
            _ret = mu*other.dir + other.start
            if self.contains(_ret):
                return _ret
            else:
                return None
        except ZeroDivisionError:
            if self.dir[0] == 0 and other.dir[0] != 0:
                return other.intersect(self)
            else:
                return None
class polygon(object):
    #2D by inference
    def __init__(self, *vertices):
        if len(vertices) < 3: return
        self.vertices = vertices
        self.edges = [segment(self.vertices[i-1], self.vertices[i]) for i in range(len(vertices))]
        self.container = {}
        self.exclusion = {}
        for i in range(len(vertices)):
            self.container[vertices[i]]=(self.edges[i-len(vertices)+1], self.edges[i])
            self.exclusion[vertices[i]]=[]
            for edge in self.edges:
                if edge not in self.container[vertices[i]]:
                    self.exclusion[vertices[i]].append(edge)
    def __repr__(self):
        return "Polygon: "+str(self.edges)
    def contains__(self, *point):
        #Legacy Implementation
        p = vector(*point)
        for vertex in self.vertices:
            n = ray(vertex,p-vertex)
            for edge in self.exclusion[vertex]:
                e = n.intersect(edge)
                if not e:
                    #Treat edge cases as exclusionary.
                    return True
                if not (e-vertex).magnitude()>n.dir.magnitude():
                    return False
        return True
    def dist(self, *point):
        """Vectoral Implementation"""
        dists = {}
        for edge in self.edges:
            lam = float((point[1]-edge.start[1])*edge.dir[1]+(point[0]-edge.start[0])*edge.dir[0])/(edge.dir[0]**2+edge.dir[1]**2)
            
            p = lam*edge.dir + edge.start
            if edge.contains(*p.dir):
                dists[edge] = (p-vector(*point)).magnitude()
        return dists
    def _dist(self, *point):
        """Legacy implementation"""
        dists = {}
        for edge in self.edges:
            dist = None
            try:
                k = (edge.end[1]-edge.start[1])/(edge.end[0]-edge.start[0])
                a = -k
                b = 1
                c = k*edge.start[0]-edge.start[1]
                dist = abs((point[0]*a+point[1]*b+c)/(a**2+b**2)**(0.5))
                #print dist
            except ZeroDivisionError:
                dist = abs(point[0]-edge[0])
            if dist is not None:
                dists[edge] = dist
        return dists
    def contains(self, *point):
        p = vector(*point)
        #TODO: Refactor as raytrace
        #Horizontal
        domain = []
        rayx = ray(p, vector(1,0))
        for edge in self.edges:
            inter = rayx.intersect(edge)
            if inter: domain.append(inter[0])
        if len(domain)%2 or not len(domain): return False #Technically an error.
        domain.sort()
        domain = zip(domain[::2], domain[1::2])
        #Vertical
        range = []
        rayy = ray(p, vector(0,1))
        for edge in self.edges:
            inter = rayy.intersect(edge)
            if inter: range.append(inter[1])
        if len(range)%2 or not len(range): return False #Technically an error.
        range.sort()
        range = zip(range[::2], range[1::2])
        for d in domain:
            if point[0]>=d[0] and point[0]<=d[1]: domain=True;break
        for r in range:
            if point[1]>=r[0] and point[1]<=r[1]: range=True;break
        return domain==range