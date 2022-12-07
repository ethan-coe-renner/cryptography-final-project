def text2byte(text):
    byte_array = bytearray()
    for c in text:
        byte_array.append(ord(c))
    return byte_array


def chunkGen(byte_array):
    chunk = []
    byte_array.reverse()
    while (len(byte_array) > 8):
        last = byte_array[-8:]
        chunk.append(last)
        byte_array = byte_array[:len(byte_array) - 8]
    diff = 8 - len(byte_array)
    for i in range(0, diff):
        byte_array.insert(0, 0)
    chunk.append(byte_array)
    return chunk


def byte2text(byte_array):
    text = ''
    for byte in byte_array:
        text += (chr(byte))
    return text


def text2chunk(input):
    n = len(input);
    u8array = []
    while len(input)%8 != 0:
        input += '_'

    for i in range(0, n/8):
        b = bytearray()
        s = input[i*8:i*8+8]
        b.extend(s.encode('utf-8'))
        u8array.append(b)
    return u8array


def bytes2chunk(input):
    u64chunkArray = []
    buffer = 0
    shift = 0
    for byte in input:
        buffer = buffer + (byte << shift)
        shift = shift + 8
        if shift == 64:
            shift = 0
            u64chunkArray.append(buffer)
            buffer = 0
    if buffer > 0:
        u64chunkArray.append(buffer)
    return u64chunkArray


def chunks2text(u64chunkArray):
    word = []
    str = ''
    for chunk in u64chunkArray:
        while chunk != 0:
            word.append(chunk % 2**8)
            chunk >>= 8
    for byte in word:
        char = chr(byte)
        str = str + char
    return str


def text2chunk(string):
    return bytes2chunk(text2byte(string))


if __name__ == "__main__":
    counter = 0
    x = text2byte("hello world")
    print(x[0])
    chunk = bytes2chunk(x)
    print(chunks2text(chunk))
    #y = chunkGen(x)
    #print("chunkList: ", y)
    #print(text2chunk(y))
            #value of the ASCII * 2^(i*8)