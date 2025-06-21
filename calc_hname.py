import hashlib
import base64
import xxhash
from sys import argv

def calc_hname(checksum, size, name):
    name = name.encode("utf8")
    a = bytearray(16)

    for i in range(8):
        a[i] = (checksum >> ((7 - i) * 8)) & 0xFF

    for i in range(8):
        a[i+8] = (size >> ((7 - i) * 8)) & 0xFF

    data = a + name
    digest = hashlib.sha1(data).digest()
    return base64.b32encode(digest).decode('utf8')

def main():
    (file_path, name) = argv[1:]
    data = open(file_path, "rb").read()
    checksum = xxhash.xxh64(data).intdigest()
    print(calc_hname(checksum, len(data), name))

main()