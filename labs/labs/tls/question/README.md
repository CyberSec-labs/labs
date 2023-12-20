# SSL/TLS Lab

In this lab students will attempt to connect a TLS client to a server.

You need to have a linux machine with openssl installed

Most of the server code is given to you.
You can run this as is with

```bash
python3 server.py
```

Now your next goal is going to be to connect the TLS client to the server.

To do this, write some code at the bottom of client.py that will do so.
You will want to connect the client with each of the keys and certificates in the directories given to you.

Run your code in a separate terminal with

```bash
python3 client.py
```

Once you do that, you should now have three certificates passing, and six failing.

At this point:
* one certificate should have failed due to being expired
* one certificate should have failed due to being used in an unsupported way
* two certificates should have failed due to an unknown CA authority
* one certificate should have failed due to MD5 hash being too weak
* one certificate should have failed due to an unknown, critical extension
* three certificates should be passing at this point

The goal of this lab is to submit, as a solution, the directories of the certificates in order.
The specific order is as follows:

```<correct_cert>_<expired_cert>_<invalid_cert>_<invalid_cn>_<invalid_md5>_...```

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

We already know at this point, the following certificates:

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

And we only have left to investigate:
* invalid_cn_cert_dir
* invalid_san_cert_dir
* valid

Now to determine which of the three certificates passing is valid, and which contains an invalid_cn, and which contains the invalid_san, we must modify the code in server.py
Go ahead and kill the process where the server is running with control C in that terminal.

In server.py, there is a function where you must return False to reject certificates that have an invalid CN for a client that was blacklisted, or an invalid SAN.

Complete this function and reject all connections with a CN of invalid_client or a SAN of "DNS:invalid_san.com",

Run server.py once more with

```bash
python3 server.py
```

Run client.py once more with

```bash
python3 client.py
```

Submit your solution as described above and again here:

```<correct_cert>_<expired_cert>_<invalid_cert>_<invalid_cn>_<invalid_md5>_...```

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

Good luck and have fun!
