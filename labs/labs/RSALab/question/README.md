
# Lab 4 - Breaking Textbook and Weakly-padded RSA
This lab has 5 parts. 

## Question 1
For question 1, locate the following files in the `lab-input` subdirectory:

 - e1
 - d1
 - n1
 - ma1
 - mb1
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
For question 2, we want to do the inverse, hence we want to write code to encrypt ma1 and mb1 in the following:

 1. Textbook RSA
 2. PKCS1.5
 3. PKCS_OAEP

For this, you do not need to submit anything.

## Question 3

For this question, we aim to break textbook RSA encryption.

In your `lab-input` folder, you will find the following:

 - ciphertexts.csv
	 - contains 'eavesdropped ciphertexts' (with corresponding identifiers)
- plaintexts.csv
	- contains 'suspected plaintexts' (and corresponding identifiers)
- pair0-1

Your task is to find the two ciphertexts and their two plaintext matches.

pair0-1 is one of the two matches. If one of the two pairs you find is listed in pair0-1 then the other should most likely be correct as well. 

Save the other pair in your answers folder as pair0-2, using the same csv format that pair0-1 has.

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
e1 and n1). The file pair1-1 in the lab-input folder contains one match (as
a pair of comma-separated identifiers of plaintext and ciphertext); check
that one of the matches you found is the same as the contents of this file.
If so, then the other pair you found should also be correct; save it in file
pair1-2 in the lab-answers folder, using the same format. 

You should also keep note of the runtime for this operation.

## Question 5

For this question we want to brute force the padding, instead of using a known pad. 

Try finding a random string with 4 bits of padding, 8 bits of padding, 12 bits of padding, 16 bits of padding, and then 20 bits of padding. 

You should find two matches for each padding length. You can double check your results with the following files:

 - Pair2-1
	 - one of the two matches for 4 bits of padding
- Pair 3-1
	- one of two matches for 8 bits of padding
- Pair 4-1
	- one of two matches for 12 bits of padding
- Pair 5-1
	- one of two matches for 16 bits of padding
- Pair 6-1
	- one of two matches for 20 bits of padding

If one of the pairs for each padding matches the given pairs, your other pair should be correct.

For each padding, submit your other pair in the same csv format as each question, that being pair2-2, pair3-2, pair4-2, pair5-2, and pair6-2.

Submit pair2-2, pair3-2, pair4-2, pair5-2, and pair6-2 in your lab-solutions folder. 

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
