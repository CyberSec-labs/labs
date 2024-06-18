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
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from fastapi import UploadFile
import zipfile
import rsa

from src.utils import Grade, LabTemplate, Lab, CLIHandler


def generateString(len):
    """Generate random string which will be what our "downloads" end up being in Q1files"""
    return "".join(random.choice(string.ascii_letters) for _ in range(len))


class Lab2LabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 2
    # Used only when seeding for the first time
    seed_name: str = "Ransomware and Encryption Lab"
    seed_section: str = "Ch2"
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

        # TODO: edit this based on pending changes to the lab that are needed. awaiting professor approval.

        try:
            f = files.read(f"{base_dir}/example.txt")

            if f == solutions[0]:
                score = 100
            else:
                feedback = feedback + "Question 1 solution is incorrect."
        except KeyError:
            feedback = feedback + "Missing example.txt from uploaded zip archive.\n"
        feedback = feedback + "Part 2 requires manual review."
        return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore
        random.seed(seed)
        if not os.path.exists(f"{self.temp_lab_dir}/Q1"):
            os.mkdir(f"{self.temp_lab_dir}/Q1")
        if not os.path.exists(f"{self.temp_lab_dir}/Q2"):
            os.mkdir(f"{self.temp_lab_dir}/Q2")
        if not os.path.exists(f"{self.temp_lab_dir}/Q3"):
            os.mkdir(f"{self.temp_lab_dir}/Q3")
        q1Solution = self.sec1(seed)
        q2Solution = self.sec2(seed)
        q3Solution = self.sec3(seed)
        # q2Solution = self.sec2()

        # Solution is valid, expired, invalid_ca, invalid_cn
        solution = f"{q1Solution}"
        # Copy the question folder into the directory that will be given to users
        self._copy_q_dir_into_lab_generated_dir()
        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )

    def sec1(self, original):
        insecureKey = random.randbytes(32)
        # this is for r1.py
        # it uses an insecure shared key to encrypt our seeds, and is not obfuscated.
        with open(f"{self.static_dir}/Malware Files/R1.py", "r") as template:
            patched = template.read()
            patched = patched.replace("INSECURE_ENCRYPTION_KEY", str(insecureKey))
            with open(f"{self.temp_lab_dir}/Q1/R1.py", "w+") as f:
                f.write(patched)
                f.close()
            template.close()

        seed_cipher = AES.new(insecureKey, AES.MODE_CBC)
        seed = random.randbytes(32)
        random.seed(seed)
        encrypted_seed = seed_cipher.encrypt(pad(seed_cipher, AES.block_size))
        cipher = AES.new(random.randbytes(32), AES.MODE_CBC)

        with open(f"{self.temp_lab_dir}/Q1/Encrypted1.txt", "r+b") as f:
            contents = f.read()
            encrypted = cipher.encrypt(pad(contents, AES.block_size))
            f.seek(0)
            f.write(encrypted)
            f.close()

        with open(f"{self.temp_lab_dir}/Q1/Encrypted1.token.txt", "w+") as f:
            f.write(str(encrypted_seed))
            f.close()
        
        random.seed(original)
    
    def sec2(self):
        # this is for r2.py
        # uses the same insecure shared key encryption, but is obfuscated to a mild degree.
        insecureKey = random.randbytes(32)
        with open(f"{self.static_dir}/Malware Files/R2.py", "r") as template:
            patched = template.read()
            patched = patched.replace("INSECURE_ENCRYPTION_KEY", str(insecureKey))
            with open(f"{self.temp_lab_dir}/R2.py", "w+") as f:
                f.write(patched)
                f.close()
            template.close()

        seed_cipher = AES.new(insecureKey, AES.MODE_CBC)
        seed = random.randbytes(32)
        random.seed(seed)
        encrypted_seed = seed_cipher.encrypt(pad(seed_cipher, AES.block_size))
        cipher = AES.new(random.randbytes(32), AES.MODE_CBC)

        with open(f"{self.temp_lab_dir}/Q1/Encrypted1.txt", "r+b") as f:
            contents = f.read()
            encrypted = cipher.encrypt(pad(contents, AES.block_size))
            f.seek(0)
            f.write(encrypted)
            f.close()

        with open(f"{self.temp_lab_dir}/Q1/Encrypted1.token.txt", "w+") as f:
            f.write(str(encrypted_seed))
            f.close()

    def sec3(self):
        keyprivate = RSA.generate(2048)
        keyprivate.public_key()
        # r3.py uses a public/private key encryption scheme. it is much more secure.
        # r3 is not obfuscated as that would pose too much of a challenge for students
        with open(f"{self.static_dir}/Malware Files//R3.py", "r") as template:
            patched = template.read()
            patched = patched.replace(
                "PUBLIC_RSA_KEY", str(keyprivate.public_key().export_key())
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
        Lab2LabTemplate(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        Lab2LabTemplate(generated_dir=settings.destination).generate_lab()
    elif cmd == "grade":
        destination = (settings.input is not None) and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = Lab2LabTemplate().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        a = shutil.make_archive(
            base_name="temp_solutions",  # Name of the archive
            format='zip',            # Format of the archive ('zip', 'tar', 'gztar', 'bztar', 'xztar')
            root_dir=Path(destination).parent,     # Root directory to archive
            base_dir=Path(destination).name,           # Base directory to be archived; use None to archive the entire root_dir
            verbose=True             # Print status messages to stdout (optional)
        )
        with open(a, "rb") as f:
            print(Lab2LabTemplate().grade("", template, spoof(f)))
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
