
# Lab 5 - TLS Lab

In this lab students will attempt to connect a TLS client to a server.

You need to have a linux machine with openssl installed. On a windows machine, you can use WSL to quickly meet this requirement. We recommend Ubuntu as your linux distro.

## Question 1

For question 1, locate the following files in your given folder:

 - server.py
 - client.py

For question one you'll want to hold off on any modifications to server.py. Instead, just run it using 
```bash
python server.py
```

Your task for this section is to open `client.py` and write the code to connect the client to the server.

To do this, write some code at the bottom of client.py.
You will want to connect the client with each of the keys and certificates in the directories given to you.
You should also print the results of the connection with each certificate. 

Run your code in a separate terminal with

```bash
python client.py
```

## Section 2
Now that your client connects to the server and (should) iterate through each set of certificates, you should notice that 3 of the 9 certificates pass, with the other 6 failing.

Here is some information on the failing certs.
* one certificate should have failed due to being expired
* one certificate should have failed due to being used in an unsupported way
* two certificates should have failed due to an unknown CA authority
* one certificate should have failed due to MD5 hash being too weak
* one certificate should have failed due to an unknown, critical extension

The goal of this lab is to submit, as a solution, the directories of the certificates in order.

Your solutions file will be a list of the directories of each certificate in a specific order, with an underscore seperating each of them. 

The order is as follows:

* valid_cert_dir
* expired_cert_dir
* invalid_self_signed_ca_cert_dir
* invalid_cn_cert_dir
* md5_cert_dir
* unknown_ext_cert_dir
* incorrect_usage_cert_dir
* invalid_san_cert_dir
* invalid_chain_cert_dir

Based off this order, we know out of the 3 certificates that are returning valid, 2 are actually still invalid. Keep that in mind for now. 

Looking at the return values for each of the certificates, we already know the following certificates:

* expired_cert_dir
* md5_cert_dir
* unknown_ext_cert_dir
* incorrect_usage_cert_dir

Next lets investigate the two certificates that are failing.
One is failing due to an invalid chain, while the other is failing since it was self signed (not signed by a valid CA)
To determine which is which, we can view the error messages on the terminal where we are running the server.
One error message distinctly shows that a certificate is self signed, and the other shows that it was unable to get the local issuer certificate for the certificate chain.
With this knowledge, you know also know:

* invalid_self_signed_ca_cert_dir
* invalid_chain_cert_dir


## Section 3
Now, we just need to figure out of the last 3 which is which: 
* invalid_cn_cert_dir
* invalid_san_cert_dir
* valid
