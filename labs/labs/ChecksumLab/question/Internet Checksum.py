def getValue(input):
    sum = 0
    length = len(input)
    for i in range(0, length, 2):
        if i + 1 > length - 1:
            sum += ord(input[i: i + 1])
        else:
            word = (ord(input[i: i + 1]) << 8) + ord(input[i + 1: i + 2])
            sum += word

    return sum


def xorStr(input):
    r = []
    for a in input:
        r.append(str(int(a) ^ 1))

    return "".join(r)


def toInternetChecksum(s):
    return bin(getValue(s))[2:]
