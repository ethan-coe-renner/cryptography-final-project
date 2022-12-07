import random

from TextBites import text2chunk

p1 = [56, 48, 40, 32, 24, 16,  8,
		  0, 57, 49, 41, 33, 25, 17,
		  9,  1, 58, 50, 42, 34, 26,
		 18, 10,  2, 59, 51, 43, 35,
		 62, 54, 46, 38, 30, 22, 14,
		  6, 61, 53, 45, 37, 29, 21,
		 13,  5, 60, 52, 44, 36, 28,
		 20, 12,  4, 27, 19, 11,  3
	]

cd_leftshifts = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]
p2 = [
		13, 16, 10, 23,  0,  4,
		 2, 27, 14,  5, 20,  9,
		22, 18, 11,  3, 25,  7,
		15,  6, 26, 19, 12,  1,
		40, 51, 30, 36, 46, 54,
		29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52,
		45, 41, 49, 35, 28, 31
	]

# initial permutation IP
ip = [57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8,  0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6
]

E = [
		31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
	]

# The (in)famous S-boxes
sb = [
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    # S8
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

# 32-bit permutation function P used on the output of the S-boxes
sboxOutput = [
    15, 6, 19, 20, 28, 11,
    27, 16, 0, 14, 22, 25,
    4, 17, 30, 9, 1, 7,
    23,13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10,
    3, 24
]

# final permutation IP^-1
finalpermute = [
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
    32,  0, 40,  8, 48, 16, 56, 24
]

def permute(bitstring, arr):
    result = ""
    for i in range(0, len(arr)):
        result = result + bitstring[arr[i]]
    return result


def generateSubKeys(k_64):
    k_56 = permute(k_64, p1)
    # print(k_64)
    # print(k_56)

    c = [k_56[0:28]]
    d = [k_56[28:56]]
    # print("c0: "+c[0] + "\td0: "+d[0])
    for i in range(16):
        c_i = c[i]
        d_i = d[i]

        for j in range(cd_leftshifts[i]):
            c_i = c_i[1:28] + c_i[0]
            d_i = d_i[1:28] + d_i[0]

        c.append(c_i)
        d.append(d_i)
        # print("c" + str(i+1) + ": "+c[i+1] + "\td" + str(i+1) + ": "+d[i+1])

    # print("\nKeys: ")
    subkeys = []
    for i in range(1,17):
        subkeys.append(permute(c[i]+d[i], p2))
        # print("k" + str(i) + ": "+subkeys[i-1])
    return subkeys


def chunkMessage(msg):
    while len(msg)%8 !=0:
        msg += " "

    chunks = []

    while len(msg) > 0:
        s = msg[0:8]
        msg = msg[8:]
        chunks.append(''.join(format(ord(i), '08b') for i in s))
    return chunks


def chunkToString(chunk):
    msg = ""
    for i in range(8):
        string = int(chunk[i*8:i*8+8], 2)
        msg += chr(string)
    return msg


def sBox(iteration, sixbit):
    row = int(sixbit[0]+sixbit[5], 2)
    column = int(sixbit[1:5], 2)
    index = row*16+column
    return "{:04b}".format(sb[iteration][index])


def func(R, subkey):
    R = permute(R, E)
    xorR = ""
    result = ""
    for i in range(len(R)):
        if R[i] == subkey[i]:
            xorR += "0"
        else:
            xorR += "1"

    count = 0
    while len(xorR) > 0:
        result += sBox(count, xorR[0:6])
        xorR = xorR[6:]
        count += 1

    result = permute(result, sboxOutput)

    return result


def desEncode(chunk,subkeys):
    chunk = permute(chunk, ip)
    #print('IP: '+ chunk)
    L = chunk[:32]
    R = chunk[32:]
    #print("L"+str(0)+": " + L)
    #print("R"+str(0)+": " + R)

    for i in range(16):
        newL = R
        funkyR = func(R, subkeys[i])
        newR = ""
        for k in range(len(funkyR)):
            if funkyR[k] == L[k]:
                newR += "0"
            else:
                newR += "1"

        L = newL
        R = newR
        #print("Subkey: "+subkeys[i])
        #print("L"+str(i+1)+": " + L)
        #print("R"+str(i+1)+": " + R)

    return permute(R+L, finalpermute)


def main():
    #k_64 = input("Enter binary key: ").replace(" ", "")
    random.seed();
    k_64 = ""
    for i in range(64):
        if random.randint(0,2) == 0:
            k_64 += "0"
        else:
            k_64 += "1"

    subkeys = generateSubKeys(k_64)
    chunks = chunkMessage(input("Enter a message here: "))
    print()
    print("Plaintext message:")
    print(chunks)
    print()
    e = []
    for c in chunks:
        encoded_msg = desEncode(c, subkeys)
        e.append(encoded_msg)
    print("Encoded Message: ")
    print(e)
    print()

    s = ""
    for es in e:
        s += chunkToString(desEncode(es, subkeys[::-1]))
    s.strip()
    print("Decrypted Message:")
    print(s)


if __name__ == "__main__":
    main()