from tkinter import *
from tkinter import ttk
import subprocess  
import os
import paramiko

def menu(salida):
	root = Tk()
	txtPorts = Text(root)
	txtPorts.insert(END, salida)
	txtPorts.config(state=DISABLED)
	txtPorts.pack() 
#	mb = Menu(root)
#	root.config(menu=mb)
#
#	S = Menu(mb)
#	Pmenu = Menu(mb)
#	Bmenu = Menu(mb)
#	Hmenu = Menu(mb)
#
#	S = Menu(mb, tearoff=0)
#	S.add_command(label="Intern")
#	S.add_command(label="Extern")
#
#	Pmenu = Menu(mb, tearoff=0)
#	Pmenu.add_command(label="Direccions ip")
#	Pmenu.add_command(label="Ports")
#	Pmenu.add_command(label="Domini") 
#
#	Bmenu = Menu(mb, tearoff=0)
#	Bmenu.add_command(label="Direccions ip")
#	Bmenu.add_command(label="Ports")
#	Bmenu.add_command(label="Domini")
#
#
#	Hmenu = Menu(mb, tearoff=0)
#	Hmenu.add_command(label="Ajuda")
#	Hmenu.add_command(label="Donar")
#	Hmenu.add_command(label="Sorti", command=root.quit)
#
#	mb.add_cascade(label="Permetre",menu=Pmenu)
#	mb.add_cascade(label="Blocar",menu=Bmenu)
#	mb.add_cascade(label="Ajuda",menu=Hmenu)
#
	root.mainloop()


def principi(n):
	
	global i
	i = Tk()
	i.title("Servidor remot")
	i.geometry("400x350")
	global txip
	global txc
	global tusr

#	if n == 1:
#		finestra.destroy()
	ip = Label(i, text="IP: ")
	ip.pack() 
	txip = Entry(i,)
	usr = Label(i, text="Usuari: ")
	tusr = Entry(i)
	c = Label(i, text="Contrasenya: ")
	txc = Entry(i,show="*")
	
	u = txip.get()
	ok = Button(i, text="Fet", command=conecta)
	ports = Button(i, text='Ports oberts', command=llistaports) 
		
	
	ip.grid(column=0, row=0, sticky="nsew")
	txip.grid(column=1, row=0, sticky="nsew")
	usr.grid(column=0, row=1, sticky="nsew")
	tusr.grid(column=1, row=1, sticky="nsew")
	c.grid(column=0, row=2, sticky="nsew")
	txc.grid(column=1, row=2, sticky="nsew")
	ok.grid(column=0, row=3, sticky="nsew")
	ports.grid(column=1, row=3, sticky="nsew")

	Grid.rowconfigure(i, 0, weight=1)
	Grid.rowconfigure(i, 1, weight=1)
	Grid.rowconfigure(i, 2, weight=1)
	Grid.rowconfigure(i, 3, weight=1)
	Grid.columnconfigure(i, 0, weight=1)
	Grid.columnconfigure(i, 1, weight=1)

	crearFicher()
	i.mainloop()
	
def conecta():
	
	try:
 
            # Conectamos por ssh

            ssh = paramiko.SSHClient()

            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.load_system_host_keys()

#            ssh.connect( hostname = txip.get() , username = tusr.get() , password = txc.get())
            ssh.connect( '10.33.140.149',22, 'paco', password = txc.get())
            sftp = ssh.open_sftp()
            obrirPort('22')
            sftp.put('firewall.sh', '/tmp/firewall.sh')
            sftp.close()	    
	    # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
            entrada, salida, error = ssh.exec_command('sudo -S /bin/sh /tmp/firewall.sh')
            entrada.write(txc.get() + '\n')
	    # Mostrar la salida estándar en pantalla
            #print(salida.read())
            #print(error.read())
            # Cerrar la conexión
            # ssh.close()
            return ssh
	     		
	except:

            #print('Error en la conexión')

            sys.exit(1)
	

# Funcio llista els ports de la maquina 
def llistaports():
	
	portsOberts = subprocess.Popen("nmap -Pn " + txip.get(), stdout=subprocess.PIPE, shell=True) 
	(salida, err) = portsOberts.communicate()
	print ("Today is", salida)
	# Mostrar la salida estándar en pantalla
	#print(error.read())
	menu(salida)		


def obrirPort(port):
	
	with open("firewall.sh", "r") as file:
		lines = file.readlines()	
	lines[1] = "iptables -A INPUT -p tcp -m tcp --dport " + port  +  " -j ACCEPT" + os.linesep

	with open("firewall.sh", "w") as file:
		for line in lines:
			file.write(line)
def crearFicher():
	
	if os.path.isfile('firewall.sh'):
		print('Existeix firewall.sh')	
	else:
		N="iptables -F"
		B="iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT"
		C="iptables -A INPUT -j DROP"
		
		#Escritura
		file = open("firewall.sh","w")
		file.write(N + os.linesep)
		file.write(B + os.linesep)
		file.write(C + os.linesep)
		file.close()

principi(0)
