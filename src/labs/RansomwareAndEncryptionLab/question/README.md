
# Lab 2 - Ransomware and Encryption Lab
This lab has three parts to it.

You are given R1.py, R2.py, and R3.py.

These are ransomware files, that, when run will encrypt a target file or all the files in it's directory.

You are also given D1.py, D2.py, and D3.py.

These will serve as the decryption files in which you will write your code for each question.

## Question 1
For question 1, locate the following files in the `lab/Q1` subdirectory:

 - R1.py
 - Solution_1.txt
 - Solution_1.txt.TOKEN

R1.py is the first iteration of the ransomware file. It features no obfuscation, and should be relatively easy to reverse. Your task is to reverse engineer the program and write a decryption program to decrypt Solution_1.txt. Drag Solution_1.txt into your solutions folder after decrypting it.

## Question 2
For question 2, locate the following files in the `lab/Q2` subdirectory:

 - R2.py
 - Solution_2.txt
 - Solution_2.txt.TOKEN

R2.py is the second iteration of the ransomware file. It features obfuscation, and should be more challenging to reverse. You need to do the same thing and write a decryption program to decrypt Solution_2.txt. Drag Solution_2.txt into your solutions folder after decrypting it.

## Question 3
For question 3, locate the following files in the `lab/Q3` subdirectory:

 - R3.py
 - Solution_3.txt
 - Solution_3.txt.TOKEN

R3.py is the third iteration of the ransomware file. Unlike the other ransomware files, R3.py uses public key encryption. It is the most challenging to reverse. You need to do the same thing and write a decryption program to decrypt Solution_3.txt. Drag Solution_3.txt into your solutions folder after decrypting it.

*** Hint: The private half of the RSA key used in R3.py was generated after setting a 16-bit seed, which means it was created under a pre-set condition. ***
