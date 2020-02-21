Requirement 
===========
First we download the zip file for the challenges:
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
