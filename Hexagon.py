import math


class Hexagon:
    def __init__(self,x,y,radius,color=(255,255,255)):
        self.middleX=x
        self.middleY=y
        self.color=color
        self.points =[
            (x + radius * math.cos(math.radians(30 + 60 * i)), y + radius * math.sin(math.radians(30 + 60 * i)))
            for i in range(6)
        ]
        self.taken=False
