import math

#Uppgift 1: räkna antal björkar

def read_trees(fname):
    file = open(fname, "r", encoding="utf-8")
    rows = file.readlines()
    file.close()
    return rows[1:]

def is_birch(tree):
    return tree.find("jörk") >= 0

big_file = "trad.csv"

trees = read_trees(big_file)
tot = 0
for tree in trees:
    if is_birch(tree):
        tot = tot + 1
print("There are a total of", tot, "birches in the file")


# Uppgift 2: överskatta (tomma namn = björk, men inte rönn)

def is_birch(tree):
    parts = tree.split(";")
    if parts[2] == "" and parts[3] == "":
        return True
    elif parts[2] == "Sorbus Aucuparia":
        return False
    elif parts[3].find("jörk") >= 0:
        return True
    else:
        return False

trees = read_trees(big_file)
tot = 0
for tree in trees:
    if is_birch(tree):
        tot = tot + 1
print("Overestimating (but no rowan) there are", tot, "birches in the file")


# Uppgift 3: relevanta björkar nära fontänen

mit_fountain = [63.820560, 20.305810]

def coords(line):
    parts = line.split(";")
    coordsn = parts[0]
    coords = coordsn.split(",")
    coords[0] = float(coords[0])
    coords[1] = float(coords[1])
    return coords

def dist(x1, y1, x2, y2):
    distx = x1 - x2
    disty = y1 - y2
    return math.sqrt(distx**2 + disty**2)

trees = read_trees(big_file)
tot = 0
for tree in trees:
    if is_birch(tree):
        t_coord = coords(tree)
        t_dist = dist(t_coord[0], t_coord[1], mit_fountain[0], mit_fountain[1])
        if t_dist <= 0.1:
            tot = tot + 1
print("There are", tot, "birches in actual Umeå")


# Uppgift 4: struktur (klass + metoder)

class Tree:
    def __init__(self, tree):
        parts = tree.split(";")

        self.pos = parts[0].split(", ")
        self.pos[0] = float(self.pos[0])
        self.pos[1] = float(self.pos[1])

        self.leafy = parts[1] == "Lövträd"
        self.latin_name = parts[2]
        self.swe_name = parts[3]
        self.function = parts[4]
        self.planted = parts[5]

    def coords(self):
        return self.pos

    def is_birch(self):
        if self.latin_name == "" and self.swe_name == "":
            return True
        elif self.latin_name == "Sorbus Aucuparia":
            return False
        elif self.swe_name.find("jörk") >= 0:
            return True
        else:
            return False

    def dist(self, x, y):
        return dist(x, y, self.pos[0], self.pos[1])

    def dist_from_tree(self, tree):
        return self.dist(tree.pos[0], tree.pos[1])

def read_trees(fname):
    file = open(fname, "r")
    rows = file.readlines()
    file.close()

    trees = []
    for row in rows[1:]:
        trees.append(Tree(row))
    return trees

trees = read_trees("trad.csv")
tree = trees[0]
print(tree.is_birch())
print(tree.dist(63.8204078, 20.3055167))


# Uppgift 6: hitta närmsta träd (gamla disten)

all_trees = read_trees("trad.csv")

min_dist_seen = 1000000
closest_tree = None
for tree in all_trees:
    new_dist = tree.dist(mit_fountain[0], mit_fountain[1])
    if new_dist < min_dist_seen:
        min_dist_seen = new_dist
        closest_tree = tree

print("Det närmsta trädet", closest_tree.swe_name, "vid",
      closest_tree.pos, "är", min_dist_seen, "ifrån")


# Uppgift 7: ny dist i meter (överskriver dist-funktionen)

def to_radian(ang_deg):
    return ang_deg * math.pi / 180

def dist(x1, y1, x2, y2):
    x1 = to_radian(x1)
    x2 = to_radian(x2)
    ydiff = to_radian(y1 - y2)
    v1 = math.sin(x1) * math.sin(x2)
    v2 = math.cos(x1) * math.cos(x2) * math.cos(ydiff)
    return math.acos(v1 + v2) * 6371000

min_dist_seen = 100000
closest_tree = None
for tree in all_trees:
    new_dist = tree.dist(mit_fountain[0], mit_fountain[1])
    if new_dist < min_dist_seen:
        min_dist_seen = new_dist
        closest_tree = tree

print("Det närmsta trädet", closest_tree.swe_name, "vid",
      closest_tree.pos, "är", min_dist_seen, "meter ifrån")

