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
	root.mainloop()


def principi():
	
	global i
	i = Tk()
	i.title("Servidor remot")
	i.geometry("400x350")
	global txip
	global txc
	global tusr
	global txp

	ip = Label(i, text="IP: ")
	ip.pack() 
	txip = Entry(i)
	usr = Label(i, text="Usuari: ")
	tusr = Entry(i)
	c = Label(i, text="Contrasenya: ")
	txc = Entry(i,show="*")
	iport = Label(i, text="Port: ")
	txp = Entry(i)
	
	u = txip.get()
	ports = Button(i, text='Ports oberts', command=llistaports) 
	oports = Button(i, text='Obir port', command=lambda: conecta('obrir')) 
	tports = Button(i, text='Tanca port', command=lambda: conecta('tancar')) 
		
	
	ip.grid(column=0, row=0, sticky="nsew")
	txip.grid(column=1, row=0, sticky="nsew")
	usr.grid(column=0, row=1, sticky="nsew")
	tusr.grid(column=1, row=1, sticky="nsew")
	c.grid(column=0, row=2, sticky="nsew")
	txc.grid(column=1, row=2, sticky="nsew")
	ports.grid(column=0, row=3, sticky="nsew", columnspan=2)
	
	iport.grid(column=0, row=4, sticky="nsew")
	txp.grid(column=1, row=4, sticky="nsew")
	
	oports.grid(column=0, row=5, sticky="nsew")
	tports.grid(column=1, row=5, sticky="nsew")

	Grid.rowconfigure(i, 0, weight=1)
	Grid.rowconfigure(i, 1, weight=1)
	Grid.rowconfigure(i, 2, weight=1)
	Grid.rowconfigure(i, 3, weight=1)
	Grid.rowconfigure(i, 4, weight=1)
	Grid.rowconfigure(i, 5, weight=1)
	Grid.columnconfigure(i, 0, weight=1)
	Grid.columnconfigure(i, 1, weight=1)

	crearFicher()
	i.mainloop()
	
def conecta(eleccio):
	
	try:
 
            # Conectamos por ssh

            ssh = paramiko.SSHClient()

            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.load_system_host_keys()

#           ssh.connect( hostname = txip.get() , username = tusr.get() , password = txc.get())
            ssh.connect( '10.33.140.149',22, 'paco', password = txc.get())
            sftp = ssh.open_sftp()
            if eleccio == 'obrir':
                obrirPort(txp.get())
            if eleccio == 'tancar':
                tancarPort(txp.get())
            sftp.put('firewall.sh', '/tmp/firewall.sh')
            sftp.close()	    
	    # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
            entrada, salida, error = ssh.exec_command('sudo -S /bin/sh /tmp/firewall.sh')
            entrada.write(txc.get() + '\n')
            return ssh
	      		
	except:

            sys.exit(1)
	

# Funcio llista els ports de la maquina 
def llistaports():
	
	portsOberts = subprocess.Popen("nmap -Pn " + txip.get(), stdout=subprocess.PIPE, shell=True) 
	(salida, err) = portsOberts.communicate()
	# Mostrar la salida estándar en pantalla
	menu(salida)		


def obrirPort(port):
	if comprovarPort(port) == False:
		# Obrim el fitxer amb mode lectura (read)	
		with open("firewall.sh", "r") as file:
			lines = file.readlines()	
	
		# Obrim el fitxer amb mode  escritura (write)	
		with open("firewall.sh", "w") as file:
			for l in range(len(lines),1,-1):
				if l == len(lines):
					lines.append(lines[l-1]) 
				else:
					lines[l] = lines[l-1]	
			lines[1] = "iptables -A INPUT -p tcp -m tcp --dport " + port  +  " -j ACCEPT" + os.linesep
			for line in lines:
				file.write(line)
def tancarPort(port):
	
	if comprovarPort(port) == True:
		# Obrim el fitxer amb mode lectura (read)	
		with open("firewall.sh", "r") as file:
			lines = file.readlines()	
	
			for idline, line in enumerate(lines):
				if port in line:
					print(idline)
					lines.pop(idline)

		# Obrim el fitxer amb mode  escritura (write)	
		with open("firewall.sh", "w") as file:

			for line in lines:
				file.write(line)

def crearFicher():
	
	if not os.path.isfile('firewall.sh'):
		
		N="iptables -F"
		H= "iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT" 
		B="iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT"
		C="iptables -A INPUT -j DROP"
				
		# Escritura
		file = open("firewall.sh","w")
		file.write(N + os.linesep)
		file.write(H + os.linesep)
		file.write(B + os.linesep)
		file.write(C + os.linesep)
		file.close()

def comprovarPort(port):	
	
	# Obrim el fitxer amb mode lectura (read)	
	with open("firewall.sh", "r") as file:
		lines = file.readlines()	

		for line in lines:
			if port in line:
				return True
	return False		

principi()
