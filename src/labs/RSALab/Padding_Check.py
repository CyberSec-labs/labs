from Crypto.PublicKey import RSA
from TextbookRSA import TextbookRSA, tobytes
import sys
sys.byteorder='big'

x = int(00)

key = RSA.import_key(tobytes(x))

cipher = tobytes(int(sys.argv[1]))

try: 
    plain = TextbookRSA.decrypt(cipher, key)
    print(plain[:1] == b'\x02')
except KeyboardInterrupt as e:
    print(e)
