from tkinter import *
from tkinter import ttk
from subprocess import PIPE, Popen 
import os

#	proces=Popen(['sshpass','-p', contra,'scp',usuari+'@'+IP+':/etc/network/interfaces','.'],
#		stdout=PIPE,stderr=PIPE, stdin=PIPE)

def menu():
	root = Tk()

	mb = Menu(root)
	root.config(menu=mb)

	S = Menu(mb)
	Pmenu = Menu(mb)
	Bmenu = Menu(mb)
	Hmenu = Menu(mb)

	S = Menu(mb, tearoff=0)
	S.add_command(label="Intern")
	S.add_command(label="Extern")

	Pmenu = Menu(mb, tearoff=0)
	Pmenu.add_command(label="Direccions ip")
	Pmenu.add_command(label="Ports")
	Pmenu.add_command(label="Domini", command=creacio) #Entendre perque falla

	Bmenu = Menu(mb, tearoff=0)
	Bmenu.add_command(label="Direccions ip")
	Bmenu.add_command(label="Ports")
	Bmenu.add_command(label="Domini")


	Hmenu = Menu(mb, tearoff=0)
	Hmenu.add_command(label="Ajuda")
	Hmenu.add_command(label="Donar")
	Hmenu.add_command(label="Sorti", command=root.quit)

	mb.add_cascade(label="Permetre",menu=Pmenu)
	mb.add_cascade(label="Blocar",menu=Bmenu)
	mb.add_cascade(label="Ajuda",menu=Hmenu)

	root.mainloop()


def principi(n):
	
	global i
	i = Tk()
	i.title("Servidor remot")
	global txip
	global txc
	global tusr

#	if n == 1:
#		finestra.destroy()
	ip = Label(i, text="IP: ")
	txip = Entry(i,)
	usr = Label(i, text="Usuari: ")
	tusr = Entry(i)
	c = Label(i, text="Contrasenya: ")
	txc = Entry(i,show="*")
	ok = Button(i, text="Fet", command=menu)


	ip.grid(column=0, row=0, sticky="nsew")
	txip.grid(column=1, row=0, sticky="nsew")
	usr.grid(column=0, row=1, sticky="nsew")
	tusr.grid(column=1, row=1, sticky="nsew")
	c.grid(column=0, row=2, sticky="nsew")
	txc.grid(column=1, row=2, sticky="nsew")
	ok.grid(column=0, row=3, sticky="nsew", columnspan=2)

	Grid.rowconfigure(i, 0, weight=1)
	Grid.rowconfigure(i, 1, weight=1)
	Grid.rowconfigure(i, 2, weight=1)
	Grid.rowconfigure(i, 3, weight=1)
	Grid.columnconfigure(i, 0, weight=1)
	Grid.columnconfigure(i, 1, weight=1)


	i.mainloop()

##DNS
#N="iptables -F"
#A="iptables -A FORWARD -p tcp -m multiport --dport 80,443,53 -j ACCEPT"
#B="iptables -A FORWARD -p udp --dport 53 -j ACCEPT"



#Escritura
#file = open("/home/paco/firewall.sh","w")
#file.write(A + os.linesep)
#file.write(B)
#file.close()

principi(1)









