---
layout: cheat
title: Cheatsheet
---


<kbd>Ctrl</kbd>+<kbd>b</kbd> <kbd>c</kbd> : create window




Tmux shortcut
=============
{% highlight%}
<kbd>Ctrl</kbd>+ b c :Create window
Ctrl + b , :Rename current window
Ctrl + b % :Split pane vertically
Ctrl + b " :Split pane horizontally
Ctrl + b z :Toggle pane zoom
Ctrl + b ! :Convert pane into a window
Ctrl + b x :Close current pane
Ctrl + b [ :Enter copy mode
q : Quit mode
/ :Search forward
? :Search backward
n :Next keyword occurance
N :Previous keyword occurance
Spacebar   :Start selection
Esc        :Clear selection
Enter      :Copy selection
Ctrl + b ] : Paste contents of buffer_0
{% endhighlight %}

---
<kbd>Ctrl</kbd>+ b c :Create window
---

[Back to the top](#tmux-shortcut)

Upgrading Simple Shells to Fully Interactive TTYs
=================================================
{% highlight python%}
python -c 'import pty; pty.spawn("/bin/bash")'
or
python3 -c 'import pty; pty.spawn("/bin/bash")'
{% endhighlight %}

Then press CTRL+Z to return to your local shell

{% highlight bash%}
stty raw -echo
stty -a
{% endhighlight %}

Note the number of rows and columns before pressing fg to return to the box

{% highlight bash%}
export SHELL=bash
export TERM=xterm256-color
stty rows number_of_row columns number_of_columns
{% endhighlight %}

Enjoy!

[Back to the top](#tmux-shortcut)

Finding binaries that the systems package manager does not recognize
====================================================================
{% highlight bash%}
for i in $(ls /sbin/*); do echo $i; done
for i in $(ls /sbin/*); do dpkg --search $i; done
for i in $(ls /sbin/*); do dpkg --search $i 1>/dev/null; done
{% endhighlight %}

To investigate on different location in the $PATH

[Back to the top](#tmux-shortcut)

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

[Back to the top](#tmux-shortcut)

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

