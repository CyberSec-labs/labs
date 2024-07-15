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

        score = 0.0
        solutions = solution.split("_")
        files = zipfile.ZipFile(file.file)
        base_dir = files.filelist[0].filename
        feedback = ""

        for ind, sol in enumerate(solutions):
            try:
                f = files.read(f'{base_dir}Solution_{ind+1}.txt').decode('utf-8')

                if f == sol:
                    score += 100/len(solutions)
                else:
                    feedback += f"Solution_{ind+1}.txt is incorrect.\n"
            except KeyError:
                feedback += f"Missing Solution_{ind+1}.txt from solutions folder.\n"
        score = int(score)

        return Grade(score=score, feedback=feedback)


    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore
        random.seed(seed)
        if not os.path.exists(f"{self.temp_lab_dir}/Q1"):
            os.mkdir(f"{self.temp_lab_dir}/Q1")
        if not os.path.exists(f"{self.temp_lab_dir}/Q2"):
            os.mkdir(f"{self.temp_lab_dir}/Q2")
        if not os.path.exists(f"{self.temp_lab_dir}/Q3"):
            os.mkdir(f"{self.temp_lab_dir}/Q3")
        q1Solution = self.sec1()
        q2Solution = self.sec2()
        q3Solution = self.sec3()

        solution = f"{q1Solution}_{q2Solution}_{q3Solution}"
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
        encrypted_seed = seed_cipher.encrypt(pad(seed, AES.block_size))
        cipher = AES.new(random.randbytes(32), AES.MODE_CBC)

        with open(f"{self.temp_lab_dir}/Q1/Solution_1.txt", "wb") as f:
            contents = generateString(25).encode('utf-8')
            encrypted = cipher.encrypt(pad(contents, AES.block_size))
            f.write(cipher.iv)
            f.write(encrypted)
            f.close()

        with open(f"{self.temp_lab_dir}/Q1/Solution_1.txt.TOKEN", "wb") as f:
            f.write(seed_cipher.iv)
            f.write(encrypted_seed)
            f.close()
        
        return contents.decode('utf-8')
    
    def sec2(self):
        # this is for r2.py
        # uses the same insecure shared key encryption, but is obfuscated to a mild degree.
        insecureKey = random.randbytes(32)
        with open(f"{self.static_dir}/Malware Files/R2.py", "r") as template:
            patched = template.read()
            patched = patched.replace("INSECURE_ENCRYPTION_KEY", str(insecureKey))
            with open(f"{self.temp_lab_dir}/Q2/R2.py", "w+") as f:
                f.write(patched)
                f.close()
            template.close()

        seed_cipher = AES.new(insecureKey, AES.MODE_CBC)
        seed = random.randbytes(32)
        random.seed(seed)
        encrypted_seed = seed_cipher.encrypt(pad(seed, AES.block_size))
        cipher = AES.new(random.randbytes(32), AES.MODE_CBC)

        with open(f"{self.temp_lab_dir}/Q2/Solution_2.txt", "wb") as f:
            contents = generateString(25).encode('utf-8')
            encrypted = cipher.encrypt(pad(contents, AES.block_size))
            f.write(cipher.iv)
            f.write(encrypted)
            f.close()

        with open(f"{self.temp_lab_dir}/Q2/Solution_2.txt.TOKEN", "wb") as f:
            f.write(seed_cipher.iv)
            f.write(encrypted_seed)
            f.close()

        return contents.decode('utf-8')

    def sec3(self):
        # r3.py uses a public/private key encryption scheme. it is much more secure.
        # r3 is not obfuscated as that would pose too much of a challenge for students
        rsa_seed = random.getrandbits(16)
        aes_seed = random.randbytes(32)
        
        random.seed(rsa_seed)

        keyprivate = RSA.generate(2048, randfunc = random.randbytes)
        keypublic = keyprivate.public_key()

        cipher_rsa = PKCS1_OAEP.new(keypublic)

        with open(f"{self.static_dir}/Malware Files//R3.py", "r") as template:
            patched = template.read()
            patched = patched.replace(
                "PUBLIC_RSA_KEY", str(keypublic.export_key())
                )
            with open(f"{self.temp_lab_dir}/Q3/R3.py", "w+") as f:
                f.write(patched)
                f.close()

        random.seed(aes_seed)
        encrypted_seed = cipher_rsa.encrypt(aes_seed)
        cipher = AES.new(random.randbytes(32), AES.MODE_CBC)

        with open(f'{self.temp_lab_dir}/Q3/Solution_3.txt', 'wb') as f:
            contents = generateString(25).encode('utf-8')
            encrypted = cipher.encrypt(pad(contents, AES.block_size))
            f.write(cipher.iv)
            f.write(encrypted)

        with open(f'{self.temp_lab_dir}/Q3/Solution_3.txt.TOKEN', 'wb') as f:
            f.write(encrypted_seed)

        # our decryption template is the same across all malware files, so only write this once.
        with open(f"{self.static_dir}/D1.py", "rb") as decryption_template:
            template = decryption_template.read()
            for i in range(1,4):
                if os.path.exists(f"{self.temp_lab_dir}/Q{i}/D{i}.py"):
                    continue
                with open(f"{self.temp_lab_dir}/Q{i}/D{i}.py", "w+b") as f:
                    f.write(template)
                    f.close()
            decryption_template.close()

        return contents.decode('utf-8')

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
            results = Lab2LabTemplate().grade("", template, spoof(f))
            print(f'Score:\n{results.score}\nFeedback:\n{results.feedback}')
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
