import sys

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

def wordanalyze(dr, key, thr, hl):
    TP = 0
    FN = 0
    
    lines = getLines(dr, key, hl)
    total = int(len(lines) / 4)
    for i in range(total):
        k, s = lineToKS(lines[i * 4 + 2], lines[i * 4 + 3])
        if s < thr or k != key:
            FN += 1
        else:
            TP += 1
    return [total, TP, FN]

def nonwordanalyze(dr, key, thr, hl):
    FP = 0
    TN = 0
    
    lines = getLines(dr, key, hl)
    total = int(len(lines) / 4)
    for i in range(total):
        k, s = lineToKS(lines[i * 4 + 2], lines[i * 4 + 3])
        if s < thr or k == "_unknown_" or k == "_silence_":
            TN += 1
        else:
            FP += 1
    return [total, TN, FP]

def __main__():
    assert(len(sys.argv) == 3)

    keys = ["on", "right", "stop", "yes"]
    nkeys = ["dog", "one"]
    
    dr = sys.argv[1]
    hl = sys.argv[2]
    assert(hl == "high" or hl == "low")
    
    print(",".join(["Threshold", "Total(word)", "TP", "FN", "Total(nonword)", "TN", "FP"]))
    for thr in range(50, 100, 5):
        resw = [0] * 3
        for key in keys:
            r = wordanalyze(dr, key, thr / 100.0, hl)
            resw = [sum(x) for x in zip(resw, r)]
        resnw = [0] * 3
        for key in nkeys:
            r = nonwordanalyze(dr, key, thr / 100.0, hl)
            resnw = [sum(x) for x in zip(resnw, r)]
        res = [thr / 100.0] + resw + resnw
        print(",".join(map(lambda f: str(f), res)))

__main__()
