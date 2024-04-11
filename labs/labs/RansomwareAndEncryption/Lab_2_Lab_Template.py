from functools import cached_property
from hashlib import sha256
import os
from pathlib import Path
import random
import shutil
import string
import subprocess
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from fastapi import UploadFile
import zipfile
import rsa

from labs.utils import Grade, LabTemplate, Lab


def generateString(len):
    """Generate random string which will be what our "downloads" end up being in Q1files"""
    return "".join(random.choice(string.ascii_letters) for _ in range(len))


class Lab2LabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 2
    # Used only when seeding for the first time
    seed_name: str = "Ransomware and Encryption Lab"
    seed_section: str = "Ch2"
    seed_short_description: str = (
        "Add short seed description"
    )
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

        # TODO: edit this based on pending changes to the lab that are needed. awaiting professor approval.

        try:
            f = files.read(f"{base_dir}/example.txt")

            if (f == solutions[0]):
                score = 100
            else:
                feedback = feedback + "Question 1 solution is incorrect."
        except KeyError:
            feedback = feedback + "Missing example.txt from uploaded zip archive.\n"
        feedback = feedback + "Part 2 requires manual review."
        return Grade(score=score, feedback=feedback)


    def generate_lab(self, *, user_id: int = 0, seed: str = "", debug: bool = False) -> Lab:  # type: ignore

        q1Solution = self.sec1()
        q2Solution = self.sec2()

        # Solution is valid, expired, invalid_ca, invalid_cn
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

        keyprivate = RSA.generate(2048)
        keyprivate.public_key()

        insecureKey = random.randbytes(32)
        # this is for r1.py
        # it uses an insecure shared key to encrypt our seeds, and is not obfuscated.
        with open(f"{self.static_dir}/Malware Files/R1.py", "r") as template:
            patched = template.read()
            patched = patched.replace(
                "INSECURE_ENCRYPTION_KEY", str(
                    insecureKey)
            )
            with open(f"{self.temp_lab_dir}/R1.py", "w+") as f:
                f.write(patched)
                f.close()

        # this is for r2.py
        # uses the same insecure shared key encryption, but is obfuscated to a mild degree.
        insecureKey = random.randbytes(32)
        with open("{self.static_dir}/Malware Files/R2.py", "r") as template:
            patched = template.read()
            patched = patched.replace(
                "INSECURE_ENCRYPTION_KEY", str(
                    insecureKey)
            )
            with open(f"{self.temp_lab_dir}/R2.py", "w+") as f:
                f.write(patched)
                f.close()

        # r3.py uses a public/private key encryption scheme. it is much more secure.
        # r3 is not obfuscated as that would pose too much of a challenge for students
        with open("{self.static_dir}/Malware Files//R3.py", "r") as template:
            patched = template.read()
            patched = patched.replace(
                "PUBLIC_RSA_KEY", str(
                    keyprivate.public_key().export_key())
            )
            with open(f"{self.temp_lab_dir}/R3.py", "w+") as f:
                f.write(patched)
                f.close()
        # our decryption template is the same across all malware files, so only write this once.

        with open(f"{self.static_dir}/D1.py", "rb") as decryption_template:
            with open(f"{self.temp_lab_dir}/D1.py", "w+b") as f:
                f.write(decryption_template.read())
                decryption_template.close()
                f.close()

    def sec2(self):
        if not os.path.exists(f"{self.temp_lab_dir}/Q2files"):
            os.mkdir(f"{self.temp_lab_dir}/Q2files")
        key = RSA.generate(2048)
        public = key.public_key()
        signer = pkcs1_15.new(key)

        with open(f"{self.temp_lab_dir}/Q2files/Q2pk.pem", "w+b") as f:
            f.write(public.export_key())
            f.close()

        possible = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(possible)
        print(possible[:5])
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
            else:
                file_2.write(
                    random.randbytes(256)
                )  # if we want the file sig to not match we just generate random bytes instead


if __name__ == "__main__":
    Lab2LabTemplate().generate_lab()
