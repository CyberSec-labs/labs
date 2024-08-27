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

from src.utils import Grade, LabTemplate, Lab, CLIHandler


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
        """
        # section 1

        score = 0
        solutions = solution.split("_")
        files = zipfile.ZipFile(file.file)
        base_dir = files.filelist[0].filename
        feedback = ""

        # section 1
        try:
            f = files.read(f"{base_dir}solution_1.txt").decode('utf-8')

            if f == solutions[0]:
                score += 25
            else:
                feedback = feedback + "Question 1 solution is incorrect.\n"
        except KeyError:
            feedback = feedback + "Missing solution_1.txt from uploaded zip archive.\n"

        # section 2
        """"""
        expectedFiles = solutions[1].split(".")
        correct = 0
        incorrect = 0 
        q2_sols = len(expectedFiles)
        # Makes sure the only files submitted for q2 are the correct ones
        for num in range(10):
            try:
                f = files.read(f"{base_dir}{num}.txt")
            except:
                continue
            if str(num) in expectedFiles:
                correct += 1
            else:
                incorrect += 1
        
        if correct == q2_sols and incorrect == 0:
            score += 75
        else:
            feedback = feedback + f"Question 2 solution is incorrect.\n"
        
        """"""

        return Grade(score=int(score), feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore

        random.seed(seed)

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
            file_1.write(fileContents.encode("utf-8"))
            if i in isTrue:  # if the file sig will match, calculate file signature
                signed = signer.sign(hasher)
                file_2.write(signed)
                qSolution = qSolution + f"{i}."
            else:
                file_2.write(
                    random.randbytes(256)
                )  # if we want the file sig to not match we just generate random bytes instead
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
        for i in range(100_000, 1_100_000, 100_000):
            bytez = random.getrandbits(i * 8).to_bytes(i, "little")
            with open(f"{self.temp_lab_dir}/Q3files/inputs/{a}00k.txt", "w+b") as f:
                f.write(bytez)
                f.close()
            a = a + 1

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
        DownloadLab(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        DownloadLab(generated_dir=settings.destination).generate_lab()
    elif cmd == "grade":
        destination = (settings.input is not None) and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = DownloadLab().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        a = shutil.make_archive(
            base_name="temp_solutions",  # Name of the archive
            format='zip',            # Format of the archive ('zip', 'tar', 'gztar', 'bztar', 'xztar')
            root_dir=Path(destination).parent,     # Root directory to archive
            base_dir=Path(destination).name,           # Base directory to be archived; use None to archive the entire root_dir
            verbose=True             # Print status messages to stdout (optional)
        )
        with open(a, "rb") as f:
            results = DownloadLab().grade("", template, spoof(f))
            print(f'Score:\n{results.score}\nFeedback:\n{results.feedback}')
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
