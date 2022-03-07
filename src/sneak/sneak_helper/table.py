from src.sneak.sneak_helper.tree_node import TreeNode
from src.sneak.sneak_helper.item import Item
from collections import defaultdict
import math
import re
import secrets

class Table:

    def __init__(self, uid):
        self.uid = uid
        self.count = 0
        self.cols = []
        self.rows = []
        self.fileline = 0
        self.linesize = 0
        self.skip = []
        self.y = []
        self.nums = []
        self.syms = []
        self.w = defaultdict(int)
        self.x = []
        self.xnums = []
        self.xsyms = []
        self.header = ""

    @staticmethod
    def compiler(x):
        try:
            int(x)
            return int(x)
        except:
            try:
                float(x)
                return float(x)
            except ValueError:
                return str(x)

    @staticmethod
    def read(file):
        lines = []
        with open(file) as f:
            curline = ""
            for line in f:
                line = line.strip()
                if line[len(line) -1] ==",":
                    curline += line
                else:
                    curline += line
                    lines.append(curline)
                    curline = ""
        return lines

    @staticmethod
    def linemaker(src, sep=",", doomed=r'([\n\t\r ]|#.*)'):
        lines = []
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                lines.append(line.split(sep))
        return lines

    def __add__(self, line):
        if len(self.header) > 0:
            self.insert_row(line)
        else:
            self.create_cols(line)

    def create_cols(self, line):
        self.header = line
        index = 0
        for val in line:
            val = self.compiler(val)
            if val[0] == "?":
                self.skip.append(index + 1)
            if val[0].isupper() or "-" in val or "+" in val:
                self.nums.append(index+1)
                self.cols.append(Num(''.join(c for c in val if not c in ['?']), index+1))
            else:
                self.syms.append(index+1)
                self.cols.append(Sym(''.join(c for c in val if not c in ['?']), index+1))

            if "!" in val or "-" in val or "+" in val:
                self.y.append(index+1)
                if "-" in val:
                    self.w[index+1] = -1
                if "+" in val:
                    self.w[index+1] = 1
            if "-" not in val and "+" not in val and "!" not in val:
                self.x.append(index+1)
                if val[0].isupper():
                    self.xnums.append(index + 1)
                else:
                    self.xsyms.append(index+1)
            index+=1
            self.linesize = index
            self.fileline += 1

    def insert_row(self, line):
        self.fileline +=1
        # print("inserting row", self.fileline, "of size", len(line), "expected = ", self.linesize)
        if len(line) != self.linesize:
            print("Line", self.fileline, "has an error")
            return
        realline = []
        realindex = 0
        index = 0
        for val in line:
            if index+1 not in self.skip:
                if val == "?" or val == "":
                    realline.append(val)
                    realindex += 1
                    continue
                self.cols[realindex] + self.compiler(val)
                realline.append(val)
                realindex += 1
            else:
                realindex += 1
            index += 1
        self.rows.append(line)
        self.count += 1

    def dump(self, f):
        f.write("Dump table:"+"\n")
        f.write("t.cols"+"\n")
        for i, col in enumerate(self.cols):
            if i+1 in self.skip:
                continue
            if i+1 in self.nums:
                f.write("|  "+str(col.uid)+"\n")
                f.write("|  |  col: "+str(col.uid)+"\n")
                f.write("|  |  hi: "+str(col.hi)+"\n")
                f.write("|  |  lo: "+str(col.lo)+"\n")
                f.write("|  |  m2: "+str(col.m2)+"\n")
                f.write("|  |  mu: "+str(col.mu)+"\n")
                f.write("|  |  n: "+str(col.n)+"\n")
                f.write("|  |  sd: "+str(col.sd)+"\n")
                f.write("|  |  name: "+str(col.name)+"\n")
            else:
                f.write("|  " + str(col.uid) + "\n")
                f.write("|  |  col: "+str(col.uid)+"\n")
                f.write("|  |  mode: "+str(col.mode)+"\n")
                f.write("|  |  most: "+str(col.most)+"\n")
                f.write("|  |  n: " + str(col.n) + "\n")
                f.write("|  |  name: " + str(col.name) + "\n")

        f.write("t.my: "+"\n")
        f.write("|  len(cols): " + str(len(self.cols))+"\n")
        f.write("|  y" + "\n")
        for v in self.y:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")
        f.write("|  nums" + "\n")
        for v in self.nums:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")
        f.write("|  syms" + "\n")
        for v in self.syms:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")
        f.write("|  w" + "\n")
        for k, v in self.w.items():
            if v not in self.skip:
                f.write("|  |  " + str(k) + ": "+str(v)+"\n")
        f.write("|  x" + "\n")
        for v in self.x:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")
        f.write("|  xnums" + "\n")
        for v in self.xnums:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")
        f.write("|  xsyms" + "\n")
        for v in self.xsyms:
            if v not in self.skip:
                f.write("|  |  " + str(v) + "\n")

    def split(self):
        """
        Implements continous space Fastmap for bin chop on data
        """
        pivot = secrets.choice(self.rows)
        east = self.mostDistant(pivot)
        west = self.mostDistant(east)
        c = self.distance(east,west)
        items = [[row, 0] for row in self.rows]

        for x in items:
            a = self.distance(x[0], west)
            b = self.distance(x[0], east)
            x[1] = (a ** 2 + c**2 - b**2)/(2*c) #cosine rule

        items.sort(key = lambda x: x[1]) #sort by distance
        splitpoint = len(items) // 2 #integral divison
        eastItems = self.rows[: splitpoint]
        westItems = self.rows[splitpoint:]

        return [east, west, eastItems, westItems]

    def split_bin(self, total_group = 10):
        """
        Implements binary space Fastmap for bin chop on data
        """
        pivot = secrets.choice(self.rows)
        east = self.mostDistant(pivot)
        west = self.mostDistant(east)
        c = self.distance(east,west)
        items = [[row, 0] for row in self.rows]

        for x in items:
            a = self.distance(x[0], west)
            b = self.distance(x[0], east)
            x[1] = (a ** 2 + c**2 - b**2)/(2*c) #cosine rule

        items.sort(key = lambda x: x[1]) #sort by distance
        splitpoint = len(items) // 2 #integral divison
        eastItems = self.rows[: splitpoint]
        westItems = self.rows[splitpoint:]

        return [east, west, eastItems, westItems]

    def distance(self, x_original_row, y_row):
        x_row = x_original_row
        distance = 0
        if len(x_row) != len(y_row):
            return -float('inf')
        for i, (x,y) in enumerate(zip(x_row, y_row)):
            d = self.cols[i].dist(self.compiler(x),self.compiler(y)) #compile the x & y bc it's in a text format
            distance += d
        return distance

    def mostDistant(self, x_original_row):
        x_row = x_original_row
        distance = -float('inf')
        point = None

        for row in self.rows:
            d = self.distance(x_row, row)
            if d > distance:
                distance = d
                point = row
        return point

    @staticmethod
    def sneakClusters(items, table, enough):
        if len(items) < enough:
            eastTable = Table(0)
            eastTable + table.header
            for item in items:
                eastTable + item
            return TreeNode(None, None, eastTable, None, None, None, True, table.header)

        west, east, westItems, eastItems = table.split()

        eastTable = Table(0)
        eastTable + table.header
        for item in eastItems:
            eastTable + item

        westTable = Table(0)
        westTable + table.header
        for item in westItems:
            westTable + item

        eastNode = Table.sneakClusters(eastItems, eastTable, enough)
        westNode = Table.sneakClusters(westItems, westTable, enough)
        root = TreeNode(east, west, eastTable, westTable, eastNode, westNode, False, table.header)
        return root

    def csvDump(self, f):
        for i, col in enumerate(self.cols):
            if i+1 in self.skip:
                continue
            if i+1 in self.nums:
                f.write(str(col.uid) + ",")
                f.write(str(col.hi)+",")
                f.write(str(col.lo)+",")
                f.write(str(col.m2)+",")
                f.write(str(col.mu)+",")
                f.write(str(col.n)+",")
                f.write(str(col.sd)+",")
            else:
                f.write(str(col.uid)+",")
                f.write(str(col.mode)+",")
                f.write(str(col.most)+",")
                f.write(str(col.n) + ",")
        f.write("\n")

    def csvHeader(self):
        header = ""
        for i, col in enumerate(self.cols):
            if i+1 in self.skip:
                continue
            if i+1 in self.nums:
                header += (str(col.name)+"_uid,")
                header += (str(col.name)+"_hi,")
                header += (str(col.name)+"_lo,")
                header += (str(col.name)+"_m2,")
                header += (str(col.name)+"_mu,")
                header += (str(col.name)+"_n,")
                header += (str(col.name)+"_sd,")
            else:
                header += (str(col.name)+"_uid,")
                header += (str(col.name)+"_mode,")
                header += (str(col.name)+"_most,")
                header += (str(col.name)+"_n,")
        header += "\n"
        return header

class Col:

    def __init__(self, name):
        self.name = name
        self.asked = False

    def __add__(self,v):
        return v

    def variety(self):
        return 0

    def xpect(self, j):
        return 0

    def like(self,x,prior, m):
        return 0

    def mid(self):
        return 0

    def dist(self, x, y):
        return 0

    def ask(self):
        self.asked = True

class Sym(Col):

    def __init__(self,name,uid,data=None):
        Col.__init__(self,name)
        self.n = 0
        self.most = 0
        self.mode = ""
        self.uid = uid
        self.cnt = defaultdict(int)
        if data != None:
            for val in data:
                self + val

    def __add__(self, v):
        self.n += 1
        self.cnt[v] += 1
        tmp = self.cnt[v]
        if tmp > self.most:
            self.most = tmp
            self.mode = v
        return v

    def variety(self):
        e = 0
        for k, v in self.cnt.items():
            p = v/self.n
            e -= p*math.log(p)/math.log(2)

    def xpect(self, j):
        n = self.n + j.n
        return self.n/n * self.variety() + j.n/n * j.variety()

    def like(self, x, prior, m):
        f = self.cnt[x]
        return (f + m * prior)/(self.n + m)

    def mid(self):
        return self.mode

    def dist(self, x, y):
        if (x == "?" or x == "") or (y == "?" or y == ""):
            return 1
        return 0 if x == y else 1

class Num(Col):

    def __init__(self, name, uid, data=None):
        Col.__init__(self, name)
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.lo = float('inf')
        self.hi = -float('inf')
        self.vals = []
        self.uid = uid
        if data != None:
            for val in data:
                self + val

    def __add__(self, v):
        self.n += 1
        self.vals.append(v)
        try:
            if v < self.lo:
                self.lo = v
            if v > self.hi:
                self.hi = v
            d = v - self.mu
            self.mu += d / self.n
            self. m2 += d * (v - self.mu)
            self.sd = self._numSd()
        except:
            print("failed col name:", self.name, self.uid)
        return v

    def _numSd(self):
        if self.m2 < 0:
            return 0
        if self.n < 2:
            return 0
        return math.sqrt(self.m2/(self.n -1))

    def variety(self):
        return self.sd

    def xpect(self, j):
        n = self.n + j.n
        return self.n / n * self.variety() + j.n / n * j.variety()

    def like(self, x, prior, m):
        var = self.sd **2
        denom = math.sqrt(math.pi * 2 * var)
        num = (math.e ** (-(x-self.mu)**2)/(2*var+10e-4))

    def mid(self):
        return self.mu

    def dist(self, x, y):
        if (x == "?" or x == "") and (y == "?" or y == ""):
            return 1
        if (x == "?" or x == "") or (y == "?" or y == ""):
            x = x if (y == "?" or y == "") else y
            x = self._numNorm(x)
            y = 0 if x > 0.5 else 1
            return y - x
        return self._numNorm(x) - self._numNorm(y)

    def _numNorm(self, x):
        return (x - self.lo)/(self.hi - self.lo + 10e-32)

