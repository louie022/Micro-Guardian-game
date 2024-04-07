class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rect(x, y, width, height)
        self.capacity = capacity
        self.particles = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        self.northwest = QuadTree((x, y, w/2, h/2), self.capacity)
        self.northeast = QuadTree((x + w/2, y, w/2, h/2), self.capacity)
        self.southwest = QuadTree((x, y + h/2, w/2, h/2), self.capacity)
        self.southeast = QuadTree((x + w/2, y + h/2, w/2, h/2), self.capacity)
        self.divided = True

    def insert(self, particle):
        if not self.boundary.contains(particle):
            return False

        if len(self.particles) < self.capacity:
            self.particles.append(particle)
            return True
        else:
            if not self.divided:
                self.subdivide()

            return (self.northwest.insert(particle) or
                    self.northeast.insert(particle) or
                    self.southwest.insert(particle) or
                    self.southeast.insert(particle))

    def query(self, range, found):
        if not self.boundary.intersects(range):
            return found

        for p in self.particles:
            if range.contains(p):
                found.append(p)

        if self.divided:
            self.northwest.query(range, found)
            self.northeast.query(range, found)
            self.southwest.query(range, found)
            self.southeast.query(range, found)

        return found
