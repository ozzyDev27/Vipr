import time
from termcolor import cprint
from random import randint
import re
import math
import os
import tkinter
import customtkinter
import datetime
#!import yaml

run = open("program.vpr", "r")
app=customtkinter.CTk()
app.geometry("750x450")
app.minsize(375,225)
app.title("Vipr")
line = 0
toolbarsize=0
# ----------------------- Tkinter Widget Initialization ---------------------- #
inputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
inputTextField.pack(side=tkinter.LEFT)
inputTextField.place(width=round((app.winfo_width()-50)/2),height=app.winfo_height()-toolbarsize,anchor=tkinter.W,relx=0,rely=0.5)
inputTextField.insert("end-1c", ''.join(run.readlines()))

#outputScrollbar=tkinter.Scrollbar(app,orient="vertical")
#outputScrollbar.pack(side=tkinter.RIGHT,fill='y')
outputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
outputTextField.pack(side=tkinter.RIGHT)

timer=tkinter.Label(text="0:00:00.00",fg="#ffffff",bg="#242424",font=("",16))
timer.place(anchor=tkinter.N,relx=.5,rely=.1+(toolbarsize/app.winfo_height()))

def importButtonFunction():
	global openFile,openAFile
	openFile=tkinter.filedialog.askopenfilename()
	if openFile in [None,""]:return
	openAFile=True
importButton=customtkinter.CTkButton(master=app,text="Import",command=importButtonFunction)
importButton.pack(side=tkinter.LEFT)
importButton.place(anchor=tkinter.N,relx=.5,rely=.3)


def exportButtonFunction():
	f = tkinter.filedialog.asksaveasfile(mode='w', initialfile = 'program.vpr',defaultextension=".vpr",filetypes=[("All Files","*.*"),("Vipr Files","*.vpr")])
	if f in [None,'']:return
	f.write(inputTextField.get(1.0,"end-1c"))
	f.close()
	
exportButton=customtkinter.CTkButton(master=app,text="Export",command=exportButtonFunction)
exportButton.pack(side=tkinter.LEFT)
exportButton.place(anchor=tkinter.N,relx=.5,rely=.4)

def runButtonFunction():
	global running,nextRun,setTime,reset
	running=not running
	if running:reset=True
	nextRun=0
	setTime=0
runButton=customtkinter.CTkButton(master=app,command=runButtonFunction,fg_color=("#1a9132","#1a9132"),hover_color=("#126b24","#126b24"))
runButton.place(anchor=tkinter.N,relx=0.5,rely=(toolbarsize/app.winfo_height()))


# --------------------------------- Functions -------------------------------- #
#? Replaces all variables with their value
def repVar(check):
	check = re.sub(r'(?<=~)\w+(?=~)', lambda x: var[x.group(0)], check).replace("~", "")
	return check
		
#? remove suffix fix
def removeEnd(toRemove, stringGet):
	if str(stringGet).endswith(str(toRemove)):
		lengthRemove = int(len(toRemove))*-1
		return stringGet[:lengthRemove]
	else:
		return stringGet

#? Error message
def error(errormsg):
	try:
		print(f"\nERROR: {errormsg} on line {userline}")
	except:print(f"\nERROR: {errormsg} on line {userline}")

# ------------------------------- All commands ------------------------------- #
def exec_next(lines):
	global line,code,userline,activeloop,comment,remember,out,nextRun
	activeloop = 0
	comment = 0
	userline = line + 1
	lines[line]=lines[line].replace("\n","")
	try:code = lines[line].split(" ")
	except IndexError:pass
	rand = 0
	cmd = code[0]
	args= code[1:]
	othr = args[2:]
	lengt = 0
	if cmd == "txt":
		toText=""
		for word in args:
			toText+=repVar(str(word))
			toText+=" "
		toText = removeEnd("\n ",toText)
		print(toText)
		out+=toText
		out+="\n"
	elif cmd == "slp":
		timeToSleep=repVar(args[0])
		nextRun=nextFrame(timeToSleep)
	elif cmd == "jmp":
		remember = line
		line = int(repVar(args[0])) - 2
	elif cmd == "rtn":line = remember
	elif cmd == "lbl":
		if args[0] == "set":labels[str(args[1]).replace("\n", "")] = line
		elif args[0] == "jmp":
			remember = line
			line = labels[str(args[1]).replace("\n", "")]
	elif cmd == "end":
		raise IndexError #?pretends to be the end of the program
	elif cmd == "var":
		kwargs=str(args[1]).replace("\n","")
		vartochange = args[0].replace("\n", "")
		if kwargs == "num":
			if   args[2] == "set":var[vartochange] = float(repVar(args[3]))
			elif args[2] == "add":var[vartochange] = float(repVar(args[3]))+float(repVar(args[4]))
			elif args[2] == "sub":var[vartochange] = float(repVar(args[3]))-float(repVar(args[4]))
			elif args[2] == "mlt":var[vartochange] = float(repVar(args[3]))*float(repVar(args[4]))
			elif args[2] == "div":var[vartochange] = float(repVar(args[3]))/float(repVar(args[4]))
			elif args[2] == "rng":var[vartochange] = randint(int(round(repVar(args[3]))),int(round(repVar(args[4]))))
			elif args[2] == "rnd":var[vartochange] = round(float(repVar(args[3])))
			elif args[2] == "sin":var[vartochange] = math.sin(float(repVar(args[3])))
			elif args[2] == "cos":var[vartochange] = math.cos(float(repVar(args[3])))
			elif args[2] == "tan":var[vartochange] = math.tan(float(repVar(args[3])))
			elif args[2] == "flr":var[vartochange] = math.floor(float(repVar(args[3])))
			elif args[2] == "cil":var[vartochange] = math.ceil(float(repVar(args[3])))
			elif args[2] == "mod":var[vartochange] = float(repVar(args[3]))%float(repVar(args[4]))
			elif args[2] == "pwr":var[vartochange] = float(repVar(args[3]))**float(repVar(args[4]))
			elif args[2] == "abs":var[vartochange] = abs(float(repVar(args[3])))
			if str(var[vartochange]).endswith(".0"):var[vartochange] = str(var[vartochange]).replace(".0", "")
		elif kwargs == "str":
			if args[2] == "set":
				toSet = ""
				for word in args[3:]:toSet += repVar(word).replace("\n","")+" "
				toSet = removeEnd(" ", toSet)
				var[vartochange] = toSet
			elif args[2] == "len":var[vartochange]=len(str(repVar(args[3])))
		elif kwargs == "inp":
			for word in othr:
				lengt += 1
				if lengt == len(othr):
					print(word.replace("\n", ""))
					out+=word.replace("\n", "")
					out+="\n"
				else:
					print(word, end=" ")
					out+=word
					out+="\n"
			print(">", end="")
			out+="> "
			notyet=input(" ")
			var[vartochange]=notyet
		elif kwargs == "cpy":var[vartochange]=var[str(args[2]).replace("\n","")]
		elif kwargs == "bnk":var[vartochange]=None
	elif cmd == "try":
		if args[1] == "eql":
			if repVar(str(args[2])) == repVar(str(args[3])):
				remember=line
				line=int(args[0]) - 2
		elif args[1] == "lss":
			if repVar(str(args[2])) < repVar(str(args[3])):
				remember=line
				line=int(args[0]) - 2
		elif args[1] == "grt":
			if repVar(str(args[2])) > repVar(str(args[3])):
				remember=line
				line=int(args[0]) - 2
	elif cmd == "snd (WIP)":
		#snd 4 100
		#plays note 4 for 1 second
		pass
	elif cmd == "new":
		for i in range(0, int(args[0])):
			print("")
			out+="\n"
	#!elif cmd == "lst":
	#!	# remove stuff
	#!	# get length
	#!	# check if inside
	#!	# replace stuff
	#!	lsttochange=str(args[0].replace("\n",""))
	#!	keyword=args[1].replace("\n","")
	#!	if keyword == "new":
	#!		var[lsttochange]=[]
	#!	elif keyword == "app":
	#!		append=''
	#!		for i in args[2:]:
	#!			append+=i
	#!			append+=' '
	#!		append=append=removeEnd("\n ", append)
	#!		var[lsttochange].append(repVar(append))
	#!	elif keyword == "ins":
	#!		#lst name ins 1 muahahahhah
	#!		append=''
	#!		for i in args[3:]:
	#!			append+=i
	#!			append+=' '
	#!		append=removeEnd("\n ", append)
	#!		var[lsttochange].insert(int(args[2])-1,repVar(append))
	#!	elif keyword == "get":
	#!		var[args[2]]=var[args[3]][int(args[4].replace("\n",""))]
	line += 1
padding=150
def nextFrame(next:int):
	return (int(round(time.time()*100))+int(next))/100
def Loop():
	global nextRun,setTime,running,reset,line,out,startTime,openFile,openAFile,var,labels,inputMode
	inputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height(),anchor=tkinter.SW,relx=0,rely=1)
	outputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height()-50,anchor=tkinter.NE,relx=1,rely=0)
	addToProgram=open("program.vpr","w")
	addToProgram.write(inputTextField.get(1.0,"end-1c"))
	runButton.configure(text=str("Pause" if running else "Run"))
	if outputTextField.get(1.0,"end-1c")!=out:
		outputTextField.delete(1.0, "end-1c")
		outputTextField.insert("end-1c", out)
	if reset:
		out=''
		outputTextField.delete(1.0, "end-1c")
		line = 0
		nextRun=0
		setTime=0
		startTime=time.time()
		reset=False
		var = {"-": "-"}	
		labels = {"-": "-"}
	if openAFile:
		inputTextField.delete(1.0, "end-1c")
		with open(openFile,"r") as f:
			fileText=f.read()
		inputTextField.insert("end-1c", fileText)
		openAFile=False
	if running:	
		timer.configure(text=f"{datetime.timedelta(seconds=math.floor(time.time()-startTime))}.{round(((time.time()-startTime)%1)*100)}")
		try:
			if time.time()>=nextRun:
				nextRun=nextFrame(1)
				exec_next(inputTextField.get(1.0,"end-1c").split("\n"))
			else:
				setTime+=1
		except IndexError:
			setTime=0
			nextRun=0	
		outputTextField.yview_moveto(1.0)
	app.after(10,Loop)

# -------------------------- Variable Initialization ------------------------- #
running=False
nextRun=0
openFile=""
openAFile=False
startTime=time.time()
setTime=0
inputMode=False
reset=True
out=""

# --------------------------------- Run Vipr --------------------------------- #
app.after(1,Loop)
app.mainloop()
run.close()
print("")
out+="\n"
