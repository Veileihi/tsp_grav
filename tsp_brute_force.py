from itertools import permutations


def distance(point1, point2):

    # returns absolute value of distance
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5


def total_distance(points):

    # returns the total distance of the inputed path
    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])


def travelling_salesman(points, start=None):
    co_ords = [body[1] for body in points.items()]


    # returns the minimum distance path that traverses all points in a cycle by brute force
    if start is None:
        start = co_ords[0]

    shortest_root = min([perm for perm in permutations(co_ords) if perm[0] == start], key=total_distance)

    final = []
    body_only = []
    for i in shortest_root:
        for j in points.items():
            if i == j[1]:
                final.append(j)
                body_only.append(j[0])

    return final, body_only