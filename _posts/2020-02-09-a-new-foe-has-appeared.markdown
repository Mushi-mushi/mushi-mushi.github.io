---
layout: post
title:  "A new foe has appeared !"
date:   09-02-2020 13:34:34
categories: malware
---
![](/images/new-foe/new-foe.jpg){: width="600" height="600")}

Introduction
============
The idea to finally set up my own blog stems from my first malware analysis where a word document was spotted on Twitter by one of my colleague. Following the Twitter thread shows that some researchers had already did some preliminary analysis but the main payload still needed to be unpacked and analized. After reaching out to one of the researcher (@Arkbird_SOLG) I was directed to a great tutorial about how to unpack python executable ([Tutorial][link1])

Sample
=======
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">interesting sample<br>maybe <a href="https://twitter.com/hashtag/APT?src=hash&amp;ref_src=twsrc%5Etfw">#APT</a><br>Hash:7c487d8462567a826da95c799591f5fb<br><br>Cc <a href="https://twitter.com/Arkbird_SOLG?ref_src=twsrc%5Etfw">@Arkbird_SOLG</a> <a href="https://twitter.com/ItsReallyNick?ref_src=twsrc%5Etfw">@ItsReallyNick</a> <a href="https://twitter.com/spider_girl22?ref_src=twsrc%5Etfw">@spider_girl22</a> <a href="https://twitter.com/DeadlyLynn?ref_src=twsrc%5Etfw">@DeadlyLynn</a> <a href="https://twitter.com/cyb3rops?ref_src=twsrc%5Etfw">@cyb3rops</a> <a href="https://t.co/migPtNcAJI">pic.twitter.com/migPtNcAJI</a></p>&mdash; @Rmy (@Rmy_Reserve) <a href="https://twitter.com/Rmy_Reserve/status/1217066627440635905?ref_src=twsrc%5Etfw">January 14, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

As mentionned before, researchers had already figure out that the document was first downloading a dropper by reaching out to an googledrive link, downloading a picture from which the python RAT was extracted. 

![](/images/new-foe/new-foe/Mickey.jpg){: width="600" height="600")}

As a result, I headed to [AnyRun][link2] in order to fetch the RAT that I now needed to unpack.





[link1]:https://infosecuritygeek.com/reversing-a-simple-python-ransomware/  
[link2]:https://app.any.run/tasks/1d7567d9-0eac-4944-ba38-4894fdfe1c2f/
