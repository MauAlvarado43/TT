import math

def mid_point(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / math.pi