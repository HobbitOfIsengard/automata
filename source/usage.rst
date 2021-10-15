.. _usage:

Getting Started
===============
After downloading the file, all what is necessary is to create an :class:`Automata` object and either call run or just switch a input string. An example of this could be ::
  
  from automata import *
  import sys
  
  automata = Automata(sys.argv[1])
  automata.run()

Syntax
------
Per default there are 9 encoded options for a line:
 - Empty/Comment
 - Assignment
 - Connection
 - Ask
 - Clear
 - Load
 - Run
 - Import
 - Name  

Empty / Comment
###############
The empty or comment lines are either empty or begin with a "#" ::

  # The first line is empty
   

Assignment
##########
This line consists of 2 aspects, a name and value pair, connected by the assignment operator.  The parser will take all characters before the assignment operator " = " as the name of the constant, and all characters after as the value.  If one wants to add two variables together just create a new variable which and add both variable names in succession seperated by a "," ::

  # Define list one.  The spaces around the = sign are important!
  list1 = abcdefghikjlmnopqrstuvwxyz

  # Define list two.
  list2 = ABCDEFGHIKJLMNOPQRSTUVWXYZ

  # Define list three as a combination of list one and two.
  # Notice spaces around the = and no spaces around the ,
  list3 = list1,list2

Connection
##########
This assignment connects two states, and implicitly defines them.  The syntax for this is: `<name 1> (<transition>)-> <name 2>`.  The states which are accepting, must start with the prefix f ::
   
  # Creating a transition between states one and two
  s1 (list2)-> f1

  # Transitioning to the same state
  f1 (list1)-> f1

  # Using a " " or a "-" character as a transition instead of a defined variable
  f1 ( -)-> s1

Ask
###
The ask statement can be run by itself or with the options `t:`, `m:` or `f:`.  The `t:` option provides test functionality, where the string after `t:` will be passed directly to the first node of the graph (being the node first declared in the graph for a connection).  The `m:` option or message option changes the default commandline query message - "Input a string to check: " - to something to the programmers choice.  Lastly the `f:` option specifies the handler function used by the function to handle the graph results.  Per default this is `print` and will simply print out the automata name and the value.  This can be customized by writing a function `<handle>` in a file called `<handle_file>` which accepts an :class:`Autonoma` as its first argument and a boolean result as its second.  This file must be imported before using.  Examples of the ask statement are ::
  
  ask

  ask t: Test
  ask m: Input your name

  import handle_file
  
  ask m: Input your name f: handle

Clear
#####
The statement `clear` is used to clear the variables and/or states from memory ::
  
  # clears all variables
  clear variables

  # clears all states
  clear states

  # clear states and variables
  clear all

Load
####
The `load` statement is followed by a string `name`. This parameter value is the name (without extension) of the file which the function will read in.  The function will append the variables defined in `<name>.txt` and :class:`States` defined in the file to the current automata ::

  # load file vars.txt
  load vars

Save
####
The `save` statement is followed by a string `name`. This parameter value is the name (without extension) of the file which the function will then (over)write (`<name>.txt`) ::

  # write the automata out to name.txt
  save name

Import
######
This statement dynamically loads the specified file to a variable.  This variable will be overwritten if another file is imported.  Functions in the file will be executed when ask is called ::
  
  import handle_file

Name
####
This simple statement changes the name of the automata, usefull for comparing and printing the automata ::

  name myAutonoma

  
Chaining automatas
------------------
A single txt file can contain multiple automatas, although a way to save an automata has not yet been implemented, chaining Automatas is as simple as using the clear statement ::

  list1 = abcdefghikjlmnopqrstuvwxyz
  list2 = ABCDEFGHIKJLMNOPQRSTUVWXYZ

  # Define Automata
  f1 (list1)-> f1

  # This clears the automata itself leaving all variables accessible for the next automata
  clear states

  # Next Automata
  f1 (list2)-> f2
  
For more comprehensive examples check out the :doc:`Downloads <downloads>` page!

Example code
------------
Check out the downloads page for more comprehensive examples

A static automata asking the user to check for space seperated words which begin with an uppercase character followed by any amount of lowercase characters:

main.py: ::

  from automata import *
  import sys
  
  automata = Automata("automata.txt")
  automata.run()

automata.txt: ::

   # Define list one.  The spaces around the = sign are important!
   list1 = abcdefghikjlmnopqrstuvwxyz
   
   # Define list two.
   list2 = ABCDEFGHIKJLMNOPQRSTUVWXYZ

   # Creating a transition between states one and two
   s1 (list2)-> f1
   
   # Transitioning to the same state
   f1 (list1)-> f1

   # Using a " " or a "-" character as a transition instead of a defined variable
   f1 ( -)-> s1

   ask m: Input your name:

   clear all

A more interactive approach at a console type structure would be replacing main.py by: ::
  
  from automata import *
  automata = Automata()
  
  print("This is an Automata console input q to quit")
  
  line = ""
  
  while not line == "q":
    try:
        automata.switch(line, 0)
    except ValueError:
        print("The entered line has no known iterpretation please try a different line:")
    line = input("> ").strip()
