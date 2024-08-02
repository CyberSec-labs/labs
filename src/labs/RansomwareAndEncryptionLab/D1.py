import random
import sys
from os import remove
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


def processFile(path):
    # TODO: Take path as input
    #       Create necessary cipher(s)
    #       Decrypt data in text file
    #       Remove token
    #       Done
    pass


def main(args):
    cmdArgs = args[1::]
    cmdArgLen = len(cmdArgs)
    if cmdArgLen < 1:
        print("usage: ./D1.py [input file]")
        return

    processFile(cmdArgs[0])


if __name__ == "__main__":
    main(sys.argv)