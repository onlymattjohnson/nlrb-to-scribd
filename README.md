nlrb-to-scribd
==============

A script to upload documents from the National Labor Relations Board to Scribd

Resources
---------
I will be using some of these resources, I imagine:
* https://code.google.com/p/python-scribd/
* http://docs.python.org/2/library/xml.etree.elementtree.html

Install
=======

MongoDB
-------
We will need to install mongodb to keep track of the files already uploaded.  This will document the process in Ubuntu Server, but you can find more detailed instructions here http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list

sudo apt-get update

sudo apt-get install mongodb-10gen

Config MongoDB
--------------
Enter mongo shell by typing ```mongo```

```use nlrb```


