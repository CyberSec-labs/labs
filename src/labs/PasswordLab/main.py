from functools import cached_property
from pathlib import Path
import py_compile
import random
import shutil
import string
import hashlib
import subprocess
import secrets
import sys
import binascii
import os

from src.utils import Grade, LabTemplate, Lab, CLIHandler

# files needed: 
#all the utils files [Login.py, gang, MostCommonPWs, PwnedPWfile, HashedPWs, PwnedPWs100k, SaltedPWs, PwnedPWs100k]
def hashF(password):
    hash = hashlib.sha256()
    hash.update(bytes(password, 'utf-8'))
    hashed = hash.hexdigest()
    return hashed

def hashAndSaltF(password):
    salt = secrets.token_bytes(8)  # generate salt
    hex_salt = str(binascii.b2a_hex(salt))[2:-1]  # easier to understand
    # the use of [2:-1] removes the b'--' from converting a bytes object to a string

    # NOTE: There are multiple ways to create a salted hash one of which is the (more rigorous)
    # PBKDF2 HMAC algorithm using SHA256. For the sake of simiplicity, we will just append the salt
    # and hash it as we did in Question 5. Feel free to research this alternative mechanism...
    # hashed = binascii.b2a_hex(hashlib.pbkdf2_hmac('sha256', bytes(temp, 'utf-8'), salt_q6, 100))

    salt_pass = hex_salt + password  # salt, hash
    hashedSalt = hashF(salt_pass)
    return f"{hex_salt},{hashedSalt}"

class PasswordLabLabTemplate(LabTemplate):
    # DB properties
    lab_template_id: int = 5
    # Used only when seeding for the first time
    seed_name: str = ""
    seed_section: str = "Password Lab"
    seed_short_description: str = (
        "Example description"
    )
    seed_long_description: str = "Example long description "
    seed_active: bool = True
    # Static dir
    static_dir: Path = Path(__file__).parent

    @staticmethod
    def _grade(submitted_solution: str, solution: str) -> Grade:
        """Grades a submissions
        """


        score = 0
        feedback = "example"

        return Grade(score=score, feedback=feedback)

    def generate_lab(self, *, user_id: int = 0, seed: str = "abcd", debug: bool = False) -> Lab:  # type: ignore
        
        random.seed(seed)
        solution = ""
        for i in range(6):
            if os.path.exists(f"{self.temp_lab_dir}/Q{i + 1}"):
                shutil.rmtree(f"{self.temp_lab_dir}/Q{i + 1}")
            os.mkdir(f"{self.temp_lab_dir}/Q{i + 1}")
            if i ==0:
                py_compile.compile(f"{self.static_dir}/Login.py", f"{self.temp_lab_dir}/Q{i+1}/Login.pyc")
            else:
                shutil.copy(f"{self.temp_lab_dir}/Q1/Login.pyc", f"{self.temp_lab_dir}/Q{i+1}/Login.pyc")

        mcp = []
        with open(f"{self.static_dir}/MostCommonPWs", "r") as f:
            mcp = f.read().split()
            f.close()
        
        pwned100k = []

        with open(f"{self.static_dir}/PwnedPWs100k", "r", errors="ignore") as f:
            pwned100k = f.read().split()
            f.close()
        
        names = []

        with open(f"{self.static_dir}/names", "r") as f:
            names = f.read().split()
            f.close()
        
        gang = []
        with open(f"{self.static_dir}/gang", "r") as f:
            gang = f.read().split()
            f.close()

        pwd = [] #gang embers respective passwords

        if len(gang) < 6:
            print("Gang file contains less than " + str(6) + " members!")
            # todo: make an exit

        random.shuffle(gang)

        if 'Adam' in gang:
            gang.remove("Adam")

        gang.append("Adam")
        gang.reverse()

        # Q1: A most common password for Adam
        pwd.append(random.choice(mcp).strip())
        # Q2: A most common password for 1 random gang member
        pwd.append(random.choice(mcp).strip())
        # Q3: A pwned100k password for 1 random gang member
        pwd.append(random.choice(pwned100k).strip())
        # Q4: A random eight digit password for 1 random gang member
        pwd.append(''.join(random.choices(string.ascii_uppercase +
                string.ascii_lowercase + string.digits, k=8)))
        # Q5: A pwned100k password for 1 random gang member + two random digits
        pwd.append(random.choice(pwned100k).strip()+str(random.randint(10, 99)))
        # Q6: A pwned100k password for 1 random gang member + one random digit
        pwd.append(random.choice(pwned100k).strip()+str(random.randint(0, 9)))

        shutil.copy(f"{self.static_dir}/MostCommonPWs", f"{self.temp_lab_dir}/Q1/MostCommonPWs")
        shutil.copy(f"{self.static_dir}/MostCommonPWs", f"{self.temp_lab_dir}/Q2/MostCommonPWs")
        shutil.copy(f"{self.static_dir}/PwnedPWs100k", f"{self.temp_lab_dir}/Q3/PwnedPWs100k")
        shutil.copy(f"{self.static_dir}/PwnedPWs100k", f"{self.temp_lab_dir}/Q5/PwnedPWs100k")
        shutil.copy(f"{self.static_dir}/PwnedPWs100k", f"{self.temp_lab_dir}/Q6/PwnedPWs100k")

        for i in range(0, 6):
            solution = solution + f"_{gang[i]}\0\1{pwd[i]}"

        for i in range(6, len(gang)):
            pwd.append(''.join(random.choices(string.ascii_uppercase +
                string.ascii_lowercase + string.digits, k=15)))
            
        # ===![ Write Solution ]|=== #
        text_hash =[]
        for i in range(len(gang)):
            hash = hashlib.sha256()
            hash.update(bytes(gang[i]+pwd[i], 'utf-8'))
            for j in range(90000):
                hash.update(hash.digest())
            hashed = hash.hexdigest()
            text_hash.append(gang[i]+","+hashed)

        random.shuffle(text_hash)

        with open(".loginCheck", "w+") as loginCheck:
            for i in range(len(gang)):
                loginCheck.write(text_hash[i]+"\n")
            loginCheck.close()

        total = 5000
        
        # Q4: Random generation of passwords, creates PwnedPWfile which contains randomly chosen names & gang members with randomly generated passwords
        
        q4 = []
        for i in range(total):
            # append a gang member with an incorrect password, or random name
            q4.append(f"{random.choice(names + gang)},{''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))}")
        q4.append(f"{gang[3]},{pwd[3]}")  # append the actual answer

        random.shuffle(q4)

        with open(f"{self.temp_lab_dir}/Q4/PwnedPWfile", "w+") as PwnedPWfile:
            PwnedPWfile.writelines(q4)
            PwnedPWfile.close()

        # Q5: Hashes a given password, creates HashedPWs which contains randomly chosen names & gang members with hashed passwords
        # Lines are stored in format: Name, hash
        q5 = []
        for i in range(total):
            temp = random.choice(pwned100k).strip()+str(random.randint(10, 99))
            hashed = hashF(temp)
            q5.append(f"{random.choice(names + gang)},{hashed}")
        q5.append(f"{gang[4]},{hashF(pwd[4])}")  # append the actual answer

        random.shuffle(q5)
        with open(f'{self.temp_lab_dir}/Q5/HashedPWs', "w+") as HashedPWs:
            HashedPWs.writelines(q5)
        HashedPWs.close()

        # Q6: Hashes and salts a given password, creates SaltedPWs which contains randomly chosen names & gang members with hashed and salted passwords
        # Lines are stored in format: Name, salt, hash
        q6 = []
        for i in range(total):
            temp = random.choice(pwned100k).strip()+str(random.randint(0, 9))
            hashedSalt = hashAndSaltF(temp)
            q6.append(f"{random.choice(names + gang)},{hashedSalt}")
        q6.append(f"{gang[5]},{hashAndSaltF(pwd[5])}")  # append the actual answer

        random.shuffle(q6)
        with open(f'{self.temp_lab_dir}/Q6/SaltedPWs', 'w+') as SaltedPWs:
            SaltedPWs.writelines(q6)
        SaltedPWs.close()

        py_compile.compile("utils/Login.py", "utils/Login.pyc")
        
        return Lab(
            lab_template_id=self.lab_template_id,
            user_id=user_id,
            seed=seed,
            unique_question_file=self._zip_temp_lab_dir_and_read(),
            solution=solution,
        )
    

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
        PasswordLabLabTemplate(settings.destination).generate_lab()
        return
    
    if cmd == "gen":
        PasswordLabLabTemplate(generated_dir=settings.destination).generate_lab()
    elif cmd == "grade":
        destination = (settings.input is not None) and settings.input or "./solutions"
        if os.path.exists(destination) == False:
            print("Failed to get solutions folder. Either specify it via ./python main grade [folder path] or drag your solutions folder into the current working directory.")
            return
        # if run locally, should use non random solutions
        template = PasswordLabLabTemplate().generate_lab().solution
        toDelete = f"{os.getcwd()}/temp_solutions.zip"
        a = shutil.make_archive(
            base_name="temp_solutions",  # Name of the archive
            format='zip',            # Format of the archive ('zip', 'tar', 'gztar', 'bztar', 'xztar')
            root_dir=Path(destination).parent,     # Root directory to archive
            base_dir=Path(destination).name,           # Base directory to be archived; use None to archive the entire root_dir
            verbose=True             # Print status messages to stdout (optional)
        )
        with open(a, "rb") as f:
            print(PasswordLabLabTemplate().grade("", template, spoof(f)))
        os.remove(toDelete)

if __name__ == "__main__":
    main(sys.argv)
