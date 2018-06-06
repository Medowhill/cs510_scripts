import sys

def getLines2(dr, key):
    return (getLines(dr, key, "low"), getLines(dr, key, "high"))

def getLines(dr, key, hl):
    name = dr + "/" + key + hl + ".pb.log"
    f = open(name, "r")
    lines = f.readlines()
    f.close()
    return lines

def lineToKS(l1, l2):
    i11 = l1.index("(")
    i12 = l1.index("=")
    i21 = l2.index("(")
    i22 = l2.index("=")
    return (l1[0:i11-1], float(l1[i12+2:-2]))

def analyze(dr, key):
    linesl, linesh = getLines2(dr, key)
    total = int(len(linesl) / 4)

    for i in range(total):
        kl, sl = lineToKS(linesl[i * 4 + 2], linesl[i * 4 + 3])
        kh, sh = lineToKS(linesh[i * 4 + 2], linesh[i * 4 + 3])
        print(str(sl) + "," + str(sh))

def __main__():
    assert(len(sys.argv) == 2)

    keys = ["on", "stop", "right", "yes"]
#    keys = ["dog", "one"]
    
    dr = sys.argv[1]
    
    print("LITTLE,big")
    for key in keys:
        analyze(dr, key)

__main__()
