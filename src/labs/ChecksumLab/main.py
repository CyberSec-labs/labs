from functools import cached_property
import os
from pathlib import Path
import random
import shutil
import string
import subprocess
import sys
import zipfile
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from fastapi import UploadFile
# from utils import Grade, LabTemplate, Lab
from src.utils import Grade, LabTemplate, Lab, CLIHandler
import io



def generateString(len):
    """Generate random string which will be what our "downloads" end up being in Q1files"""

    return "".join(random.choice(string.ascii_letters) for _ in range(len))


def getValue(input):
    sum = 0
    length = len(input)
    for i in range(0, length, 2):
        if i + 1 > length - 1:
            sum += ord(input[i : i + 1])
        else:
            word = (ord(input[i : i + 1]) << 8) + ord(input[i + 1 : i + 2])
            sum += word

    return sum


def xorStr(input):
    r = []
    for a in input:
        r.append(str(int(a) ^ 1))

    return "".join(r)


def toInternetChecksum(s):
    return bin(getValue(s))[2:]


def checkInternetChecksum(input, check):
    o = bin(int(check, 2) + input)[2:]
    for a in o:
        if a == "0":
            return False
    return True


class Lab3LabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 3
    # Used only when seeding for the first time
    seed_name: str = "Integrity Lab"
    seed_section: str = "Ch3"
    seed_short_description: str = "In this lab users will learn about "
    seed_long_description: str = "Lab 2 todo"
    seed_active: bool = True
    # Static dir
    static_dir: Path = Path(__file__).parent

    @staticmethod
    def _grade(submitted_solution: str, solution: str, file: UploadFile) -> Grade:
        """Grades a submissions"""

        score = 0
        solutions = solution.split("_")
        files = zipfile.ZipFile(file.file)
        base_dir = files.filelist[0].filename
        feedback = ""

        # for question 1
        try:
            f = files.read(f"{base_dir}h1b.txt").decode('utf-8')

            if f == solutions[0]:
                score = 25
            else:
                feedback = feedback + "Question 1 solution is incorrect.\n"
        except KeyError:
            feedback = feedback + "Missing h1b.txt from uploaded zip archive.\n"

        # for question 2
        try:
            f2b = files.read(f"{base_dir}f2b.txt").decode('utf-8')
            submittedHash = files.read(f"{base_dir}h2.txt").decode('utf-8')
            sol2 = solutions[1]

            temp = sol2.split("|\0\1|")
            hash = temp[0]
            f2acontents = temp[1]

            if submittedHash == hash:
                if f2acontents != f2b:
                    score = score + 25
                else:
                    feedback = (
                        feedback
                        + "Submitted file f2b.txt is the same as the given file f2a.txt\n"
                    )
            else:
                feedback = feedback + "Hash does not match expected input\n"

        except KeyError:
            feedback = (
                feedback + "Missing f2b.txt or h2.txt from uploaded zip archive.\n"
            )

        # for question 3
        try:
            with io.TextIOWrapper(files.open(f"{base_dir}f3b.txt"), encoding="utf-8") as f:
                f = f.read()
            sol3 = solutions[2]
            split = sol3.split("|\0\1|")
            if toInternetChecksum(f) == split[2]:
                if (f.find(f'Do not change this line: {split[0]}')!=-1) and (f.find(f'Do not change this line: {split[1]}')!=-1):
                    if f.find("replace this with your matching string") == -1:
                        score = score + 25
                    else:
                        feedback = feedback + "No modification detected.\n"
                else:
                    feedback += "Unauthorized modification made to line 1 or 3 in question 3.\n"
            else:
                feedback = (
                    feedback + "Question 3 solution is incorrect. Hash does not match\n"
                )
        except KeyError:
            feedback = feedback + "Missing f3b.txt from uploaded zip archive.\n"

        # question 4
        try:
            with io.TextIOWrapper(files.open(f"{base_dir}f4b.html"), encoding="utf-8") as f:
                f = f.read()
            sol4 = solutions[3]
            split = sol4.split("|\0\1|")
            checkIfExists = split[0]
            shouldMatch = split[1]
            if toInternetChecksum(f) == shouldMatch:
                if f.find(checkIfExists) == -1:
                    score = score + 25
                else:
                    feedback = feedback + "No modification to f4b.html present.\n"
            else:
                feedback = (
                    feedback + "Question 4 solution is incorrect. Hash does not match\n"
                )
        except KeyError:
            feedback = feedback + "Missing f4b.html from uploaded zip archive.\n"

        return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore
        random.seed(seed)

        for i in range(4):
            if not os.path.exists(f"{self.temp_lab_dir}/q{i + 1}"):
                os.mkdir(f"{self.temp_lab_dir}/q{i + 1}")

        solution = self.sec1()
        solution = solution + "_" + self.sec2()
        solution = solution + "_" + self.sec3()
        solution = solution + "_" + self.sec4()

        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )

    def sec1(self):
        f1a = open(f"{self.temp_lab_dir}/q1/f1a.txt", "w+")
        h1a = open(f"{self.temp_lab_dir}/q1/h1a.txt", "w+")
        f1b = open(f"{self.temp_lab_dir}/q1/f1b.txt", "w+")
        h1b = open(f"{self.temp_lab_dir}/q1/h1b.txt", "w+")

        # generate a random string to fill f1a.txt, then we check what the internet checksum hash for this would be
        f1aContents = generateString(25)
        # f1hash = binascii.crc32(bytes(f1aContents, "utf8"))
        f1hash = toInternetChecksum(f1aContents)

        # generate another random string for the file b's contents. Don't calculate the hash since it's uneeded, we can check later on submission
        f1bContents = generateString(30)
        # write all our contents and close files.
        f1a.write(f1aContents)
        h1a.write(str(f1hash))
        f1b.write(f1bContents)
        f1a.close()
        f1b.close()
        h1a.close()
        h1b.close()

        return toInternetChecksum(
            f1bContents
        )  # our expected input file will be h1b's internet checksum.

    def sec2(self):
        # create required files
        f2a = open(f"{self.temp_lab_dir}/q2/f2a.txt", "w")
        f2b = open(f"{self.temp_lab_dir}/q2/f2b.txt", "w")
        h2 = open(f"{self.temp_lab_dir}/q2/h2.txt", "w")

        f2aContents = generateString(25)
        # write to them
        f2a.write(f2aContents)
        f2b.write(
            "replace this file contents with a different string that has the same checksum as f2a.txt"
        )
        h2.write(
            "replace this file contents with the matching checksum value of both files"
        )

        # close everything
        f2a.close()
        f2b.close()
        h2.close()

        return toInternetChecksum(f2aContents) + "|\0\1|" + f2aContents

    def sec3(self):
        f3a = open(f"{self.temp_lab_dir}/q3/f3a.txt", "w+")
        h3 = open(f"{self.temp_lab_dir}/q3/h3.txt", "w+")

        s1 = generateString(25)
        s2 = generateString(25)
        content = (
            "Do not change this line: " + s1 + "\n"
            + "replace this with your matching string\n"
            + "Do not change this line: " + s2
        )

        f3a.write(content)
        h3.write(toInternetChecksum(content))

        f3a.close()
        h3.close()

        return s1 + "|\0\1|" + s2 + "|\0\1|"+ toInternetChecksum(content) 

    def sec4(self):
        # clone files
        with open(f"{self.static_dir}/f4_template.html", "r") as file:
            content = file.read()
            file.close()

        toChange = generateString(25)
        content = content.replace("%%IfStatementValue%%", toChange)

        with open(f"{self.temp_lab_dir}/q4/f4a.html", "w+") as file:
            file.write(content)
            file.close()

        return toChange + "|\0\1|" + toInternetChecksum(content)

class spoof:
    def __init__(self, f) -> None:
        self.file = f
        pass

def main(args: list[str]):
    args.pop(0)
    
    cmd = args[0]
    settings = CLIHandler.handle(args)

    if len(args) == 0:
        print("No arguments specified, defaulting to new lab gen...")
        Lab3LabTemplate(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        Lab3LabTemplate(settings.destination).generate_lab()
    elif cmd == "grade":
        destination = settings.input is not None and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = Lab3LabTemplate().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        a = shutil.make_archive(
            base_name="temp_solutions",  # Name of the archive
            format='zip',            # Format of the archive ('zip', 'tar', 'gztar', 'bztar', 'xztar')
            root_dir=Path(destination).parent,     # Root directory to archive
            base_dir=Path(destination).name,           # Base directory to be archived; use None to archive the entire root_dir
            verbose=True             # Print status messages to stdout (optional)
        )
        with open(a, "rb") as f:
            results = Lab3LabTemplate().grade("", template, spoof(f))
            print(f'Score:\n{results.score}\nFeedback:\n{results.feedback}')
        os.remove(toDelete)

if __name__ == "__main__":
    
    # Lab3LabTemplate().generate_lab()
    main(sys.argv)
