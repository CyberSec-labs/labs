
# Lab 4 - Breaking Textbook and Weakly-padded RSA
This lab has 5 parts. 

## Question 1
For question 1, locate the following files in the `lab-input` subdirectory:

 - TextbookRSA.py
 - e1
 - d1
 - n1
 - m1
 - m2
 - cx1a
 - cx1b
 - cx1c
 - cy1a
 - cy1b
 - cy1c

The a, b, and c versions of cx and cy files are encrypted using different versions of RSA. A corresponds to Textbook RSA, B uses PKCS1.5, and C uses PKCS1_OAEP.

Your task is to implement the 3 versions of RSA decryption needed to decrypt the A, B, and C versions of the files. Files e1 and d1 contain RSA encryption and decryption keys, both which use the modulus found in n1. 

 1. Use the private key and modulus to decrypt cx1a and cy1a.
 2. Decrypt cx1b and cy2b.
 3. Decrypt cx1c and cy1c.
*Hint*: remember to remove the padding for both PKCS and OAEP encryptions.

Save the results in the corresponding files mx1a,
mx1b, mx1c, my1a, my1b, and my1c in the lab-answers folder. 

To allow you to check your program, one result from each pair should be identical
to one of the two input message files, ma1 and mb1. If you got this one
right, you likely also got the other decryption right. You can also
confirm that during the decryption of the PKCS#1 version 1.5 and OAEP
ciphertexts, you find correctly padded plaintexts.

## Question 2
For question 2, we want to do the inverse, hence we want to write code to encrypt m1 and m2 in the following:

 1. Textbook RSA
 2. PKCS1.5
 3. PKCS_OAEP

For this, you do not need to submit anything.

## Question 3

For questions 3-5, you will use the files e2 and n2 in the 'lab/lab-input' folder to form the necessary key for these parts.

For this question, we aim to break textbook RSA encryption. 

In your `lab-input` folder, you will find the following:

- ciphertexts.csv
	- contains 'eavesdropped ciphertexts' (with corresponding identifiers)
- plaintexts.csv
	- contains 'suspected plaintexts' (and corresponding identifiers)
- pair0-1

Your task is to find the two ciphertexts and their two plaintext matches.

pair0-1 is one of the two matches. If one of the two pairs you find is listed in pair0-1 then the other should most likely be correct as well. 

Save the other pair in your answers folder as pair0-2, using the same csv format that pair0-1 has. The only difference will be the numbers in file names.

You may also want to measure the runtime.

## Question 4

Now you see how easy textbook RSA is, without any padding it's very simple. 
Let’s try a naive padding.
Specifically, let us define the NP1 (‘Naive Padding 1’) as: NP1(m) =
0x02 ++ r ++ m, where m is the (pre-padding) plaintext message, r is one
byte consisting of four random bits followed by four zero bits. This is an
(overly) simplified version of the PKCS#1 version 1.5 padding algorithm, as defined in Equation 6.59 (subsection 6.5.6).

Reuse the ciphertexts.csv and plaintexts.csv files. You should again be able
to identify two of the plaintexts from plaintexts.csv as corresponding to two
of the ciphertexts (in ciphertexts.csv). This time, when applying padding
NP1 to the plaintexts before applying RSA textbook encryption (using
e2 and n2). The file pair4-1 in the lab-input folder contains one match (as
a pair of comma-separated identifiers of plaintext and ciphertext); check
that one of the matches you found is the same as the contents of this file.
If so, then the other pair you found should also be correct; save it in file
pair4-2 in the lab-answers folder, using the same format. 

You should also keep note of the runtime for this operation.

## Question 5

For this question we want to brute force the padding, instead of using a known pad.

Try finding a random string, r, with 8 random bits of padding, 12 random bits followed by four zero bits of padding, 16 random bits of padding, and then 20 random bits followed by four zero bits of padding. Use this r in the NP1(m) function defined in question 4.

You should find two matches for each padding length. You can double check your results with the following files:

- Pair8-1
	- one of the two matches for 8 random bits of padding
- Pair 12-1
	- one of two matches for 12 random bits followed by four zero bits of padding 
- Pair 16-1
	- one of two matches for 16 random bits of padding
- Pair 20-1
	- one of two matches for 20 random bits followed by four zero bits of padding

*** Duplicate solutions may be found, but each pair is used only once as a solution. For example, if a file pair is identified by both the 12 and 16 random bit pads, it will only be the solution for padding with 12 random bits. *** 

If one of the pairs for each padding matches the given pairs, your other pair should be correct.

For each padding, submit your other pair in the same csv format as each question, that being pair2-2, pair3-2, pair4-2, and pair5-2.

Submit pair8-2, pair12-2, pair16-2, and pair20-2 in your lab-solutions folder. 

You should also test the runtime to find each set of pairs. Test and keep note of each.

In addition, do the following:
- Create a graph of the runtime for the time it took to decrypt using
a random string from 0 to 20 bits.
- Identify the function giving the runtime as a function of the number
of random bits.
- Using the function you identified, approximate the runtime if you
used this attack to decrypt encryption with padding of eight random
bytes, the minimal number of random bytes required by PKCS#1
version 1.5.
- Repeat, for padding of 4 random bytes and check how long it takes.

## Challenge

In this lab, you tried to find the proper decryptions of several files and how padding can make that task more difficult. To do so, you made use of a list of plaintexts that your ciphertexts could potentially decrypt into. In more realistic situations, an attacker who has eavesdropped a ciphertext should not know the private half of the RSA key nor should they know what the message could potentially be. Even without this information at their disposal, an attacker can still learn the contents of the plaintext due to the malleability of RSA. As discussed in this chapter, the Bleichenbacher attack against the PKCS#1 version 1.5 padding scheme takes these factors into account. Your task for this part of the lab will be to implement a Bleichenbacher attack against the NP1(m) function that was defined in Question 4. You will perform this attack for when r is 64 bits of padding and for when r is 96 bits of padding.

In the lab/Challenge folder, you will find the files e3 and n3, which make up the public half of the RSA key used for encryption. You will also find the file Padding_Check.pyc which will serve as the oracle that tells you whether or not a ciphertext is properly padded according to NP1(m). The files c64-1 and c64-2 will be the ciphertexts when r is 64 bits and c96-1 and c96-2 are the ciphertexts when r is 96 bits. The files p64-1 and p96-1 are the original unpadded plaintexts for their corresponding ciphertext and are given to you in order to help you test your code. When you are able to find p64-1 by running the attack on c64-1, run the attack on c64-2 and submit the recovered plaintext in p64-2. Repeat this for c96-1 and c96-2 and submit p96-2.

*** Hint: use big-endian byte ordering to ensure correct processing. ***
