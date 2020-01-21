---
layout: default
title: Cheatsheet
---

Upgrading Simple Shells to Fully Interactive TTYs
--------------
{% highlight bash%}
python -c 'import pty; pty.spawn("/bin/bash")'
{% endhighlight %}

Then press CTRL+Z to background

{% highlight bash%}
stty raw -echo
{% endhighlight %}

Press Enter, fg, then Enter twice to return to your original shell

{% highlight bash%}
stty -a
{% endhighlight %}

This will give you the number of columns and rows of the terminal

{% highlight bash%}
stty rows number_of_row columns number_of_columns
{% endhighlight %}

Interesting Links:
--------------
- [jwt.io][link1]: Decode and edit jwt token
- [cyberchef][link3]: Decode and encode in multiple format
- [stackedit.io][link4]: Markdown editor
- [devhints.io][link5]: Jekyll dev ops tricks
- [jekyllrb.com][link6]: Jekyll tuto
- [PayloadsAllTheThings][link7]: Payload for everything

[link1]:https://jwt.io/  
[link2]:http://jekyllrb.com
[link3]:https://gchq.github.io/CyberChef/
[link4]:https://stackedit.io/app#
[link5]:https://devhints.io/jekyll 
[link6]:https://jekyllrb.com/
[link7]:https://github.com/swisskyrepo/PayloadsAllTheThings
