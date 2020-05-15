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
There is as well the p==e @section..rdata command that gives you a visual representation of entropy but I don't really know how to interpret that though... Since the entropy reported is always under 7, the chances of the sample to be packed and/or encrypted is pretty low at this point. Next, let's take a look at the header to see what kind of binary that is. Checking the header in R2 can be done either by typing i(a bit easier to read) or ih:
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

Now we can check the imported functions of the sample by simply typing ii:
{% highlight bash%}
[0x004014a0]> ii
[Imports]
Num  Vaddr       Bind      Type Name
   1 0x00406150    NONE    FUNC ADVAPI32.dll_RegCloseKey
   2 0x00406154    NONE    FUNC ADVAPI32.dll_RegCreateKeyA
   3 0x00406158    NONE    FUNC ADVAPI32.dll_RegOpenKeyExA
   4 0x0040615c    NONE    FUNC ADVAPI32.dll_RegQueryValueExA
   5 0x00406160    NONE    FUNC ADVAPI32.dll_RegSetValueExA
   1 0x00406168    NONE    FUNC KERNEL32.dll_AllocConsole
   2 0x0040616c    NONE    FUNC KERNEL32.dll_DeleteCriticalSection
   3 0x00406170    NONE    FUNC KERNEL32.dll_EnterCriticalSection
   4 0x00406174    NONE    FUNC KERNEL32.dll_GetCurrentProcess
   5 0x00406178    NONE    FUNC KERNEL32.dll_GetCurrentProcessId
   6 0x0040617c    NONE    FUNC KERNEL32.dll_GetCurrentThreadId
   7 0x00406180    NONE    FUNC KERNEL32.dll_GetLastError
   8 0x00406184    NONE    FUNC KERNEL32.dll_GetStartupInfoA
   9 0x00406188    NONE    FUNC KERNEL32.dll_GetSystemTimeAsFileTime
  10 0x0040618c    NONE    FUNC KERNEL32.dll_GetTickCount
  11 0x00406190    NONE    FUNC KERNEL32.dll_InitializeCriticalSection
  12 0x00406194    NONE    FUNC KERNEL32.dll_LeaveCriticalSection
  13 0x00406198    NONE    FUNC KERNEL32.dll_QueryPerformanceCounter
  14 0x0040619c    NONE    FUNC KERNEL32.dll_SetUnhandledExceptionFilter
  15 0x004061a0    NONE    FUNC KERNEL32.dll_Sleep
  16 0x004061a4    NONE    FUNC KERNEL32.dll_TerminateProcess
  17 0x004061a8    NONE    FUNC KERNEL32.dll_TlsGetValue
  18 0x004061ac    NONE    FUNC KERNEL32.dll_UnhandledExceptionFilter
  19 0x004061b0    NONE    FUNC KERNEL32.dll_VirtualProtect
  20 0x004061b4    NONE    FUNC KERNEL32.dll_VirtualQuery
   1 0x004061bc    NONE    FUNC msvcrt.dll___getmainargs
   2 0x004061c0    NONE    FUNC msvcrt.dll___initenv
   3 0x004061c4    NONE    FUNC msvcrt.dll___lconv_init
   4 0x004061c8    NONE    FUNC msvcrt.dll___p__acmdln
   5 0x004061cc    NONE    FUNC msvcrt.dll___p__fmode
   6 0x004061d0    NONE    FUNC msvcrt.dll___set_app_type
   7 0x004061d4    NONE    FUNC msvcrt.dll___setusermatherr
   8 0x004061d8    NONE    FUNC msvcrt.dll__amsg_exit
   9 0x004061dc    NONE    FUNC msvcrt.dll__cexit
  10 0x004061e0    NONE    FUNC msvcrt.dll__initterm
  11 0x004061e4    NONE    FUNC msvcrt.dll__iob
  12 0x004061e8    NONE    FUNC msvcrt.dll__onexit
  13 0x004061ec    NONE    FUNC msvcrt.dll_abort
  14 0x004061f0    NONE    FUNC msvcrt.dll_calloc
  15 0x004061f4    NONE    FUNC msvcrt.dll_exit
  16 0x004061f8    NONE    FUNC msvcrt.dll_fclose
  17 0x004061fc    NONE    FUNC msvcrt.dll_fopen
  18 0x00406200    NONE    FUNC msvcrt.dll_fprintf
  19 0x00406204    NONE    FUNC msvcrt.dll_fputc
  20 0x00406208    NONE    FUNC msvcrt.dll_free
  21 0x0040620c    NONE    FUNC msvcrt.dll_fwrite
  22 0x00406210    NONE    FUNC msvcrt.dll_malloc
  23 0x00406214    NONE    FUNC msvcrt.dll_memcpy
  24 0x00406218    NONE    FUNC msvcrt.dll_signal
  25 0x0040621c    NONE    FUNC msvcrt.dll_strlen
  26 0x00406220    NONE    FUNC msvcrt.dll_strncmp
  27 0x00406224    NONE    FUNC msvcrt.dll_vfprintf
   1 0x0040622c    NONE    FUNC USER32.dll_FindWindowA
   2 0x00406230    NONE    FUNC USER32.dll_GetAsyncKeyState
   3 0x00406234    NONE    FUNC USER32.dll_ShowWindow
{% endhighlight %}
As I tend to be very protective of my registry, the following functions are usually something I don't like to see in a sample:
RegCloseKey,RegCreateKeyA,RegOpenKeyExA,RegQueryValueExA,RegSetValueExA. Indeed editing registry keys is a popular trick for malware to maintain persistence as documented in the [ATTACK Mittre Matrix][link2].

We can also see that the sleep function was imported which is sometimes use as an evasion[technique][link3]

The function GetAsyncKeyState is also imported which is often tied to key logging [capabilities][link4]

Finally we don't see any functions related to network traffic such as inet or socket. There is however a ShowWindow function which seems a bit unusual in malware sample ...

Moving on ! Let's look at the string:
{% highlight bash%}
[0x004014a0]> iz
[Strings]
Num Paddr      Vaddr      Len Size Section  Type  String
000 0x00002400 0x00404000  18  19 (.rdata) ascii ConsoleWindowClass
001 0x00002413 0x00404013  23  24 (.rdata) ascii c:\%windir%\svchost.exe
002 0x0000242e 0x0040402e  11  12 (.rdata) ascii svchost.log
003 0x0000243a 0x0040403a   7   8 (.rdata) ascii [SHIFT]
004 0x00002442 0x00404042   8   9 (.rdata) ascii \n[ENTER]
005 0x0000244b 0x0040404b  11  12 (.rdata) ascii [BACKSPACE]
006 0x00002457 0x00404057   5   6 (.rdata) ascii [TAB]
007 0x0000245d 0x0040405d   6   7 (.rdata) ascii [CTRL]
008 0x00002464 0x00404064   5   6 (.rdata) ascii [DEL]
009 0x0000246a 0x0040406a   4   5 (.rdata) ascii [;:]
010 0x0000246f 0x0040406f   4   5 (.rdata) ascii [/?]
011 0x00002474 0x00404074   4   5 (.rdata) ascii [`~]
012 0x00002479 0x00404079   6   7 (.rdata) ascii [ [{ ]
013 0x00002480 0x00404080   4   5 (.rdata) ascii [\|]
014 0x00002485 0x00404085   6   7 (.rdata) ascii [ ]} ]
015 0x0000248c 0x0040408c   4   5 (.rdata) ascii ['"]
016 0x00002491 0x00404091  11  12 (.rdata) ascii [CAPS LOCK]
017 0x00002738 0x00404338  45  46 (.rdata) ascii SOFTWARE\Microsoft\Windows\CurrentVersion\Run
018 0x00002766 0x00404366   7   8 (.rdata) ascii svchost
019 0x00002794 0x00404394  13  14 (.rdata) ascii Unknown error
020 0x000027a4 0x004043a4  42  43 (.rdata) ascii _matherr(): %s in %s(%g, %g)  (retval=%g)\n
021 0x000027d0 0x004043d0  30  31 (.rdata) ascii Argument domain error (DOMAIN)
022 0x000027ef 0x004043ef  27  28 (.rdata) ascii Argument singularity (SIGN)
023 0x0000280c 0x0040440c  31  32 (.rdata) ascii Overflow range error (OVERFLOW)
024 0x0000282c 0x0040442c  53  54 (.rdata) ascii The result is too small to be represented (UNDERFLOW)
025 0x00002864 0x00404464  34  35 (.rdata) ascii Total loss of significance (TLOSS)
026 0x00002888 0x00404488  36  37 (.rdata) ascii Partial loss of significance (PLOSS)
027 0x000028c8 0x004044c8  27  28 (.rdata) ascii Mingw-w64 runtime failure:\n
028 0x000028e4 0x004044e4  31  32 (.rdata) ascii Address %p has no image-section
029 0x00002904 0x00404504  48  49 (.rdata) ascii   VirtualQuery failed for %d bytes at address %p
030 0x00002938 0x00404538  38  39 (.rdata) ascii   VirtualProtect failed with code 0x%x
031 0x00002960 0x00404560  49  50 (.rdata) ascii   Unknown pseudo relocation protocol version %d.\n
032 0x00002994 0x00404594  41  42 (.rdata) ascii   Unknown pseudo relocation bit size %d.\n
033 0x000029c0 0x004045c0  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
034 0x000029d4 0x004045d4  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
035 0x000029e8 0x004045e8  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
036 0x000029fc 0x004045fc  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
037 0x00002a10 0x00404610  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
038 0x00002a24 0x00404624  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
039 0x00002a38 0x00404638  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
040 0x00002a4c 0x0040464c  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
041 0x00002a60 0x00404660  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
042 0x00002a74 0x00404674  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
043 0x00002a88 0x00404688  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
044 0x00002a9c 0x0040469c  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
045 0x00002ab0 0x004046b0  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
046 0x00002ac4 0x004046c4  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
047 0x00002ad8 0x004046d8  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
048 0x00002aec 0x004046ec  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
049 0x00002b00 0x00404700  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
050 0x00002b14 0x00404714  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
051 0x00002b28 0x00404728  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
052 0x00002b3c 0x0040473c  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
053 0x00002b50 0x00404750  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
054 0x00002b64 0x00404764  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
055 0x00002b78 0x00404778  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
056 0x00002b8c 0x0040478c  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
057 0x00002ba0 0x004047a0  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
058 0x00002bb4 0x004047b4  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
059 0x00002bc8 0x004047c8  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
060 0x00002bdc 0x004047dc  16  17 (.rdata) ascii GCC: (GNU) 9.2.0
{% endhighlight %}

Here we can see some strange strings related to keyboard keys ([TAB][DEL][CTRL]) as well as a windows registry key SOFTWARE\Microsoft\Windows\CurrentVersion\Run often use for persistence. We can also see scvhost.exe mentionned a couple of time. The rest of the string after line 20 have been added by the compiler.  

We can also look at strings located in specific sections of the sample:
{% highlight bash%}
[0x004014a0]> px @section..data
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00403000  0a00 0000 f02d 4000 ffff ffff ffff ffff  .....-@.........
0x00403010  ff00 0000 0200 0000 ffff ffff a02d 4000  .............-@.
0x00403020  b02d 4000 c02d 4000 4ee6 40bb b119 bf44  .-@..-@.N.@....D
0x00403030  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403040  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403050  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403060  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403070  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403080  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x00403090  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030a0  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030b0  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030c0  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030d0  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030e0  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x004030f0  0000 0000 0000 0000 0000 0000 0000 0000  ................
[0x004014a0]> px @section..rdata
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00404000  436f 6e73 6f6c 6557 696e 646f 7743 6c61  ConsoleWindowCla
0x00404010  7373 0063 3a5c 2577 696e 6469 7225 5c73  ss.c:\%windir%\s
0x00404020  7663 686f 7374 2e65 7865 0061 2b00 7376  vchost.exe.a+.sv
0x00404030  6368 6f73 742e 6c6f 6700 5b53 4849 4654  chost.log.[SHIFT
0x00404040  5d00 0a5b 454e 5445 525d 005b 4241 434b  ]..[ENTER].[BACK
0x00404050  5350 4143 455d 005b 5441 425d 005b 4354  SPACE].[TAB].[CT
0x00404060  524c 5d00 5b44 454c 5d00 5b3b 3a5d 005b  RL].[DEL].[;:].[
0x00404070  2f3f 5d00 5b60 7e5d 005b 205b 7b20 5d00  /?].[`~].[ [{ ].
0x00404080  5b5c 7c5d 005b 205d 7d20 5d00 5b27 225d  [\|].[ ]} ].['"]
0x00404090  005b 4341 5053 204c 4f43 4b5d 0000 0000  .[CAPS LOCK]....
0x004040a0  9e19 4000 c119 4000 e419 4000 071a 4000  ..@...@...@...@.
0x004040b0  2a1a 4000 4d1a 4000 701a 4000 931a 4000  *.@.M.@.p.@...@.
0x004040c0  b31a 4000 d31a 4000 231b 4000 231b 4000  ..@...@.#.@.#.@.
0x004040d0  231b 4000 231b 4000 231b 4000 231b 4000  #.@.#.@.#.@.#.@.
0x004040e0  231b 4000 231b 4000 231b 4000 231b 4000  #.@.#.@.#.@.#.@.
0x004040f0  231b 4000 231b 4000 231b 4000 231b 4000  #.@.#.@.#.@.#.@.
[0x004014a0]> px @section..text
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00401000  c38d b426 0000 0000 8db4 2600 0000 0090  ...&......&.....
0x00401010  83ec 1c31 c066 813d 0000 4000 4d5a c705  ...1.f.=..@.MZ..
0x00401020  8c53 4000 0100 0000 c705 8853 4000 0100  .S@........S@...
0x00401030  0000 c705 8453 4000 0100 0000 c705 2850  .....S@.......(P
0x00401040  4000 0100 0000 7518 8b15 3c00 4000 81ba  @.....u...<.@...
0x00401050  0000 4000 5045 0000 8d8a 0000 4000 7450  ..@.PE......@.tP
0x00401060  a30c 5040 00a1 9453 4000 85c0 7532 c704  ..P@...S@...u2..
0x00401070  2401 0000 00e8 021d 0000 e805 1d00 008b  $...............
0x00401080  15a8 5340 0089 10e8 e40c 0000 833d 1830  ..S@.........=.0
0x00401090  4000 0174 4b31 c083 c41c c38d 7426 0090  @..tK1......t&..
0x004010a0  c704 2402 0000 00e8 d01c 0000 ebcc 6690  ..$...........f.
0x004010b0  0fb7 5118 6681 fa0b 0174 3d66 81fa 0b02  ..Q.f....t=f....
0x004010c0  759e 83b9 8400 0000 0e76 958b 91f8 0000  u........v......
0x004010d0  0031 c085 d20f 95c0 eb86 8db6 0000 0000  .1..............
0x004010e0  c704 24d0 1f40 00e8 f413 0000 31c0 83c4  ..$..@......1...
0x004010f0  1cc3 8db6 0000 0000 8379 740e 0f86 5eff  .........yt...^.
{% endhighlight %}
Unfortunately not much additional info there ... Do let's move the fun part and look at the assembly code.
{% highlight bash%}
[0x00403030]> s main
[0x00401530]> pdf
/ (fcn) main 135
|   main ();
|           ; var int local_1ch @ ebp-0x1c
|           ; var int local_18h @ ebp-0x18
|           ; var int local_14h @ ebp-0x14
|           ; var int local_10h @ ebp-0x10
|           ; var int local_ch @ ebp-0xc
|           ; var int local_4h_2 @ ebp-0x4
|           ; var int local_4h @ esp+0x4
|           ; CALL XREF from section..text (+0x381)
|           0x00401530      8d4c2404       lea ecx, dword [local_4h]   ; 4
|           0x00401534      83e4f0         and esp, 0xfffffff0
|           0x00401537      ff71fc         push dword [ecx - 4]
|           0x0040153a      55             push ebp
|           0x0040153b      89e5           mov ebp, esp
|           0x0040153d      51             push ecx
|           0x0040153e      83ec34         sub esp, 0x34               ; '4'
|           0x00401541      e8fa070000     call fcn.00401d40
|           0x00401546      a168614000     mov eax, dword sym.imp.KERNEL32.dll_AllocConsole ; [0x406168:4]=0x6290 reloc.KERNEL32.dll_AllocConsole
|           0x0040154b      ffd0           call eax
|           0x0040154d      c74424040000.  mov dword [local_4h], 0
|           0x00401555      c70424004040.  mov dword [esp], str.ConsoleWindowClass ; section..rdata ; [0x404000:4]=0x736e6f43 ; "ConsoleWindowClass"
|           0x0040155c      a12c624000     mov eax, dword sym.imp.USER32.dll_FindWindowA ; [0x40622c:4]=0x6562 reloc.USER32.dll_FindWindowA ; "be"
|           0x00401561      ffd0           call eax
|           0x00401563      83ec08         sub esp, 8
|           0x00401566      8945f4         mov dword [local_ch], eax
|           0x00401569      c74424040000.  mov dword [local_4h], 0
|           0x00401571      8b45f4         mov eax, dword [local_ch]
|           0x00401574      890424         mov dword [esp], eax
|           0x00401577      a134624000     mov eax, dword sym.imp.USER32.dll_ShowWindow ; [0x406234:4]=0x6584 reloc.USER32.dll_ShowWindow
|           0x0040157c      ffd0           call eax
|           0x0040157e      83ec08         sub esp, 8
|           0x00401581      e8c9050000     call sub.SOFTWARE__Microsoft__Windows__CurrentVersion__Run_401b4f
|           0x00401586      8945f0         mov dword [local_10h], eax
|           0x00401589      837df002       cmp dword [local_10h], 2
|       ,=< 0x0040158d      7515           jne 0x4015a4
|       |   0x0040158f      c745ec134040.  mov dword [local_14h], str.c:___windir___svchost.exe ; 0x404013 ; "c:\%windir%\svchost.exe"
|       |   0x00401596      8b45ec         mov eax, dword [local_14h]
|       |   0x00401599      890424         mov dword [esp], eax
|       |   0x0040159c      e873060000     call sub.SOFTWARE__Microsoft__Windows__CurrentVersion__Run_401c14
|       |   0x004015a1      8945e8         mov dword [local_18h], eax
|       |   ; CODE XREF from main (0x40158d)
|       `-> 0x004015a4      e80e000000     call sub.KERNEL32.dll_Sleep_4015b7
|           0x004015a9      8945e4         mov dword [local_1ch], eax
|           0x004015ac      8b45e4         mov eax, dword [local_1ch]
|           0x004015af      8b4dfc         mov ecx, dword [local_4h_2]
|           0x004015b2      c9             leave
|           0x004015b3      8d61fc         lea esp, dword [ecx - 4]
\           0x004015b6      c3             ret
[0x00401530]> 
{% endhighlight %}
Visual mode might be helpfull here:
![](/images/radare2/visual.PNG){: width="50%"}
[link1]:https://www.youtube.com/watch?v=DnZLy_sq-nY&feature=emb_logo
[link2]:https://attack.mitre.org/techniques/T1060/
[link3]:https://attack.mitre.org/techniques/T1497/
[link4]:https://attack.mitre.org/techniques/T1056/
