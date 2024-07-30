
# Lab 2 - Ransomware and Encryption Lab
This lab has three parts to it.

You are given R1.py, R2.py, and R3.py.

These are ransomware files, that, when run will encrypt a target file or all the files in it's directory.

You are also given D1.py, D2.py, and D3.py.

These will serve as the decryption files in which you will write your code for each question.

## Question 1
For question 1, locate the following files in the `lab/Q1` subdirectory:

 - R1.py
 - Solution_1.txt.encrypted
 - Solution_1.txt.Token

R1.py is the first iteration of the ransomware file. It features no obfuscation, and should be relatively easy to reverse. Your task is to reverse engineer the program and write a decryption program to decrypt Solution_1.txt.encrypted. Once decrypted, submit Solution_1.txt in your solutions folder.

## Question 2
For question 2, locate the following files in the `lab/Q2` subdirectory:

 - R2.py
 - Solution_2.txt.encrypted
 - Solution_2.txt.Token

R2.py is the second iteration of the ransomware file. It features obfuscation, and should be more challenging to reverse. You need to do the same thing and write a decryption program to decrypt Solution_2.txt.encrypted. Submit Solution_2.txt in your solutions folder after recovering its contents.

## Question 3
For question 3, locate the following files in the `lab/Q3` subdirectory:

 - R3.py
 - Solution_3.txt.encrypted
 - Solution_3.txt.Token

R3.py is the third iteration of the ransomware file. Unlike the other ransomware files, R3.py uses hybrid encryption. It is the most challenging to reverse. You need to do the same thing and write a decryption program to decrypt Solution_3.txt.encrypted. Submit Solution_3.txt in submission folder after performing the decryption.

*** Hint: A psuedorandom generator with a 16-bit seed is used to generate the RSA key and the symmetric key, allowing two methods of attack. ***
