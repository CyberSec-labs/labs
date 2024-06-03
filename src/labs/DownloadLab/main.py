from functools import cached_property
from hashlib import sha256
import os
from pathlib import Path
import random
import shutil
import string
import subprocess
import sys
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from fastapi import UploadFile
import zipfile
import rsa

from utils import Grade, LabTemplate, Lab


def generateString(len):
    """Generate random string which will be what our "downloads" end up being in Q1files"""
    return "".join(random.choice(string.ascii_letters) for _ in range(len))


class DownloadLab(LabTemplate):
    # DB properties
    lab_template_id: int = 1
    # Used only when seeding for the first time
    seed_name: str = "Download Lab"
    seed_section: str = "Ch1"
    seed_short_description: str = "Add short seed description"
    seed_long_description: str = "Add short seed description"
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
        # section 1

        score = 0
        solutions = solution.split("_")
        files = zipfile.ZipFile(file.file)
        base_dir = files.filelist[0].filename
        feedback = ""

        # section 1
        try:
            f = files.read(f"{base_dir}/solution_1.txt")

            if f == solutions[0]:
                score = 25
            else:
                feedback = feedback + "Question 1 solution is incorrect."
        except KeyError:
            feedback = feedback + "Missing solution_1.txt from uploaded zip archive.\n"

        # section 2
        """"""
        expectedFiles = solution[1].split(".")
        correct = 0 
        list = 0
        for name in expectedFiles:
            list = list + 1
            try:
                f = files.read(f"{base_dir}/{name}")
                correct = correct + 1
            except:
                pass
        
        if list != correct:
            feedback = feedback + f"{abs(list - correct)} are incorrect.\n"
        else:
            feedback = feedback + f"Question 2 correct.\n"
        """"""

        return Grade(score=score, feedback="na")

    def generate_lab(self, *, user_id: int = 0, seed: str = "", debug: bool = False) -> Lab:  # type: ignore
        q1Solution = self.sec1()
        q2Solution = self.sec2()
        self.sec3()

        solution = f"{q1Solution}_{q2Solution}"
        # Copy the question folder into the directory that will be given to users
        self._copy_q_dir_into_lab_generated_dir()
        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )

    def sec1(self):
        if not os.path.exists(f"{self.temp_lab_dir}/Q1files"):
            os.mkdir(f"{self.temp_lab_dir}/Q1files")

        hashedFileKey = random.randrange(0, 10)

        for i in range(10):
            file = open(f"{self.temp_lab_dir}/Q1files/{i}.txt", "w+")
            # get a string to put for our file
            fileContents = generateString(25)
            if i == hashedFileKey:
                fileHash = SHA256.new()
                fileHash.update(
                    fileContents.encode("utf-8")
                )  # get the hash of our file

                Q1Hash = open(
                    f"{self.temp_lab_dir}/Q1files/Q1.hash", "w+b"
                )  # write our hash file in binary
                Q1Hash.write(fileHash.digest())  # write hash to Q1.hash
                Q1Hash.close()  # close

            file.write(fileContents)

            file.close()
        return str(hashedFileKey) + ".txt"

    def sec2(self):
        if not os.path.exists(f"{self.temp_lab_dir}/Q2files"):
            os.mkdir(f"{self.temp_lab_dir}/Q2files")
        key = RSA.generate(2048)
        public = key.public_key()
        signer = pkcs1_15.new(key)

        with open(f"{self.temp_lab_dir}/Q2files/Q2pk.pem", "w+b") as f:
            f.write(public.export_key())
            f.close()
        qSolution = ""
        possible = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(possible)
        isTrue = possible[:5]
        for i in range(10):
            file_1 = open(f"{self.temp_lab_dir}/Q2files/{i}.txt", "w+b")
            file_2 = open(f"{self.temp_lab_dir}/Q2files/{i}_sig.txt", "w+b")

            # get a string to put for our file
            fileContents = generateString(25)
            hasher = SHA256.new(fileContents.encode("utf-8"))
            file_1.write(hasher.digest())
            if i in isTrue:  # if the file sig will match, calculate file signature
                signed = signer.sign(hasher)
                file_2.write(signed)
                qSolution = qSolution + f"{i}."
            else:
                file_2.write(
                    random.randbytes(256)
                )  # if we want the file sig to not match we just generate random bytes instead
        print("ok" + qSolution[:-1])
        return qSolution[:-1]

    def sec3(self):
        # remember to reorder a, b, c, and d.
        # validate that the key pairs generated in b match
        # for c we want to change that so that they first try to sign raw text (digest it in blocks), and then do a hash then sign

        # part A, no input files needed

        # we need to generate several input lengths
        if not os.path.exists(f"{self.temp_lab_dir}/Q3files"):
            os.mkdir(f"{self.temp_lab_dir}/Q3files")
        if not os.path.exists(f"{self.temp_lab_dir}/Q3files/inputs"):
            os.mkdir(f"{self.temp_lab_dir}/Q3files/inputs")

        a = 1
        for i in range(100_000, 1_000_000, 100_000):
            bytez = random.getrandbits(i * 8).to_bytes(i, "little")
            with open(f"{self.temp_lab_dir}/Q3files/inputs/{a}.txt", "w+b") as f:
                f.write(bytez)
                f.close()
            a = a + 1
        pass

class spoof:
    def __init__(self, f) -> None:
        self.file = f
        pass

def main(args: list[str]):
    args.pop(0)
    if len(args) == 0:
        print("No arguments specified, defaulting to new lab gen...")
        DownloadLab().generate_lab()
        return
    
    cmd = args[0]

    if cmd == "gen":
        DownloadLab().generate_lab()
    elif cmd == "grade":
        destination = len(args) > 1 and args[1] or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = DownloadLab().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        shutil.make_archive("temp_solutions", 'zip', base_dir=destination, root_dir=os.getcwd())
        with open(toDelete, "rb") as f:
            print(DownloadLab().grade("", template, spoof(f)))
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
