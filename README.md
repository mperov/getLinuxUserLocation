# getLinuxUserLocation
Using this project you may check location of each user which is connected to your Linux server.

## How to start
1. Get project:
```console
$ git clone https://github.com/mperov/getLinuxUserLocation.git
$ cd getLinuxUserLocation/
```
2. Create special Python virtual enviroment by
```console
$ sudo apt-get install python3-venv -y
$ python3 -m venv getLinuxUserLocation
$ source getLinuxUserLocation/bin/activate
```
3. Next install some Python modules - `pip3 install -r requirements` or `python3 -m pip install -r requirements`  
If you don't have pip3 then you may install it [how described here](https://pip.pypa.io/en/stable/installation/)
4. Generate public and private ssh keys **without password** via `ssh-keygen -t rsa`
5. Add public key to remote server using `ssh-copy-id -i ~/.ssh/id_rsa.pub -p SSH_PORT YOUR_USER_NAME@IP_ADDRESS_OF_THE_SERVER`
6. On remote machine change `/etc/sudoers` file to run sudo commands without password. For it `/etc/sudoers` should contain line like this `coder ALL=(ALL:ALL) NOPASSWD: ALL`
7. Copy script `whereFrom` to remote server to `/opt/` directory, e.g. `scp -p 22 ./ubuntu/whereFrom root@192.168.1.5:/opt/whereFrom`.  
In this project there are some files `whereFrom`, for Ubuntu, CentOS and for openVPN server. Choose your variante.

## Usage
1. Load virtual enviroment
```console
$ source getLinuxUserLocation/bin/activate
```
2. Get location list
```console
$ ./getLocation.py -hi 192.168.1.5 -u coder -p 10028 -k /home/coder/.ssh/id_rsa -o
```   
option `-o` means that remote server has old operating system, e.g. CentOS 7.9

By the way, there is help output:
```console
$ ./getLocation.py -h
usage: getLocation.py [-h] [-hi HOSTIP] [-p PORT] [-u USER] [-k KEY] [-d] [-o]

optional arguments:
  -h, --help            show this help message and exit
  -hi HOSTIP, --hostIP HOSTIP
                        contain IP address your server
  -p PORT, --port PORT  contain ssh port
  -u USER, --user USER  contain username with sudo rules
  -k KEY, --private-key KEY
                        contain path to private key file
  -d, --debug           this option enables debug mode
  -o, --old             this option for old Linux distributions
```
