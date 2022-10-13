from itertools import permutations


def distance(point1, point2):

    # returns absolute value of distance
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5


def total_distance(points):

    # returns the total distance of the inputed path
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])


def travelling_salesman(points, start=None):
    
    # returns the minimum distance path that traverses all points in a cycle by brute force
    if start is None:
        start = points[0]
    return min([perm for perm in permutations(points) if perm[0] == start], key=total_distance)