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
pattern create 200          :Create cyclic patterm
pattern offset              :Get the offset based on the value off RSP/ESP
info functions              :List fonctions
break * 0x00                :Break at 0x00

#python2 -c 'import struct;print "A"*40 + struct.pack("Q",0x400883)+struct.pack("Q",0x601060)+struct.pack("Q",0x4005e0)' > input
#python2 -c 'from pwn import *;print("A" * 40 + p64(0x0400883) + p64(0x00601060) + p64(0x00400810))' > input

r < input                   :Injecting payload to input
{% endhighlight %}
[Back to the top](#header)

Radar2
=======
{% highlight bash%}
aaaa                                        :Analyse the binary
afl                                         :List all fonctions
aflj                                        :List all fonctions in Json
aflj:{}                                     :List all fonctions in Json but with better formating
pdf @ function                              :Show the fonction
iz                                          :Show strings
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
gg            :beginning of the document
G             :end of the document
dd            :delete line
yy            :copy line
p             :paste
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

Additional ressources
=======================
Gdb/Gef
-------
[link1]:https://gef.readthedocs.io/en/master/commands/pattern/ 
[link2]:https://github.com/hugsy/gef
