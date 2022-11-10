def text2byte(text):
    byte_array = bytearray()
    for c in text:
        byte_array.append(ord(c))
    return byte_array


def byte2text(byte_array):
    text = ''
    for byte in byte_array:
        text += (chr(byte))
    return text
