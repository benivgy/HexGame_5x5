import math

class Hexagon:
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        self.middleX = x
        self.middleY = y
        self.color = color
        self.radius = radius
        self.points = [
            (x + radius * math.cos(math.radians(30 + 60 * i)), y + radius * math.sin(math.radians(30 + 60 * i)))
            for i in range(6)
        ]
        self.taken = False

    def mouseCollision(self, mouse_pos):
        #Retruns wheres the mouse is on a hexagon
        # Mouse position is a tuple (mouse_x, mouse_y)
        mouse_x, mouse_y = mouse_pos

        # Check if the mouse position is within the bounding rectangle of the hexagon
        if (
            self.middleX - self.radius <= mouse_x <= self.middleX + self.radius and
            self.middleY - self.radius <= mouse_y <= self.middleY + self.radius
        ):
            # Check if the mouse position is inside the hexagon using ray casting algorithm
            odd_nodes = False
            j = 5
            for i in range(6):
                if (
                    (self.points[i][1] < mouse_y and self.points[j][1] >= mouse_y) or
                    (self.points[j][1] < mouse_y and self.points[i][1] >= mouse_y)
                ) and (
                    self.points[i][0] + (mouse_y - self.points[i][1]) / (self.points[j][1] - self.points[i][1]) * (self.points[j][0] - self.points[i][0]) < mouse_x
                ):
                    odd_nodes = not odd_nodes
                j = i
            return odd_nodes
        else:
            return False
