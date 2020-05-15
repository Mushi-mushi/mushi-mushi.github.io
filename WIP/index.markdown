---
layout: post
title:  "A very, very  basic intro to malware analysis using R2"
date:   09-02-2020 13:34:34
categories: malware
tags: Malware R2 Radare2
---

So since I haven't wrote any blog post here for a while and that a friend of mine asked for some pointer on malware analysis using Radare2, I though I would give a that a try!

First of all, I only used R2 a couple of time before so I'll mostly follow what is showed in this [presentation][link1]. The goal here is to rely a maximum on R2 and avoid any other tool for learning purposes.

So let's begin by checking if the sample is packed/encrypted. We can easily get the entrhopi of the file by first loading the sample into R2 and typing the following command:
{% highlight bash%}
root@kali:~/sample# r2 -n sample.bin 
[0x00000000]> ph entropy $s
5.316590
{% endhighlight %}
or simply 
{% highlight bash%}
root@kali:~/sample# r2 -qfnc "ph entropy" sample.bin 
5.316590
{% endhighlight %}
Now it could be interesting to look at the entropy per sections, whish luckely R2 enable us to do easily !
{% highlight bash%}
root@kali:~/sample# r2 sample.bin 
[0x004014a0]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[x] Enable constraint types analysis for variables
[0x004014a0]> iS
[Sections]
Nm Paddr       Size Vaddr      Memsz Perms Name
00 0x00000400  7680 0x00401000  8192 -r-x .text
01 0x00002200   512 0x00403000  4096 -rw- .data
02 0x00002400  2048 0x00404000  4096 -r-- .rdata
03 0x00000000     0 0x00405000  4096 -rw- .bss
04 0x00002c00  2048 0x00406000  4096 -rw- .idata
05 0x00003400   512 0x00407000  4096 -rw- .CRT
06 0x00003600   512 0x00408000  4096 -rw- .tls

[0x004014a0]> iS entropy
[Sections]
Nm Paddr       Size Vaddr      Memsz Perms Checksum          Name
00 0x00000400  7680 0x00401000  8192 -r-x entropy=5.90224208 .text
01 0x00002200   512 0x00403000  4096 -rw- entropy=0.57814914 .data
02 0x00002400  2048 0x00404000  4096 -r-- entropy=5.00207308 .rdata
03 0x00000000     0 0x00405000  4096 -rw- entropy=0.00000000 .bss
04 0x00002c00  2048 0x00406000  4096 -rw- entropy=4.18768876 .idata
05 0x00003400   512 0x00407000  4096 -rw- entropy=0.27482548 .CRT
06 0x00003600   512 0x00408000  4096 -rw- entropy=0.00000000 .tls

[0x004014a0]> 
{% endhighlight %}
Since the entropy reported is always under 7, the chances of the sample to be packed and/or encrypted is pretty low at this point. Next, let's take a look at the header to see what kind of binary that is. Checking the header in R2 can be done either by typing i(a bit easier to read) or ih:
{% highlight bash%}
[0x004014a0]> i
blksz    0x0
block    0x100
fd       3
file     sample.bin
format   pe
iorw     false
mode     r-x
size     0x3800
humansz  14K
type     EXEC (Executable file)
arch     x86
baddr    0x400000
binsz    14336
bintype  pe
bits     32
canary   false
retguard false
sanitiz  false
class    PE32
cmp.csum 0x000046bf
compiled Thu Jan  1 04:00:00 1970
crypto   false
endian   little
havecode true
hdr.csum 0x000046bf
laddr    0x0
linenum  true
lsyms    true
machine  i386
maxopsz  16
minopsz  1
nx       false
os       windows
overlay  false
pcalign  0
pic      false
relocs   true
signed   false
static   false
stripped false
subsys   Windows GUI
va       true
{% endhighlight %}
Here we learn that this a windows (os windows) executable file (type EXEC) for 32bits (arch x86 and bits32) which apparently has been compiled on Thu Jan  1 04:00:00 1970(that can be manipulated though). We can also see that executable-space protection is disable (nx false) although since this is a malware and not a crackme challenge this is probably not that relevant at this point. That being said looking back at the section permission could potentially give us additional information:
{% highlight bash%}
Nm Paddr       Size Vaddr      Memsz Perms Name
00 0x00000400  7680 0x00401000  8192 -r-x .text
01 0x00002200   512 0x00403000  4096 -rw- .data
02 0x00002400  2048 0x00404000  4096 -r-- .rdata
03 0x00000000     0 0x00405000  4096 -rw- .bss
04 0x00002c00  2048 0x00406000  4096 -rw- .idata
05 0x00003400   512 0x00407000  4096 -rw- .CRT
06 0x00003600   512 0x00408000  4096 -rw- .tls
{% endhighlight %}
For example, if the .text section was writable, we could have a sample that self modified itself, which is pretty rare in legitimate application. However this is not the case here.



[link1]:https://www.youtube.com/watch?v=DnZLy_sq-nY&feature=emb_logo
