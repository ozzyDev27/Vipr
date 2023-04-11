# Hello!
Vipr is a high-level language pretending to be a low-level one, making it not very efficient.  
However, it is fun to use and to learn the basics of programming with :D  
It is my first "large" project, and helped me learn a lot!
# Getting Started
## Code Window
The code window is the text area on the left of the screen.  
This is where you enter your code, and the code gets run!
## Console
The console window is the text area on the right of the screen.  
This is where all the code gets run, and you see the output!
## Run Button
When you press this, the code you have typed gets run!  
It also allows you to stop the code, when it is running.
# Commands
## Text and Printing
Using the command `txt` allows you to print anything after it, for example,
```txt Hello world!``` 
You may also use any variables that have been
declared, using a `~`. For example, if a "name" variable had been declared, you could say
```txt Hi, my name is ~name~```
There is also the `new` command, allowing you to make a new line based on the argument, for example, `new 2` would be the same as pressing enter twice. Redundant, possibly.
## Waiting / Sleeping
Using the command `slp` is really simple, as it merely makes the program wait for an amount of time before going to the next line. If I were to type
```slp [enter int here]```, where it would wait for n seconds, where n is the integer inputted divided by 100.
You may also use a variable that is an integer using
```slp ~variable```
## Jumping, Trying, Returns and Labels
Jumping  is Vipr's form of loops and if statements. Each one has its own respective command, with jumping being `jmp`,trying being `try`, returns being `rtn`, and labels being `lbl`.
### Jumping
The jump command makes it go to another line, so if I were to input
```jmp 13```
it would jump to line 13, and read line 13 onwards.
You may also use a variable that is an integer, using 
```jmp ~variable~```
### Trying
Trying is slightly more complex, where you can check if something (can be a string, a variable, etc) is equal, less (must be numbers), or greater (must be numbers) than another thing (string, variable, etc). Examples:
Check if variable "number" is greater than 27, if it is, go to line 6
```try 6 grt ~number~ 27```
You can replace `grt` with `lss` (check if it is less) or `eql` (check if it is equal, also works with strings)
### Returns
After you make a jump or a try, you can use `rtn` to go back to the line you were at, making it really easy to make functions.
### Labels
To use label, use the `lbl` command. Labels make it super easy to make functions or go back to a part of the code. Setting a label allows you to make a name for that part of the code, and you can insert that name and it jumps you back!
To set a label, use
```lbl set name```
This would set a label on that line as "name".
If you want to go back to that line, you can use
```lbl jmp name```
Which would allow you to jump back to the line!
# Variables
Variables in Vipr are easily the most important things, and you can do a lot with them. Use the `var` command with the variable name after it, and then anything you want!
## Strings
To use the string command, use `var str`, and then another argument afterwards. There are a few things you can do with strings, such as simply setting it:
`var hello str set Hello, world!`
You may also use variables in this.
You can also merge two strings, using the `mrg` argument:
```
var greeting str set Hi there, 
var name str set Bill
var sayHi str mrg ~greeting~ ~name~
```
In this case, the variable `sayHi` would be `Hi there, Bill`.
Unfortunately, you can only use variables in this.
### Length of a string
To get the length of a string, use the `len` argument, or
```var length str len ~name~```
This would get the length of the variable `name`, for example, if `name` were to be `Jamie`, it would return 1.
## Inputs
Using the `inp` argument (`var name inp Text here`) you can get the users input! Anything after the `inp` will print out, and the user can type anything in, and the variable gets set to that! You can also use variables in the text! Example:
```var name inp Hi there! What's your name?```
## Copying
Copying a variable is a really simply task, merely using the `cmd` argument, or for example:
```var name cpy blank```
In this example, the new variable `name` would be the same as the variable `blank`.
## Blank Variables
Blank variables are another really simple thing, using the `bnk` argument, or for example:
```var name bnk```
The variable `name` would be blank, having nothing in it.
## Numbers and Arithmetics
This is going to be long.
### Setting a number
To set a number as a number (float/int), use the `num set`, or ```var name num set 27```.
In this case, the variable `name` would be 27.
### Addition
To add two numbers, use `num add`, or ```var name num add ~epicNumber 27```.
In this case, the new variable, `name`, would return the variable `epicNumber` plus 27! You can add two variables, two numbers, anything!
### Subtraction
To subtract a number from another, use `num sub`, or ```var name num sub ~epicNumber~ 27```.
In this case, the new variable, `name`, would return the variable `epicNumber` minus 27!
### Multiplication
To multiply two numbers, use `num mlt`, or ```var name num mlt ~epicNumber~ 27```.
In this case, the new variable, `name`, would return the variable `epicNumber` times 27!
### Division
To divide a number by another, use `num div`, or ```var name num div ~epicNumber~ 27```.
In this case, the new variable, `name`, would return the variable `epicNumber~` divided by 27!
### Random Number
To get a random number, use the `num rng` command.
```var name num rng 6 27```
The new variable, `name`, would return a random number from 6 to 27. You may also use a variable!
### Rounding
To round a number to its nearest whole, use the `num rnd` command.
```var name num rnd 27.2```
The new variable, `name`, would return 27, as 27.2 rounded is 27. You may also use variables!
If you want to round it up, you can use the `num cil` command instead of `num rnd`, and if you want to round down, use the `num flr` command instead.
### Sine, Cosine, Tangent
To use sine, cosine, or tangent, you can use `sin`, `cos`, and `tan` respectively! Example:
```var name num sin 45```
The new variable, `name`, would return the sin of 45! You can also use variables!
### Modulus
To use the modulus (remainder) operation, use the command `mod`, for example:
```var name num mod 27 7```
This would return 27 mod 7, or 6.
You can also use variables!
### Exponents
To use an exponent, use the `pwr` command!
For example:
```var name num pwr 3 4```
The new variable, `name`, would return 3 to the power of 4, or 81!
