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
- h3.txt

You will find that f3a.txt consists of three lines of text. However, you will only want to edit the second line of the file by replacing the text that is there with your own string. 

h3.txt is the hash of this entire file (f3a.txt) in internet checksum.

Your goal is to write a program that creates the file f3b.txt, which is identical to f3a.txt besides the second line and should have the same checksum value. 

Submit your f3b.txt file.

## Question 4
For question 3, locate the following files in your `q4` subdirectory:

- f4a.html

Opening up f4a in the browser, you see a simple web page with some text on it.

Your goal is to change how the webpage functions. 

Open the file in your code editor of choice and locate the `<script>` tag. 

You will see an if statement in it. You want to change that so that the overall checksum of the file is the same, but the if statement fails. If the if statement evaluates to false, something else should be displayed on the webpage instead. That is your goal. 

You will submit f4b.html, which will be your modified version of f4a.html.
