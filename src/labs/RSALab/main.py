from functools import cached_property
from pathlib import Path
import random
import shutil
import string
import subprocess
import sys
import os
from Crypto.PublicKey import RSA

from fastapi import UploadFile
import zipfile

import rsa
from Crypto.Cipher import PKCS1_OAEP

from src.utils import Grade, LabTemplate, Lab, CLIHandler

# make sure you add pycryptodome!


def generateString(len):
    """Generate random string which will be what our "downloads" end up being in Q1files"""

    return "".join(random.choice(string.ascii_letters) for _ in range(len))


class PublicKey:
    e: int
    n: int


class PrivateKey:
    d: int
    n: int


def frombytes(bytes: bytes):
    """Internal function, should not be used

    Args:
        bytes (bytes): _description_

    Returns:
        _type_: _description_
    """
    return int.from_bytes(bytes, sys.byteorder)


def tobytes(_int: int):
    """Internal function, should not be used

    Args:
        bytes (bytes): _description_

    Returns:
        _type_: _description_
    """
    return _int.to_bytes((_int.bit_length() + 7) // 8, sys.byteorder)


class TextbookRSA:
    def __init__(self) -> None:
        pass

    def encrypt(text: bytes, key: PublicKey):
        """Encrypt a text with RSA. Requires a public key.

        Args:
            text (bytes): Text to encrypt
            key (PublicKey): Public key that will be used

        Returns:
            bytestring: byte string of our encrypted text.
        """
        return tobytes(pow(frombytes(text), key.e, key.n))

    def decrypt(text: bytes, key: PrivateKey):
        """Decrypt encrypted text

        Args:
            text (bytes): Byte string representing the encrypted text
            key (PublicKey): Private Key, used for decrypting the text

        Returns:
            bytestring: A bytestring representing the original, unencrypted text.
        """
        return tobytes(pow(frombytes(text), key.d, key.n))


keyPair = RSA.generate(2048)


class RSALabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 4
    # Used only when seeding for the first time
    seed_name: str = "Breaking textbook and weakly-padded RSA"
    seed_section: str = "Ch6"
    seed_short_description: str = (
        "In this lab users will learn about "
    )
    seed_long_description: str = "Lab 4 todo"
    seed_active: bool = True
    # Static dir
    static_dir: Path = Path(__file__).parent

    @staticmethod
    def _grade(submitted_solution: str, solution: str, file: UploadFile) -> Grade:
        """Grades a submissions

        Give 25% for each correct cert
        Submissions are supposed to be in the form of:
        0_1_2_3
        """

        solutions = solution.split('_')
        for i in range(len(solutions)):
            solutions[i] = solutions[i].split(";")
        files = zipfile.ZipFile(file.file)
        base_dir = files.filelist[0].filename
        feedback = ""

        score = 0

        # Question 1 
        q1_files = ["mx1a", "mx1b", "mx1c", "my1a", "my1b", "my1c"]
        for ind, foi in enumerate(q1_files):
            try:
                f = files.read(f"{base_dir}{foi}").decode("utf-8")

                if f == solutions[0][ind]:
                    score += 4
                else:
                    feedback = feedback + f"File {foi} is incorrect.\n"
            except KeyError:
                feedback = feedback + f"Missing {foi} from uploaded zip archive.\n"
        score+=score//24

        # Question 2 does not get graded

        # Question 3
        try:
            f = files.read(f"{base_dir}pair0-2.csv").decode("utf-8").split('\n')[1]
            if f == solutions[1][0]:
                score += 25
            else:
                feedback = feedback + f"File pair0-2.csv is incorrect.\n"
        except KeyError:
            feedback = feedback + f"Missing pair0-2.csv from uploaded zip archive.\n"

        # Question 4
        try:
            f = files.read(f"{base_dir}pair1-2.csv").decode("utf-8").split('\n')[1]
            if f == solutions[2][0]:
                score += 25
            else:
                feedback = feedback + f"File pair1-2.csv is incorrect.\n"
        except KeyError:
            feedback = feedback + f"Missing pair1-2.csv from uploaded zip archive.\n"
        
        # Question 5
        q5_files = ["pair2-2.csv", "pair3-2.csv", "pair4-2.csv", "pair5-2.csv"]
        q5_score = 0
        for ind, foi in enumerate(q5_files):
            try:
                f = files.read(f"{base_dir}{foi}").decode("utf-8").split('\n')[1]

                if f == solutions[3][ind]:
                    q5_score += 6
                else:
                    feedback = feedback + f"File {foi} is incorrect.\n"
            except KeyError:
                feedback = feedback + f"Missing {foi} from uploaded zip archive.\n"
        q5_score += q5_score//24
        score+=q5_score

        return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore

        random.seed(seed)
        solution1 = self.sec1()
        self.sec2()
        solution3, solution4, solution5 = self.sec3()

        solution = f'{solution1}_{solution3}_{solution4}_{solution5}'

        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )

    def sec1(self):
        labInput = self.temp_lab_dir / "lab-input"
        if not os.path.exists(labInput):
            os.mkdir(labInput)

        # we save the private decryption key to d1
        publicKey = keyPair.public_key()
        cx1Plain = generateString(25)
        cx2Plain = generateString(25)
        cipher = PKCS1_OAEP.new(publicKey, randfunc=random.randbytes)
        solution = ""

        with open(f"{labInput}/TextbookRSA.py", "w") as f:
            with open('main.py', 'r') as g:
                lines = g.readlines()
                f.write('import sys\n\n')
                for i in range(27, 88):
                    f.write(lines[i])

        # CX
        # part a is textbook rsa, part b is with PKCS1.5 and part C is OAEP
        with open(f"{labInput}/cx1a", "wb") as f:
            content = TextbookRSA.encrypt(bytes(cx1Plain, "utf-8"), publicKey)
            f.write(content)
            f.close()
            solution+=f"{cx1Plain};"

        with open(f"{labInput}/cx1b", "wb") as f:
            content = rsa.encrypt(bytes(cx1Plain, "utf-8"), publicKey)
            f.write(content)
            f.close()
            solution+=f"{cx1Plain};"

        with open(f"{labInput}/cx1c", "wb") as f:
            content = cipher.encrypt(bytes(cx1Plain, "utf-8"))
            f.write(content)
            f.close()
            solution+=f"{cx1Plain};"

        # CY
        with open(f"{labInput}/cy1a", "wb") as f:
            content = TextbookRSA.encrypt(bytes(cx2Plain, "utf-8"), publicKey)
            f.write(content)
            f.close()
            solution+=f"{cx2Plain};"

        with open(f"{labInput}/cy1b", "wb") as f:
            content = rsa.encrypt(bytes(cx2Plain, "utf-8"), publicKey)
            f.write(content)
            f.close()
            solution+=f"{cx2Plain};"

        with open(f"{labInput}/cy1c", "wb") as f:
            content = cipher.encrypt(bytes(cx2Plain, "utf-8"))
            f.write(content)
            f.close()
            solution+=f"{cx2Plain}"

        
        boooool = random.random() < 0.5
        with open(f"{labInput}/ma1", "w") as f:
            f.write(boooool and cx1Plain or generateString(25))
            f.close()

        with open(f"{labInput}/mb1", "w") as f:
            f.write(not boooool and cx2Plain or generateString(25))
            f.close()
        with open(f"{labInput}/d1", "wb") as f:
            f.write(keyPair.export_key())
            f.close()

        with open(f"{labInput}/e1", "wb") as f:
            f.write(keyPair.public_key().export_key())
            f.close()

        with open(f"{labInput}/n1", "w") as f:
            f.write(str(keyPair.n))
            f.close()

        return solution

    def sec2(self):
        pass

    def sec3(self):
        solution3 = ""
        solution4 = ""
        solution5 = ""

        labInput = self.temp_lab_dir / "lab-input"

        if not os.path.exists(labInput):
            os.mkdir(labInput)

        cipherDir = labInput / "ciphertexts"
        if not os.path.exists(cipherDir):
            os.mkdir(cipherDir)
        else:
            shutil.rmtree(cipherDir, ignore_errors=True)
            os.mkdir(cipherDir)

        plainDir = labInput / "plaintexts"
        if not os.path.exists(plainDir):
            os.mkdir(plainDir)
        else:
            shutil.rmtree(plainDir, ignore_errors=True)
            os.mkdir(plainDir)

        # for this question we are required to use TEXTBOOK rsa encryption. Different from the previous warmup questions.
        # keyPair = RSA.generate(2048)  # easy key gen
        # this is our textbook encryption thing
        publicKey = rsa.PublicKey(keyPair.n, keyPair.e)
        # publicKey = keyPair.public_key() # the commented section is for OAEP, we do not use this in this question.
        # cipher = PKCS1_OAEP.new(publicKey)

        # the difference between OAEP and PKCS #1.5 is that OAEP is an "all or nothing" encryption scheme. Every bit of the encrypted message needs to be valid for the original message to be recovered
        # in PKCS 1.5, the deciphering is still recoverable if some random bits are changed... tldr; insecure

        # rsa.encrypt()  # rsa.encrypt uses PKCS #1.5 which is what we want

        # No overlapping numbers, well mostly no overlapping numbers
        cipherRange = [val for val in range(100)]
        plaintextRange = [val for val in range(100)]
        random.shuffle(cipherRange)
        random.shuffle(plaintextRange)

        plaintextcsvFile = "Plaintext\n"
        ciphetextcsvFile = "Ciphertext\n"

        # this is for question 3
        matching_pair_3 = (-1, -1)
        # this is for question 4
        matching_pair_4 = (-1, -1)
        # the following are for question 5
        matching_pair_5 = (-1, -1) #  8 random bits
        matching_pair_6 = (-1, -1) # 12 random bits
        matching_pair_7 = (-1, -1) # 16 random bits
        matching_pair_8 = (-1, -1) # 20 random bits
        

        for i in range(100):

            ciphername = str(100 + cipherRange.pop())
            plainname = str(700 + plaintextRange.pop())
            # add a and b
            plaintextcsvFile += f"plaintext {plainname}.txt\n"
            ciphetextcsvFile += f"ciphertext {ciphername}.txt\n"
            ############################ QUESTION 3 ############################
            if i == 0 or i == 1:
                # just to make sure we don't have any collisions
                para = generateString(25) + str(random.randint(0, 100000000))
                with open(f"{plainDir}/plaintext {plainname}.txt", "w") as f:
                    f.write(para)
                    f.close()

                with open(f"{cipherDir}/ciphertext {ciphername}.txt", "wb") as f:
                    f.write(TextbookRSA.encrypt(bytes(para, "utf-8"), publicKey))
                    f.close()
                matching_pair_3 = (ciphername, plainname)
                if i == 0:
                    solution3 += f"plaintext {matching_pair_3[1]}.txt,ciphertext {matching_pair_3[0]}.txt"
                continue

            ############################ QUESTION 4 ############################
            if i == 2 or i == 3:
                # add the padding, one 02 byte, one random byte, and then the message
                fully = generateString(25) + str(random.randint(0, 100))
                
                what = random.randint(0,15)
                what = what << 4
                rByte = chr(what)
                
                para = (b"\x02".decode() +rByte)+fully

                with open(f"{plainDir}/plaintext {plainname}.txt", "w") as f:
                    f.write(fully)
                    f.close()

                with open(f"{cipherDir}/ciphertext {ciphername}.txt", "wb") as f:
                    f.write(TextbookRSA.encrypt(para.encode("utf-8"), publicKey))
                    f.close()
                matching_pair_4 = (ciphername, plainname)
                if i == 2:
                    solution4 += f'plaintext {matching_pair_4[1]}.txt,ciphertext {matching_pair_4[0]}.txt'
                continue

            ############################ QUESTION 5 ############################
            if i == 4 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9 or i == 10 or i == 11:
                # add the padding: one 02 byte, random string , and then the message
                fully = bytes(generateString(25) + str(random.randint(0, 100)), "utf-8")
                
                what = ""
                if i == 4 or i == 5:
                    # 8 random bits for padding
                    what = chr(random.randint(0, 255))
            
                    matching_pair_5 = (ciphername, plainname)
                    if i == 4:
                        solution5 += f'plaintext {matching_pair_5[1]}.txt,ciphertext {matching_pair_5[0]}.txt;'

                if i == 6 or i == 7:
                    # 12 random bits followed by four zero bits for padding
                    what = chr(random.randint(0, 255)) + chr(random.randint(0,15) << 4)
                                    # 8 bits                 # 4 bits             # 4 zero bits
                    matching_pair_6 = (ciphername, plainname)
                    if i == 6:
                        solution5 += f'plaintext {matching_pair_6[1]}.txt,ciphertext {matching_pair_6[0]}.txt;'

                if i == 8 or i == 9:
                    # 16 random bits for padding
                    what = chr(random.randint(0, 255)) + chr(random.randint(0, 255))

                    matching_pair_7 = (ciphername, plainname)
                    if i == 8:
                        solution5 += f'plaintext {matching_pair_7[1]}.txt,ciphertext {matching_pair_7[0]}.txt;'

                if i == 10 or i == 11:
                    # 20 random bits followed by four zero bits for padding
                    what = chr(random.randint(0, 255)) + chr(random.randint(0, 255)) + chr(random.randint(0,15) << 4)
            
                    matching_pair_8 = (ciphername, plainname)
                    if i == 10:
                        solution5 += f'plaintext {matching_pair_8[1]}.txt,ciphertext {matching_pair_8[0]}.txt;'

                # same starting byte as question 4
                para = (b"\x02" + bytes(what, "utf-8"))+fully
    
                with open(f"{plainDir}/plaintext {plainname}.txt", "wb") as f:
                    f.write(fully)
                    f.close()

                with open(f"{cipherDir}/ciphertext {ciphername}.txt", "wb") as f:
                    f.write(TextbookRSA.encrypt(para, publicKey))
                    f.close()
                continue
            #####################################################################
            random1 = generateString(25) + str(random.randint(0, 100000000))
            random2 = generateString(25) + str(random.randint(0, 100000000))
            with open(f"{plainDir}/plaintext {plainname}.txt", "w") as f:
                f.write(random1)
                f.close()

            with open(f"{cipherDir}/ciphertext {ciphername}.txt", "wb") as f:
                # this is for PKCS #1.5
                f.write(rsa.encrypt(random2.encode("utf-8"), publicKey))
                f.close()

        with (open(f"{labInput}/pair0-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_3[1]}.txt,ciphertext {matching_pair_3[0]}.txt")
            f.close()
        with (open(f"{labInput}/pair1-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_4[1]}.txt,ciphertext {matching_pair_4[0]}.txt")
            f.close()
        with (open(f"{labInput}/pair2-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_5[1]}.txt,ciphertext {matching_pair_5[0]}.txt")
            f.close()
        with (open(f"{labInput}/pair3-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_6[1]}.txt,ciphertext {matching_pair_6[0]}.txt")
            f.close()
        with (open(f"{labInput}/pair4-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_7[1]}.txt,ciphertext {matching_pair_7[0]}.txt")
            f.close()
        with (open(f"{labInput}/pair5-1.csv", "w")) as f:
            f.write(
                f"Plaintext,Ciphertext\nplaintext {matching_pair_8[1]}.txt,ciphertext {matching_pair_8[0]}.txt")
            f.close()

        with (open(f"{labInput}/ciphertexts.csv", "w")) as f:
            f.write(ciphetextcsvFile)
            f.close()

        with (open(f"{labInput}/plaintexts.csv", "w")) as f:
            f.write(plaintextcsvFile)
            f.close()

        return solution3, solution4, solution5

class spoof:
    def __init__(self, f) -> None:
        self.file = f
        pass

def main(args: list[str]):
    args.pop(0)
    
    cmd = args[0]
    settings = CLIHandler.handle(args)
    ## ============================================================ ##
    if len(args) == 0:
        print("No arguments specified, defaulting to new lab gen...")
        RSALabTemplate(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        RSALabTemplate(generated_dir=settings.destination).generate_lab()
    elif cmd == "grade":
        destination = (settings.input is not None) and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = RSALabTemplate().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        a = shutil.make_archive(
            base_name="temp_solutions",  # Name of the archive
            format='zip',            # Format of the archive ('zip', 'tar', 'gztar', 'bztar', 'xztar')
            root_dir=Path(destination).parent,     # Root directory to archive
            base_dir=Path(destination).name,           # Base directory to be archived; use None to archive the entire root_dir
            verbose=True             # Print status messages to stdout (optional)
        )
        with open(a, "rb") as f:
            results= RSALabTemplate().grade("", template, spoof(f))
            print(f'Score:\n{results.score}\nFeedback:\n{results.feedback}')
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
