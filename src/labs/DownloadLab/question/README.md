
# Lab 1 - Download Lab
This lab has three parts.

## Question 1
For question 1, locate the following files in the `Q1files` subdirectory:

 - 10 text files starting from 0, to 9
 - Q1.hash

Q1.hash is the sha256 hash for one of the files. Your task is to figure out which file it is and submit the file in your submission folder.

## Question 2
For question 2, locate the following files in your `Q2files` subdirectory:

- Q2pk.pem
- 10 text files numbered 0 - 9 with random strings
- 10 text files with file hashes
	- these are labeled the same as the other 10 text files, with `_sig` appended to the end of the name.

The catch is that only half of the signature files are actually correct. 

Your task is to identify which file-signature pairs actually match and submit the text files only in your submissions folder. Drag the text file of the matching signatures into your submissions folder and just submit that to either the website or specify the folder as your input when using the autograde locally.

## Question 3
Question 3 is optional.

To get a feeling for the performance of public key signatures and of
cryptographic hash functions, perform experiments to the following:

 1.  The time required for hashing as a function of the input length, from
100000 bytes to one million bytes.
2. The time required for generation of signing and validation public key
pairs, from keys of lengths from 1000 bits to the maximal length you
find feasible (say, up to five minutes).
3. The time required to sign inputs for inputs of length from 100000 bytes to 1,000,000 bytes, using each of the private signing keys you generated
in the previous item.
4. The time required to validate signatures for inputs of length from
100,000 bytes to 1,000,000 bytes, using each of the private signing keys
you generated in the previous item.
5.  Explain how the results received in the previous items make sense,
and the implications for the time required for hashing, signing,
and validating, and the relations to the Hash-then-Sign paradigm
(subsection 3.2.6).

In your `Q3Files` directory, you will find input files for inputs starting from 100,000 bytes up to 1,000,000 bytes, all labeled accordingly.
