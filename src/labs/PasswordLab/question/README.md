# Lab __ - Password Lab
This lab has 6 parts. 

## Question 1
Many users select weak passwords; for example, in 2020, the password **'123456’** was used by over 2 million users and exposed over 23 million times, check this [link](#). The file **MostCommonPWs** lists a few of the most common passwords.

As a Connecticut law-enforcement cybersec researcher, you are asked to help find the password to the account of **Benedict Arnold**, a dangerous criminal, in the darknet server of Benedict’s gang. Benedict’s username is simply his first name, **Benedict**. Since Benedict didn’t study cybersecurity and is known for cruelty rather than intelligence, you decide he is likely to use one of these very common passwords. So, try common passwords against the login program of the gang’s server, **Login.pyc**, to find out Benedict’s password. You can do this manually, easily, and it’s not a bad idea to do so as a warm-up exercise. However, you **should** write a (simple) Python script, **Break1.py**, that will find Benedict’s password by trying the different passwords against **Login.pyc**. Your program (**Break1.py**) should also print the time, at both the beginning and the end of the run; the runtime should be very short.

**Submit in your submissions folder**: (only) the password in file question1.

**Note:** the file **LoginTemplate.py** may help you understand how **Login.pyc** works; we created **Login.pyc** from it by replacing the string `##passwrd` with a random password from **MostCommonPWs**.

## Question 2

After breaking into Benedict’s phone, you found there a file, **gang**, that contains all usernames in the gang’s server. Surely few of these guys also use one of the common passwords in the file **MostCommonPWs**! Modify **Break1.py** into **Break2.py**, which will find another gang member who uses one of the passwords in **MostCommonPWs**, by using the login program **Login.pyc**.

**Submit in your submissions folder**: the name of the gang member and their password in file question2.

The format should be in csv format. ie:

```username,password```

## Question 3

Even when users do not use one of the obviously-weak passwords such as these in **MostCommonPWs**, they still often use commonly-used passwords. We now want to find passwords of an additional gang member, whose password is from the `dictionary’ of 100,000 common passwords, which you will find in the file **PwnedPWs100K** (downloaded from [https://haveibeenPwned.com](https://haveibeenPwned.com) – a useful resource, visit it!).

Modify **Break2.py** so that the modified program, **Break3.py**, will try out all of the passwords in **PwnedPWs100K**, for gang members whose password was not found yet. Run this modified program (**Break3**), see how long it takes to find the password for one gang member. Try to make your program efficient! Note: while in reality the passwords in the file are sorted by popularity, we pick them uniformly, i.e., each password is equally likely. Confirm the exposures using **Login.pyc**.

**Submit in your submissions folder**: (only) the name and password of one gang member exposed (only) in this question in file question3.

The format should be in csv format. ie:

```username,password```

## Question 4

Often, attackers get hold of a leaked file of passwords, and use it to break into accounts of the user at other services, where the users reused the same passwords; this is called `credential stuffing attack`. There were billions of passwords exposed in the recent years, and the numbers seem to even grow over time. Attackers often use a password file exposed from one service/site, to break into accounts of the same users in another service/site – since many users use the same password in multiple sites.

In this question, you will use this technique to find the passwords of additional gang members, where the techniques of previous questions failed. In fact, these will be quite random passwords. You receive an exposed passwords file, **PwnedPWfile**, and will write a program, **Break4.py**, that will search for gang members who have an account (and password) in the file. For any gang members whose passwords are listed in **PwnedPWfile**, **Break4** will check if the password `works` against the login program **Login.py**.

**Submit in your submissions folder**: (only) the name and password of one gang member exposed (only) in this question in file question4.

The format should be in csv format. ie:

```username,password```

## Question 5

To reduce the exposure from a leaked passwords file, password files are usually kept in a form which makes it easy to check if a given string is the correct password (of a given user), but harder to find the passwords given only the file. In this question, we discuss the more basic form of this defense, where the file contains the hashed passwords. You are given another exposed passwords file, **HashedPWs**, which contains, for each user x, the results of applying a cryptographic hash function h(.) to the password PW x of user x, i.e., h(PW x). (In the next question, we will see an improved defense.)

**Cryptographic hash functions h(.)** are efficient functions mapping from arbitrary-long strings into short, fixed-length strings, e.g., 160 bits. They have many applications and several security requirements. The application of making it harder to abuse an exposed passwords file relies on the one-way property, which basically says that given h(pw), the hash of a password pw, should not help the attacker to find pw (or any other password pw’ which will hash to the same value, i.e., h(pw’)=h(pw)).

Write a new program, **Break5.py**, that uses the file **HashedPWs** to find, as quickly as possible, the passwords of these additional gang members. It will be infeasible to test all random passwords (why?); instead, focus on gang members who pick a random password from **PwnedPWs100K**, and concatenate to it two random digits. (Many users do such minor tweaks to their passwords, to bypass password-choice requirements, or in the incorrect hope that this suffices to prevent password guessing.). For gang members whose passwords you recover using **HashedPWs**, use **Login.pyc** to check if the gang member used the same password.

**Submit in your submissions folder**: (only) the name and password of one gang member exposed (only) in this question in file question5.

The format should be in csv format. ie:

```username,password```
**Hint:** think carefully about how to do this efficiently, or it may be quite slow (which may be annoying, and may result in a lower grade).

## Question 6

To further improve security, password files usually do not contain the hash of the password PW x of user x. Instead, the password file contains two values for each user x: a random value salt x, called salt, and the result of hashing a combination of the password PW x and of the salt. In this question, you are given a file **SaltedPWs** which contains, for each user x, the pair (salt x, h(salt x + PW x + PW x)), where salt x is a random value chosen for user x. Here we use the + sign to denote concatenation.

Write a new program, **Break6.py**, that uses the file **SaltedPWs** to find the passwords of as many additional gang members as possible that use passwords from **PwnedPWs100K** concatenated with one random digit, as quickly as possible. **Break6** should also save a file containing the names and corresponding passwords. Confirm the exposures using **Login.pyc**.

**Submit in your submissions folder**: (only) the name and password of one gang member exposed (only) in this question in file question6.

The format should be in csv format. ie:

```username,password```
