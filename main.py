import time
from termcolor import cprint
from random import randint
import re
import math
import os
import tkinter
import customtkinter
import datetime
#import PyYaml
#^^^ MAKE WORK!!! (please)
#ORR make a "settings tab" on the tkinter window
run = open("program.vpr", "r")
app=customtkinter.CTk()
app.geometry("750x450")
app.minsize(375,225)
app.title("Vipr")
options = {
	"devkey":False,
	"color": True,
	"insult":"❤️"
}
devkey = options["devkey"]
color = options["color"]
whotoinsult = options["insult"]
line = 0
rid = float(0)
settline = 0
complete = 0
var = {"-": "-"}	
labels = {"-": "-"}
toolbarsize=40
# ----------------------- Tkinter Widget Initialization ---------------------- #
inputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
inputTextField.pack(side=tkinter.LEFT)
inputTextField.place(width=round((app.winfo_width()-50)/2),height=app.winfo_height()-toolbarsize,anchor=tkinter.W,relx=0,rely=0.5)
getProgram=open("program.vpr", "r")
inputTextField.insert("end-1c", ''.join(getProgram.readlines()))

outputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
outputTextField.pack(side=tkinter.RIGHT)
outputTextField.place(width=round((app.winfo_width()-50)/2),height=app.winfo_height()-toolbarsize,anchor=tkinter.E,relx=1,rely=0.5)

timer=tkinter.Label(text="0:00:00+00",fg="#ffffff",bg="#242424")
timer.place(anchor=tkinter.N,relx=.5,rely=.1+(toolbarsize/app.winfo_height()))

#toolbar=tkinter.Frame(app,bg="#242424",height=toolbarsize)
#toolbar.pack(side=tkinter.TOP,fill=tkinter.X)
def runButtonFunction():
	global running,nextRun,setTime,reset
	running=not running
	if running:reset=True
	nextRun=0
	setTime=0
runButton=customtkinter.CTkButton(master=app,command=runButtonFunction)
runButton.place(anchor=tkinter.N,relx=0.5,rely=(toolbarsize/app.winfo_height()))
# Replaces all variables with their value
def repVar(check):
	check = re.sub(r'(?<=~)\w+(?=~)', lambda x: var[x.group(0)], check).replace("~", "")
	return check
		
#remove suffix fix
def removeEnd(toRemove, stringGet):
	if str(stringGet).endswith(str(toRemove)):
		lengthRemove = int(len(toRemove))*-1
		return stringGet[:lengthRemove]
	else:
		return stringGet
color = False

out=""
def error(errormsg):
	try:
		if color:
			cprint(f"\nERROR: {errormsg} on line {userline}", "yellow")
		else:
			print(f"\nERROR: {errormsg} on line {userline}")
	except:print(f"\nERROR: {errormsg} on line {userline}")
def exec_next(lines):
	global line
	global code
	global complete
	global userline
	global activeloop
	global comment
	global rid
	global remember
	global whotoinsult
	global out
	global nextRun
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
		nextRun=int(timeToSleep)
		rid += int(timeToSleep)
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
		raise IndexError
	elif cmd == "dbg (NO)":
		if args[0] == "1":print(var)
	elif cmd == "var":
		kwargs=str(args[1]).replace("\n","")
		vartochange = args[0].replace("\n", "")
		if kwargs == "num":
			if args[2] == "set":var[vartochange] = float(repVar(args[3]))
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
			cprint(">", "blue" if color else "white", end="")
			out+="> "
			notyet=input(" ")
			if notyet == whotoinsult:var[vartochange]="dumb"
			else:var[vartochange]=notyet
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
	elif cmd == "lst":
		# remove stuff
		# get length
		# check if inside
		# replace stuff
		lsttochange=str(args[0].replace("\n",""))
		keyword=args[1].replace("\n","")
		if keyword == "add":
			var[lsttochange]=[]
		elif keyword == "app":
			append=''
			for i in args[2:]:
				append+=i
				append+=' '
			append=append=removeEnd("\n ", append)
			var[lsttochange].append(repVar(append))
		elif keyword == "ins":
			#lst name ins 1 muahahahhah
			append=''
			for i in args[3:]:
				append+=i
				append+=' '
			append=removeEnd("\n ", append)
			var[lsttochange].insert(int(args[2])-1,repVar(append))
	
	line += 1
totallines = run.readlines()
complete = 0
padding=150

def Loop():
	global complete
	global nextRun
	global setTime
	global running
	global reset
	global line
	global out
	global startTime
	global toolbarsize
	inputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height()-toolbarsize,anchor=tkinter.SW,relx=0,rely=1)
	outputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height()-toolbarsize,anchor=tkinter.SE,relx=1,rely=1)
	addToProgram=open("program.vpr","w")
	addToProgram.write(inputTextField.get(1.0,"end-1c"))
	runButton.configure(text=str(running))
	if outputTextField.get(1.0,"end-1c")!=out:
		outputTextField.delete(1.0, "end-1c")
		outputTextField.insert("end-1c", out)
	if reset:
		out=''
		outputTextField.delete(1.0, "end-1c")
		line = 0
		nextRun=0
		setTime=0
		complete=0		
		startTime=time.time()
		reset=False
	if running:	
		timer.configure(text=f"{datetime.timedelta(seconds=math.floor(time.time()-startTime))}.{round(((time.time()-startTime)%1)*100)}")
		try:
			if setTime>=nextRun:
				nextRun=0
				setTime=0
				exec_next(totallines)
				complete += 1
			else:
				setTime+=1
		except IndexError:
			setTime=0
			nextRun=0
	else:
		complete=0
	app.after(10,Loop)
running=False
nextRun=0
startTime=time.time()
setTime=0
reset=True
app.after(1,Loop)
app.mainloop()
if devkey: cprint(f"Dev > Run Lines: {complete}", "magenta")
run.close()
print("")
out+="\n"