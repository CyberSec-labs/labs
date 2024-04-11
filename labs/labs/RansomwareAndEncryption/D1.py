import random
import sys
from os import remove
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES


def processFile(path, seed):
    random.seed(seed)
    cipher = AES.new(random.randbytes(32), AES.MODE_CBC)
    with open(f"{path}", "r+b") as f:
        contents = f.read()

        encrypted = cipher.decrypt(unpad(contents, AES.block_size))
        f.seek(0)
        f.write(encrypted)

    remove(f"{path}.TOKEN")


def main(args):
    cmdArgs = args[1::]
    cmdArgLen = len(cmdArgs)
    print(cmdArgs, cmdArgLen)
    if cmdArgLen < 1:
        print("usage: ./D1.py [input file] [key]")
        return

    processFile(cmdArgs[0])


if __name__ == "__main__":
    main(sys.argv)

# todo:
# take decrypted seed as input with file name
# decrypt file using seed
# remove junk
# done
