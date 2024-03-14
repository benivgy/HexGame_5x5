
class DisjointSet:
    def __init__(self, elems):
        self.elems = elems
        self.parent = {}
        self.size = {}
        for elem in elems:
            self.make_set(elem)

    def make_set(self, x):
        self.parent[x] = x
        self.size[x] = 1

    def find(self, x):
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        elif self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

# class Group:
#     def __init__(self,index:tuple):
#         self.island = {index}
#
#     def printIsland(self):
#         print(self.island)
#
#     def addToIsland(self,index:tuple):
#         self.island.add(index)
#
#     def mergeIsland(self, otherIsland):
#         """
#         Merges the elements of another group into this group.
#
#         Args:
#             otherIsland: A Group object containing elements to be merged.
#         """
#         # Update the island set of this group with the union of both sets
#         self.island.update(otherIsland.island)
#
#     def neighbors(self,index,boardSize): #Returns a list of the neighbors of a caertain hexagon
#         neighbors=[]
#         row , col = index
#
#         if row-1>=0:
#             neighbors.append((row-1,col))
#             if col+1<boardSize:
#                 neighbors.append((row-1,col+1))
#         if col-1>=0:
#             neighbors.append((row,col-1))
#         if col + 1 < boardSize:
#             neighbors.append((row, col + 1))
#
#         if row+1<boardSize:
#             neighbors.append((row+1,col))
#             if col - 1 >= 0:
#                 neighbors.append((row+1, col - 1))
#         return neighbors
#
#     def areNeighbors(self,otherIsland,boardSize):
#         for index in self.island:
#             for otherIndex in otherIsland.island:
#                 otherIndexNeighbors = self.neighbors(otherIndex,boardSize)
#                 if index in otherIndexNeighbors:
#                     return True
#         return False
#
#
#
