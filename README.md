#Mural Way-finding by ByteMe
#####Authors: Isaac Lance, Justin Robles, Jeremiah Clothier, Petter Lovett, Noah Palmer, Jeanie Chen, Wyatt Reed
###Requirements
* python 3.6
* pip3
* MongoDB database
* AWS Account using S3

##Credentials.py
This file holds all your credentials like passwords etc.

[MongoDB Info](https://docs.mongodb.com/tutorials/connect-to-mongodb-python/)

DB_USER = "MongoDB user name"

DB_PASSWORD = "MongoDB password"

DB_DOMAIN = "Address of MongoDB Instance" 

[AWS Info](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html)

AWSAccessKeyId ='Account ID'

AWSSecretKey = 'Account PW'

###Site admin login and password:
ADMIN_ID = "desired username"

ADMIN_PW = "desired pass"

###To run the site locally:
In the command line:

Setup:

    git clone https://github.com/Hack4Eugene/mural-way-finding-by-byte-me.git

In the new directory created by clone:
    
    sudo pip3 install -r requirements.txt
    python3 flask_main.py

###To add admin to the site:
    python3 flask_main.py adminsetup
This will take your ADMIN\_ID and ADMIN\_PW and create a valid login for the admin tools on the site.
To update password, just use an existing ADMIN\_ID with a new ADMIN\_PW

Depending on need, this can easily be extended to allow for regular user accounts, and creating admins directly on the site.
We expect a fairly small amount of admin accounts would be created for this application.