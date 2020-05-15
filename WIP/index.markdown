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





[link1]:https://www.youtube.com/watch?v=DnZLy_sq-nY&feature=emb_logo
