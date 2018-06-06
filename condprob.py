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

def analyze(dr, key, interval, thr, distr):
    linesl, linesh = getLines2(dr, key)
    total = int(len(linesl) / 4)

    for i in range(total):
        kl, sl = lineToKS(linesl[i * 4 + 2], linesl[i * 4 + 3])
        kh, sh = lineToKS(linesh[i * 4 + 2], linesh[i * 4 + 3])
    
        nors = int(sl / interval) * interval
        distr[nors][0] += 1
        if sh >= thr:
            distr[nors][1] += 1

def __main__():
    assert(len(sys.argv) == 4)

    keys = ["dog", "one"]
    
    dr = sys.argv[1]
    interval = float(sys.argv[2])
    thr = float(sys.argv[3])

    distr = {}
    for m in range(int(1 / interval)):
        distr[interval * m] = [0, 0]
    
    for key in keys:
        analyze(dr, key, interval, thr, distr)

    print(",".join(["Start", "End", "Total", "Recognized"]))
    for m in range(int(1 / interval)):
        s = interval * m
        r = [s, s + interval] + distr[s]
        print(",".join(map(lambda x: str(x), r)))

__main__()
