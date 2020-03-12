---
layout: tips
title: Cheat Sheets
---
Syscalls in x32 and x64
==========================
{% highlight bash%}
x86_32
+---------+------+------+------+------+------+------+
| syscall | arg0 | arg1 | arg2 | arg3 | arg4 | arg5 |
+---------+------+------+------+------+------+------+
|   %eax  | %ebx | %ecx | %edx | %esi | %edi | %ebp |
+---------+------+------+------+------+------+------+
offset_padding + system_addr + 4_bytes_padding + print_flag_cmd

x86_64
+---------+------+------+------+------+------+------+
| syscall | arg0 | arg1 | arg2 | arg3 | arg4 | arg5 |
+---------+------+------+------+------+------+------+
|   %rax  | %rdi | %rsi | %rdx | %r10 | %r8  | %r9  |
+---------+------+------+------+------+------+------+
offset_padding + pop_rdi_gadget + print_flag_cmd + system_addr
{% endhighlight %}
[Back to the top](#header)

Gdb/Gef
=======
{% highlight bash%}
b main                      :Break at main 
start                       :Start and break at the entry point
r                           :Run
vmmap                       :Show memory layout
info functions              :List functions
disassemble fonctions       :Show function

i r                         :Print register (not really necessary with gef)
x/20x $sp                   :Dump the stack starting at $sp
telescope $esp l30          :Dump the stack starting at $sp
x/4i $pc                    :Dump 4 instruction starting at $pc
b * 0x00                    :Break at 0x00

pattern create 200          :Create cyclic patterm
pattern search xxx          :Search for the patern xxx
pattern offset              :Get the offset based on the value off RSP/ESP
r < input                   :Injecting payload to input

#python2 -c 'import struct;print "A"*40 + struct.pack("Q",0x400883)+struct.pack("Q",0x601060)+struct.pack("Q",0x4005e0)' > input
#python2 -c 'from pwn import *;print("A" * 40 + p64(0x0400883) + p64(0x00601060) + p64(0x00400810))' > input
{% endhighlight %}
[Back to the top](#header)

Radare2
=======
{% highlight bash%}
aaaa                                        :Analyse the binary
afl                                         :List all functions
aflj                                        :List all functions in Json
aflj:{}                                     :List all functions in Json but with better formating
afl!exec                                    :List all functions containing "exec"
pdf @ function                              :Show the function
izz                                         :Show strings
izz~FLAG                                    :Show strings containing "FLAG"
axt 0x0000                                  :Show cross-reference of the address 0x0000
/a pop rdi, ret                             :Search for gadget pop rdi, ret
rabin2 -i <binary>                          :List fonctions in a binary
rabin2 -I <binary>                          :List protections and info about a binary
rabin2 -qs <binary> | grep -ve imp -e ' 0 ' :List fonctions in a binary in an easier format
rabin2 -z <binary>                          :Looking strings in a binary
{% endhighlight %}
[Back to the top](#header)
  
Metasploit shortcut
===================
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
sessions -l :list sessions
{% endhighlight %}

[Back to the top](#header)

VIM shortcut
=============
{% highlight bash%}
gg                                            :beginning of the document
G                                             :end of the document
dd                                            :delete line
yy                                            :copy line
p                                             :paste
u                                             :undo
.                                             :repeat last command
SHIFT-A                                       :append
gg dG                                         :delete all
gg " + y G                                    :yank all line 
:% y +                                        :yank all line (shorter)
:%!                                           :execute bash command (like "sort u")
:%s/patern_to_search/replace                  :replace text
:%!xargs -n1 -I{} sh -c 'echo{} | base64 -d'  :execute base64 -d on each line
|vim -                                        :send output to vim buffer
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

Tmux shortcut
=============
{% highlight bash%}
mysql -u root -p                  :login 
show databases;                   :show databases
use elk;                          :select a databas
show tables;                      :show tables
select * from alerts;             :show content of alert tables
show columns from alerts.elk;     :show coloumns of the table alerts in the database elk

Setting up mariadb and root password
------------------------------------
sudo apt install mariadb-server
sudo mysql -u root

#mysql commands:
use mysql;
update user set plugin='' where User='root';
flush privileges;
exit

#back to bash:
sudo systemctl restart mariadb.service
sudo mysql_secure_installation

#Python
mycursor.execute(CREATE DATABASE IF NOT EXISTS elk;)
mycursor.execute("CREATE TABLE IF NOT EXISTS alerts (id INT PRIMARY KEY, username VARCHAR(255),tags VARCHAR(255),url VARCHAR(255))")
mycursor.execute("INSERT IGNORE INTO alerts (id,username,tags,url) VALUES (%s,%s,%s,%s)",(ID, username, hashtags, link)) #IGNORE is to ignore the error generate by duplicate entry
mariadb_connection.commit() #dont forget to commit!

{% endhighlight %}
[Back to the top](#header)

Additional ressources
=======================

Gdb/Gef
-------
-[gef.readthedocs.io][link1]
-[github.com/hugsy/][link2]
-[cheat Sheet][link3]

Radare2
-------
-[radare.gitbooks.io][link4]

[Back to the top](#header)

[link1]:https://gef.readthedocs.io/en/master/commands/pattern/ 
[link2]:https://github.com/hugsy/gef
[link3]:https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
[link4]:https://radare.gitbooks.io/radare2book/debugger/migration.html
