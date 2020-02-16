class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def translate_new(self, dx, dy):
        p = Point(self.x, self.y)
        p.x += dx
        p.y += dy
        return p
