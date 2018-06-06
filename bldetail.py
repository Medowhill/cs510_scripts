import sys

THR = 0.7

def getTotal(dr, keys):
    total = 0
    for key in keys:
        total += len(getKSs(dr, key, "low"))
    return total

def getKSs2(dr, key):
    return (getKSs(dr, key, "low"), getKSs(dr, key, "high"))

filecache = {}
def getKSs(dr, key, hl):
    name = dr + "/" + key + hl + ".pb.log"
    if name in filecache:
        return filecache[name]
    else:
        f = open(name, "r")
        lines = f.readlines()
        f.close()
        ks = parseToKS(lines)
        filecache[name] = ks
        return ks

def lineToKS(l1, l2):
    i11 = l1.index("(")
    i12 = l1.index("=")
    i21 = l2.index("(")
    i22 = l2.index("=")
    return (l1[0:i11-1], float(l1[i12+2:-2]))

def parseToKS(lines):
    ks = []
    for i in range(int(len(lines) / 4)):
        ks.append(lineToKS(lines[i * 4 + 2], lines[i * 4 + 3]))
    return ks

def wordanalyze(dr, key, hl):
    TP = 0
    for ks in getKSs(dr, key, hl):
        k, s = ks
        if s >= THR and k == key:
            TP += 1
    return TP

def nonwordanalyze(dr, key, hl):
    TN = 0
    for ks in getKSs(dr, key, hl):
        k, s = ks
        if s < THR or k == "_unknown_" or k == "_silence_":
            TN += 1
    return TN

def blwordanalyze(dr, key, th1, th2):
    BU = 0
    TP = 0
    ksl, ksh = getKSs2(dr, key)
    for i in range(len(ksl)):
        kl, sl = ksl[i]
        kh, sh = ksh[i]
        if kl != "_unknown_" and kl != "_silence_":
            if th1 <= sl and sl < th2:
                BU += 1
                if THR <= sh and kh == key:
                    TP += 1
            elif th2 <= sl:
                TP += 1
    return (BU, TP)

def blnonwordanalyze(dr, key, th1, th2):
    BU = 0
    TN = 0
    ksl, ksh = getKSs2(dr, key)
    for i in range(len(ksl)):
        kl, sl = ksl[i]
        kh, sh = ksh[i]
        if kl != "_unknown_" and kl != "_silence_":
            if th1 <= sl and sl < th2:
                BU += 1
                if sh < THR or kh == "_unknown_" or kh == "_silence_":
                    TN += 1
            elif sl < th1:
                TN += 1
        else:
            TN += 1
    return (BU, TN)

def target(dr, keys, a):
    vl = 0
    vh = 0
    for key in keys:
        vl += a(dr, key, "low")
        vh += a(dr, key, "high")
    return (vh, vl)

def __main__():
    assert(len(sys.argv) == 2)
    dr = sys.argv[1]
    keys = ["on", "right", "stop", "yes"]
    nkeys = ["dog", "one"]

    total = getTotal(dr, nkeys)

    print("", end=",")
    for th2 in range(0, 101, 5):
        print(th2, end=",")
    print()

    for th1 in range(0, 101, 5):
        print(th1, end=",")
        for th2 in range(0, 101, 5):
            if th2 < th1:
                print("", end=",")
            else:
                bu = 0
                for key in nkeys:
                    bu_, tn_ = blnonwordanalyze(dr, key, th1 / 100.0, th2 / 100.0)
                    bu += bu_
                print("%.3f" % (bu / total), end=",")
        print()


__main__()
