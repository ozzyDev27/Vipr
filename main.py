import time
from termcolor import cprint
from random import randint
import re
import math
import os
import tkinter
import customtkinter
#import PyYaml
#^^^ MAKE WORK!!! (please)
#ORR make a "settings tab" on the tkinter window
run = open("program.vpr", "r")
app=customtkinter.CTk()
app.geometry("750x450")
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
loop = 0
var = {"-": "-"}	
labels = {"-": "-"}


inputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
inputTextField.pack(side=tkinter.LEFT,expand=True,fill=tkinter.BOTH)
inputTextField.place(width=round((app.winfo_width()-50)/2),height=app.winfo_height(),anchor=tkinter.W,relx=0,rely=0.5)
getProgram=open("program.vpr", "r")
inputTextField.insert("end-1c", ''.join(getProgram.readlines()))

outputTextField=tkinter.Text(app,bg="#242424",fg="#ffffff",wrap=tkinter.NONE)
outputTextField.pack(side=tkinter.RIGHT,expand=True,fill=tkinter.BOTH)
outputTextField.place(width=round((app.winfo_width()-50)/2),height=app.winfo_height(),anchor=tkinter.E,relx=1,rely=0.5)
def runButtonFunction():
	global running,nextRun,setTime
	running=not running
	if running: 
		out=''
		outputTextField.delete(1.0, "end-1c")
	nextRun=0
	setTime=0
runButton=customtkinter.CTkButton(master=app,command=runButtonFunction)
runButton.place(anchor=tkinter.N,relx=0.5,rely=0)
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
	global loop
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
		#print(nextRun)
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
		#playsound('static\Among Us Drip Theme Song Original (Among Us Trap Remix _ Amogus Meme Music).mp3')
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
	inputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height(),anchor=tkinter.W,relx=0,rely=0.5)
	outputTextField.place(width=round((app.winfo_width()-padding)/2),height=app.winfo_height(),anchor=tkinter.E,relx=1,rely=0.5)
	addToProgram=open("program.vpr","w")
	addToProgram.write(inputTextField.get(1.0,"end-1c"))
	runButton.configure(text=str(running))
	#print(inputTextField.get(1.0,"end-1c"))
	addToProgram.close()
	writeOut=open("output.txt", "w")
	writeOut.write(out)
	writeOut.close()
	if outputTextField.get(1.0,"end-1c")!=out:
		outputTextField.delete(1.0, "end-1c")
		outputTextField.insert("end-1c", out)
	#print(f"{nextRun}!{setTime}")
	if running:
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
	#time.sleep(.01)
running=False
nextRun=0
setTime=0
app.after(1,Loop)
app.mainloop()
if devkey: cprint(f"Dev > Run Lines: {complete}", "magenta")
run.close()
print("")
out+="\n"
