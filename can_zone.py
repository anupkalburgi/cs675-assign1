__author__ = 'anupkalburgi'

import math
import Pyro4

@Pyro4.expose
class Point(object):
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]

    # def __lt__(self, other):
    #     return bool(self.x < other.x and )

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.x)

    #Check Idea borowed from http://stackoverflow.com/questions/2303278/find-if-4-points-on-a-plane-form-a-rectangle
def is_rectangle(points):
    if len(points) == 4:
        point1,point2,point3,point4 = points
        cx = (point1[0]+point2[0]+point3[0]+point4[0])/4
        cy = (point1[1]+point2[1]+point3[1]+point4[1])/4

        dd1 = pow((cx-point1[0]), 2) + pow((cy-point1[1]), 2)
        dd2 = pow((cx-point2[0]), 2) + pow((cy-point2[1]), 2)
        dd3 = pow((cx-point3[0]), 2) + pow((cy-point3[1]), 2)
        dd4 = pow((cx-point4[0]), 2) + pow((cy-point4[1]), 2)

        return dd1 == dd2 and dd1 == dd3 and dd1 == dd4
    else:
        return False


@Pyro4.expose
class CAN_Zone(object):
    def __init__(self, xy_min, xy_max):
        # Type assertion makes sense to test the pre-condition invariant but not sure in this case
        self.min = Point(xy_min)
        self.max = Point(xy_max)

    def __contains__(self, point):
        return bool(self.min.x <= point.x <= self.max.x and self.min.y <= point.y <= self.max.y)

    def __repr__(self):
        return '(%s,%s)-(%s,%s)' % (self.min.x,self.min.y,self.max.x,self.max.y)

    @property
    def height(self):
        return self.max.y - self.min.y

    @property
    def width(self):
        return self.max.x - self.min.x

    @property
    def area(self):
        return self.height * self.width

    @property
    def center(self):
        return Point((self.max.x/2, self.max.y/2))

    def isSquare(self):
        return bool(self.height == self.width)

    def within(self, zone):
        return bool(set(self.sides()).intersection(zone.sides()))
        # return (self.min.x <= zone.min.x <= zone.max.x <= self.max.x
        #         or self.min.y <= zone.min.y <= zone.max.y <= self.max.y)

    def sides(self):
        return [(self.min.x, self.min.y),
                (self.max.x, self.min.y),
                (self.min.x, self.max.y),
                (self.max.x, self.max.y)]

    def is_valid_merge(self,zone):
        all_sides = self.sides() + zone.sides()
        common_sides = set(self.sides()).intersection(zone.sides())
        sides = set(all_sides) - common_sides
        return is_rectangle(list(sides))


    @staticmethod
    def distance_cal(point1, point2):
        dist = math.sqrt(pow((point1.x - point2.x), 2) + pow((point1.y - point2.y), 2))
        return dist

    def distance(self, point):
        return self.distance_cal(point, self.center)

    def _hsplit(self):
        first_min_xy = (self.min.x, self.min.y)
        first_max_xy = (self.max.x, self.max.y/2.0)

        second_min_xy = (self.min.x, self.max.y/2.0)
        second_max_xy = (self.max.x, self.max.y)
        return CAN_Zone(first_min_xy, first_max_xy),CAN_Zone(second_min_xy,second_max_xy)

    def _vsplit(self):
        first_min_xy = (self.min.x, self.min.y)
        first_max_xy = (self.max.x/2.0, self.max.y)

        second_min_xy = (self.max.x / 2.0, self.min.y)
        second_max_xy = (self.max.x, self.max.y)
        return CAN_Zone(first_min_xy, first_max_xy), CAN_Zone(second_min_xy, second_max_xy)

    def split(self):
        if self.isSquare():
            return self._vsplit() #V/H-Split to return two tuples xy_min and xy_max
        else:
            return self._hsplit()

    def merge(self,zone):
        x_min = min(self.x,zone.min.x)
        y_min = min(self.y,self.min.y)

        x_max = max(self.x,zone.max.x)
        y_max = max(self.y,zone.max.y)
        return CAN_Zone((x_min,y_min),(x_max,y_max))
