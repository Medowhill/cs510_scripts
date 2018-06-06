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

def wordanalyze(dr, key, th1, th2, thb):
    BU = 0
    TP = 0
    linesl, linesh = getLines2(dr, key)
    total = int(len(linesl) / 4)
    for i in range(total):
        kl, sl = lineToKS(linesl[i * 4 + 2], linesl[i * 4 + 3])
        kh, sh = lineToKS(linesh[i * 4 + 2], linesh[i * 4 + 3])
        if kl != "_unknown_" and kl != "_silence_":
            if th1 <= sl and sl < th2:
                BU += 1
                if thb <= sh and kh == key:
                    TP += 1
            elif th2 <= sl:
                TP += 1
    return [total, BU, TP]

def nonwordanalyze(dr, key, th1, th2, thb):
    BU = 0
    TN = 0
    linesl, linesh = getLines2(dr, key)
    total = int(len(linesl) / 4)
    for i in range(total):
        kl, sl = lineToKS(linesl[i * 4 + 2], linesl[i * 4 + 3])
        kh, sh = lineToKS(linesh[i * 4 + 2], linesh[i * 4 + 3])
        if kl != "_unknown_" and kl != "_silence_":
            if th1 <= sl and sl < th2:
                BU += 1
                if sh < thb or kh == "_unknown_" or kh == "_silence_":
                    TN += 1
            elif sl < th1:
                TN += 1
        else:
            TN += 1
    return [total, BU, TN]

def printResult(dic, f):
    print("th1/th2," + ",".join(map(lambda i: str(i / 100), list(range(55, 100, 5)))))
    for th1 in range(50, 100, 5):
        print(th1 / 100, end=",")
        for th2 in range(55, 105, 5):
            if (th1, th2) in dic:
                l = dic[(th1, th2)]
                print(f(l), end=",")
            else:
                print("", end=",")
        print()

def __main__():
    assert(len(sys.argv) == 2)

    keys = ["on", "right", "stop", "yes"]
    nkeys = ["dog", "one"]
    
    dr = sys.argv[1]
    
    dic = {}
    print(",".join(["Threshold", "Total(word)", "TP", "FN", "Total(nonword)", "TN", "FP"]))
    for th1 in range(50, 100, 5):
        for th2 in range(th1 + 5, 105, 5):
            resw = [0] * 3
            for key in keys:
                r = wordanalyze(dr, key, th1 / 100.0, th2 / 100.0, 0.7)
                resw = [sum(x) for x in zip(resw, r)]
            resnw = [0] * 3
            for key in nkeys:
                r = nonwordanalyze(dr, key, th1 / 100.0, th2 / 100.0, 0.7)
                resnw = [sum(x) for x in zip(resnw, r)]
            dic[(th1, th2)] = resw + resnw

    print("TP")
    printResult(dic, lambda l: l[2] / l[0])
    print("BU - Hotword")
    printResult(dic, lambda l: l[1] / l[0])
    print("TN")
    printResult(dic, lambda l: l[5] / l[3])
    print("BU - Hotword")
    printResult(dic, lambda l: l[4] / l[3])

__main__()
