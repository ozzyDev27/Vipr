import time
from termcolor import cprint
from random import randint
import re
import math
import os
#import PyYaml
#^^^ MAKE WORK!!! (please)
run = open("program.vpr", "r")
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

# Replaces all variables with their value
def repVar(check):
	#get every thing to be replaced
	#if starts with ! make variable, & is list, $ is color change, etc
	check = re.sub(r'(?<=~)\w+(?=~)', lambda x: var[x.group(0)], check).replace("~", "")
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
def jummp(rurn):
	line = int(rurn) - 2
def exec_next(lines):
	global jummp
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
	if str(cmd).startswith("#"):pass

	elif cmd == "txt":
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
		slpp = int(timeToSleep) / 100
		time.sleep(slpp)
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
				for word in args[3:]:
					toSet += repVar(word).replace("\n","")
					toSet += " "
				toSet = removeEnd(" ", toSet)
				var[vartochange] = toSet
			elif args[2] == "len":
				var[vartochange]=len(str(repVar(args[3])))
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
		elif kwargs == "bnk":var[vartochange]=""
		else:error("unknown variable type")
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
		# insertion of stuff
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
	#if line>len(totallines): raise KeyboardInterrupt
totallines = run.readlines()
complete = 0
while True:
	writeOut=open("output.txt", "w")
	writeOut.write(out)
	try:
		exec_next(totallines)
		complete += 1
	except IndexError:
		break
if devkey: cprint(f"Dev > Run Lines: {complete}", "magenta")
run.close()
writeOut.close()
print("")
out+="\n"
