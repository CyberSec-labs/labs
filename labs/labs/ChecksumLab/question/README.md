# Lab 3 - Checksum Lab
This lab has three parts. 
You're also given the file Internet_Checksum.py. This file contains the method toInternetChecksum(s: string). It returns a string, which is the hash of the string.

## Question 1
For question 1, locate the following files in the `q1` subdirectory:

 - f1a.txt
 - h1a.txt
 - f1b.txt
 - h1b.txt

h1a.txt is the internet checksum hash of f1a.txt. Your task is to find the internet checksum of f1b.txt and place it in h1b.txt. 

You can use f1a.txt and h1a.txt to make sure your code is correct. 

Submit h1b.txt in your submission folder.

## Question 2
For question 2, locate the following files in your `q2` subdirectory:

- f2a.txt
- f2b.txt
- h2.txt

f2a has some randomly generated string, while h2 and f2b are both blank. 

Your goal is to find some string that is different from f2a, but produces the same internet checksum hash. This is a hash collision.

Submit both the matching hash h2b.txt, and f2b.txt in your submissions folder.

## Question 3
For question 3, locate the following files in your `q3` subdirectory:

- f3a.txt
- h3a.txt

You will find that f3a.txt has 25 randomly generated characters on line 1, followed by "replace this with your matching string" on line 2. Proceeded by 25 more randomly generated characters on line 3. 

h3a.txt is the hash of this entire file (f3a.txt) in internet checksum.

Your goal is to write a program that replaces the second line with a different string while still producing the same hash result given in h3a.txt, which is the initial hash of the file f3a.txt.

Submit your modified f3a.txt file.

## Question 4
For question 3, locate the following files in your `q4` subdirectory:

- f4b.html

Opening up f4b in the browser, you see a simple web page with some text on it.

Your goal is to change how the webpage functions. 

Open the file in your code editor of choice and locate the `<script>` tag. 

You will see an if statement in it. You want to change that so that the overall checksum of the file is the same, but the if statement fails. If the if statement evaluates to false, something else should be displayed on the webpage instead. That is your goal. 

Submit your modified f4b.html file in your submissions folder when finished. 
