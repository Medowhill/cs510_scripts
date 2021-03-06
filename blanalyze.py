import sys

THR = 0.7
FTR = 0.2

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

    total_w = getTotal(dr, keys)
    total_n = getTotal(dr, nkeys)
    
    tph, tpl = target(dr, keys, wordanalyze)
    tnh, tnl = target(dr, nkeys, nonwordanalyze)
    target_tp = tph * (1 - FTR) + tpl * FTR
    target_tn = tnh * (1 - FTR) + tnl * FTR

    best = (-1, -1, 0, 0, total_n)
    for th1 in range(0, 101, 1):
        for th2 in range(th1, 101, 1):
            tp = 0
            tn = 0
            bu = 0
            for key in keys:
                bu_, tp_ = blwordanalyze(dr, key, th1 / 100.0, th2 / 100.0)
                tp += tp_
            for key in nkeys:
                bu_, tn_ = blnonwordanalyze(dr, key, th1 / 100.0, th2 / 100.0)
                bu += bu_
                tn += tn_
            if target_tp <= tp and target_tn <= tn and bu < best[4]:
                best = (th1, th2, tp, tn, bu)
    th1, th2, tp, tn, bu = best

    print(total_w, total_n)
    print("%.3f %.3f" % (tpl / total_w, tnl / total_n))
    print("%.3f %.3f" % (tph / total_w, tnh / total_n))
    print("%.3f %.3f" % (target_tp / total_w, target_tn / total_n))
    print(th1, th2)
    print(tp, tn, bu)
    print("%.3f %.3f %.3f" % (tp / total_w, tn / total_n, bu / total_n))

__main__()
