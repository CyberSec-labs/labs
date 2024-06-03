# updated for S23 by Mason Tumminelli
# original code by Amir Herzberg and Connor Rickermann

import random
import string
import hashlib
import secrets
import binascii
import json
import shutil
import py_compile
import os
# DO NOT RUN IN MAIN LAB1 DIRECTORY

# can ignore, moves necessary files into folders and compiles login - administrative setup


def admin():
    print("Compiling, copying and moving files..")
    # compiles Login file
    py_compile.compile("utils/Login.py", "utils/Login.pyc")
    shutil.copy("utils/Login.py", "LoginTemplate.py")

    for i in range(6):
        os.mkdir(f"Q{i+1}")
        shutil.copy("utils/Login.pyc", f"Q{i+1}/Login.pyc")
        shutil.copy("utils/gang", f"Q{i+1}/gang")

    shutil.copy("utils/MostCommonPWs", "Q1/MostCommonPWs")
    shutil.copy("utils/MostCommonPWs", "Q2/MostCommonPWs")
    shutil.copy("utils/PwnedPWs100k", "Q3/PwnedPWs100k")
    shutil.move("PwnedPWfile", "Q4/PwnedPWfile")
    shutil.move("HashedPWs", "Q5/HashedPWs")
    shutil.copy("utils/PwnedPWs100k", "Q5/PwnedPWs100k")
    shutil.move("SaltedPWs", "Q6/SaltedPWs")
    shutil.copy("utils/PwnedPWs100k", "Q6/PwnedPWs100k")

    # Ronald - 1/25/2023
    # Moved from top of function to fix permission error
    os.system("chown -R cse:cse utils")

    os.mkdir("LabGen")
    shutil.move("Lab1Gen.py", "LabGen/Lab1Gen.py")
    return

# takes in a password as input, and returns its hash


def hashF(password):
    hash = hashlib.sha256()
    hash.update(bytes(password, 'utf-8'))
    hashed = hash.hexdigest()
    return hashed

# takes in a password as input, hashes and salts it


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

# main labgen functions


def labGen():
    # ===|[ Definitions ]|===#
    mcp = open("utils/MostCommonPWs", "r").read().split()
    pwned100k = open("utils/PwnedPWs100k", "r", errors='ignore').read().split()
    names = open("utils/names", "r").read().split()
    gang = open("utils/gang", "r").read().split()  # list of gang members
    pwd = []  # gang members respective passwords
    studentSolution = {}  # for autograding

    # ===|[ Setup and Generate Solutions ]|===#
    # ensures there are unique members for each password
    if len(gang) < 6:
        print("Gang file contains less than " + str(6) + " members!")
        return -1

    # ensures that 'Adam' is the first member and randomize student's gang members
    random.shuffle(gang)
    if 'Adam' in gang:
        gang.remove('Adam')
    gang.append('Adam')
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

    # iterate and add solutions to dictionary. The first 6 random gang members (including Adam) are chosen as the solution.
    # add remainder of the gang members with a random complex password that is hard to guess.
    studentSolution[f"Q1"] = f"{pwd[0]}"  # Adam's password
    for i in range(1, 6):
        # for autograding, record username
        studentSolution[f"Q{i+1}A"] = f"{gang[i]}"
        # for autograding, record password
        studentSolution[f"Q{i+1}B"] = f"{pwd[i]}"
    for i in range(6, len(gang)):
        pwd.append(''.join(random.choices(string.ascii_uppercase +
                   string.ascii_lowercase + string.digits, k=15)))
    # ===|[ Write Solutions ]|===#
    # hash passwords and add them for Login.py to utilize
    text_hash = []
    for i in range(len(gang)):
        hash = hashlib.sha256()
        # simple defenses against dictionary attack
        hash.update(bytes(gang[i]+pwd[i], 'utf-8'))
        for j in range(90000):
            hash.update(hash.digest())  # prepend name and iterate
        hashed = hash.hexdigest()
        text_hash.append(gang[i]+","+hashed)
    # shuffle order of the gang members, so cannot tell order in file
    random.shuffle(text_hash)

    # write to file, all gang members in shuffled order with their respective hashed passwords
    with open('.loginCheck', "w+") as loginCheck:
        for i in range(len(gang)):
            loginCheck.write(text_hash[i]+"\n")
    loginCheck.close()

    # write solutions to JSON file for autograding
    with open('Solutions.json', "w") as f:
        json.dump(studentSolution, f)
    f.close()

    # ===|[ File Generation for Questions 4, 5 and 6]|===#
    total = 5000

    # Q4: Random generation of passwords, creates PwnedPWfile which contains randomly chosen names & gang members with randomly generated passwords
    q4 = []
    for i in range(total):
        # append a gang member with an incorrect password, or random name
        q4.append(f"{random.choice(names + gang)},{''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))}")
    q4.append(f"{gang[3]},{pwd[3]}")  # append the actual answer

    random.shuffle(q4)
    with open('PwnedPWfile', "w+") as PwnedPWfile:
        for i in q4:
            PwnedPWfile.write(i+"\n")
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
    with open('HashedPWs', "w+") as HashedPWs:
        for i in q5:
            HashedPWs.write(i+"\n")
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
    with open('SaltedPWs', 'w+') as SaltedPWs:
        for i in q6:
            SaltedPWs.write(i+"\n")
    SaltedPWs.close()

    admin()  # do admin work
    print("Success!")


if __name__ == "__main__":
    labGen()
