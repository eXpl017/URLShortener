import string

BASE62 = tuple(string.digits + string.ascii_letters)
B62_POS = dict((e,i) for i,e in enumerate(BASE62))

def b62_encode(num):
    if not num: return BASE62[0]
    encoded = ''
    while num:
        num, rem = divmod(num, 62)
        encoded = BASE62[rem] + encoded
    return encoded

def b62_decode(string):

    decoded = 0
    for i,e in enumerate(string[::-1]):
        decoded += (62 ** i) * B62_POS[e]
    return decoded
