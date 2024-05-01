
class DisjointSet:
    def __init__(self, elems):
        self.elems = elems #The cells on the game board and the board boundaries
        self.parent = {}  # Dictionary to store the parent of each element
        self.size = {}  # Dictionary to store the size of each set
        for elem in elems:
            # Initialize each element as a singleton set
            self.make_set(elem)

    def make_set(self, x):
        # Create a new set with a single element
        self.parent[x] = x  # The element is its own parent initially
        self.size[x] = 1  # The size of the set is initially 1

    def find(self, x):
        # Find the representative (root) of the set containing element x
        if self.parent[x] == x:
            return x
        else:
            # Path compression: Update the parent of x to the root
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

    def union(self, x, y):
        # Union operation: Merge the sets containing elements x and y
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return  # Elements are already in the same set
        elif self.size[root_x] < self.size[root_y]:
            # Attach smaller set (root_x) to the larger set (root_y)
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            # Attach smaller set (root_y) to the larger set (root_x)
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

