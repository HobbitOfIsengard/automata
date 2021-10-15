import importlib
class State(object):
    """
    Base module node for an :class:`Automata` graph. Connects to other nodes, which ultimately evaluate the acceptance of a string inputed by the user

    :param __name__: The name of the :class:`State`.  This is used for identification purposes
    :type __name__: str
    :param __transitions: The connections inbetween nodes.  Forms a connection between one node and the next.  The transition to the next :class:`State` object is taken if the first character of the string is contained in the __transitions[x][1] string
    :type __transitions: [[:class:`State`, str]]
    :param __final: Checks wether the :class:`State` is a final :class:`State`, meaning that if no further characters are in the string, if the result will be true or false
    :type __final: bool
    """
    def __init__(self,name,final = False):
        """
        Constructor for class State

        :param name: Name for :class:`State` node.  Crucial for indexing in the indexing of an :class:`Automata`.  Used for comparison when parsing txt file
        :type name: String
        :param final: Optional parameter which indicates when the node recieves an empty string, whether to return true or false.
        :type final: Boolean
        """
        self.__name__ = name
        self.__transitions = []
        self.__final = final

    def __eq__(self, other):
        """
        Equality operator overload

        :param other: Other State object to be checked for equality
        :type other: State
        :return: A comparison between the name of the two class:`State` objects
        :rtype: bool
        """
        return self.__name__ == other.__name__

    def __str__(self):
        """
        String representation of :class:`State` object

        :return: Returns the object name as string representation
        :rtype: str
        """
        return self.__name__

    def __repr__(self):
        """
        String representation of :class:`State` object

        :return: Returns the object name as string representation
        :rtype: str
        """

        return self.__name__()

    
    def add(self,state, transition):
        """
        Member which adds a transition to the transition graph of the node.
        
        :param state: The state in which is to be transitioned if the first member of the parsing string is in transition
        :type state: :class:`State`
        :param transition: A string of characters which identifies the nessesary transition based on a input character
        :type transition: str
        """
        self.__transitions.append([state, transition])

    def evaluate(self,string):
        """
        Recursive function which recursively goes through the transition graph of each node, determining if when all characters in the input string are parsed, if the graph evaluates the given input as True (if parsing ends in a __final :class:`State`) or otherwise False.  The function prints the graph path taken in the console.

        :param string: The String which is to be recursively parsed throughout the graph
        :type string: str
        """
        print(" --> ", end = "")
        if len(string) == 0:
            print("(" + self.__name__+",\u03B5)")
            return self.__final
        
        for t in self.__transitions:
            if string[0] in t[1]:
                print("(" + self.__name__+","+string+")", end = "")
                return t[0].evaluate(string[1:])
        print()
        return False

    def transitions(self):
        return self.__transitions

class Automata(object):
    """
    Automata class parser.  This class constructs a graph of :class:`State`'s based on a parsed txt file.  The class also allowes for a more dynamic approach by giving direct access to the parser :meth:`switch`, which takes a line and parses it out to functions.  The class is made to be subclassed to extend the basic parser functionality.

    :param __filename: Optional name of file which is parsed when calling :meth:`run`
    :type __filename: str
    :param __variables: List which stores name value pairs\
    of the constant variables instanced in the program
    :type __variables: [name,value]
    :param __states: List of states in the graph.  Used to build up a list which contains one entry with each state.  The states are then connected to form the evaluating transition graph
    :type __states: [class::`State`]
    :param __module: The python modules which can be improted to handle the ask result
    :type __module: [name, module name]
    """
    def __init__(self,filename = "", name = ""):
        """
        Constructor for class :class:`Automata`

        :param filename: optional parameter for the filename with relative path to the python script
        :type filename: str
        """
        self.__filename = filename
        self.__variables = []
        self.__states = []
        self.__module = None
        self.__name__ = name

    def __eq__(self, other):
        """
        Equality operator overload
            
        :param other: Other State object to be checked for equality
        :type other: :class:`Automata`
        :return: A comparison between the name of the two class:`State` objects
        :rtype: bool
        """
        return self.__name__ == other.__name__

    def __str__(self):
        """
        String representation of :class:`Automata` object

        :return: Returns the object name as string representation
        :rtype: str
        """
        return self.__name__

    def __repr__(self):
        """
        String representation of :class:`Automata` object

        :return: Returns the object name as string representation
        :rtype: str
        """

        return self.__name__()

    
    def __blank(self, name):
        """
        Placeholder function, returns its parameter
        :param: name
        :rval: name
        """
        return name
    def __get_transition(self, name):
        """
        Member function to get the transition stored in __variables given a name for the transition.  If multiple comma seperated names are given, the names are split and returned

        :param name: name of transition
        :return: String with all transitions which are available under the comma seperated names given.
        :rtype: str
        """
        names = name.split(",")
        returnval = ""
        for n in names:
            for v in self.__variables:
                if v[0] == n:
                    returnval += v[1]
        if returnval == "":
            return name
        return returnval

    def __comment(self,line):
        """
        Member function which is called when a comment (line beginning with #) or empty line is read in
        
        :param line: the parsed line (for subclassing purposes)
        :type line: str
        """
        pass
    
    def __assign(self,line):
        """
        Parses the line argument by taking the string before " = " as the name and the string after as the value.  If another variable or comma seperated list of variables is given, the combined value of these variables is stored under the transition value.

        :param line: the parsed line
        :type line: str
        """
        self.__variables.append([line.split(" = ")[0],
                              self.__get_transition(line.split(" = ")[1])])

    def __connect(self, line):
        """
        Parses the line argument by creating 2 states out of the first characters before " (" and the characters after the "-> ".  If the name of these states is already present use those states otherwise add new states.  Then use the transition specified by the value inbetween the parentheses to connect the two graph nodes.

        :param line: the parsed line
        :type line: str
        """
        s1 = State(line.split(" (")[0],"f" == line.split(" (")[0][0])
        if not s1 in self.__states:
            self.__states.append(s1)
        s2 = State(line.split(" (")[1].split(")-> ")[1],
                   "f" == line.split(" (")[1].split(")-> ")[1][0])
        if not s2 in self.__states:
            self.__states.append(s2)
            
        self.__states[self.__states.index(s1)].add(
            self.__states[self.__states.index(s2)],
            self.__get_transition(line.split(" (")[1].split(")-> ")[0]))

    def __ask(self, line):
        """
        Asks the user for an input.  Different flags can be set to enrich the input.  If no flags are set, then the default message will appear to the reader: "input a string to check: ".  Modifications to the output message are possible using the " m: " flag.  This flag will lead to a change of query message to the user.  A test flag " t: " can be used to statically code the string passed to the automata.  The default handler for the result is print, meaning the output of the graph will simply be printed in the console. To override this behavior and use the value provided by the automata, all what has to be done is using the :meth:`__import_file`, import the python file containing your handler (you may only load one file at a time, the file can change throughout the program if so implemented), and then use the " f: " option on the ask statement, where the name of the handler has to be stated.

        :param line: the parsed line
        :type line: str
        """
        line = self.__combine(line.split(" "),["t:","m:","f:"])

        if len(line) == 1:
            print(self.__states[0].evaluate(input("input string to check: ")))
            return

        eval_statement = ""
        out_func = print
        eval_func = input
        
        if "t:" in line:
            eval_statement = line[line.index("t:")+1]
            eval_func = self.__blank
        if "m:" in line:
            eval_statement = line[line.index("m:")+1]
            eval_func = input
        if "f:" in line:
            out_func = getattr(self.__module, line[line.index("f:")+1])

        out_func(self, self.__states[0].evaluate(eval_func(eval_statement)))
        
    def __clear(self, line):
        """
        Clears the variables, __variables and __states, so that they can be redifiend, allowing for multiple Automata defined in the same file, and parsed by the same object.

        :param line: the parsed line
        :type line: str
        """
        if line[6:] == "all": 
            self.__variables = []
            self.__states = []
        elif line[6:] == "variables":
            self.__variables = []
        elif line[6:] == "states":
            self.__states = []

    def __rest(self, line, index):
        """
        This function is called by :meth:`switch` if no parsing method is provided.  This method can easily be subclassed to extend the current switch functionality and not tampering with the default parsing settings.  Per default this function raises a ValueError to inform the programmer of their parsing mistake.
        
        :param line: the parsed line
        :type line: str
        :param index: the line index
        :type index: int
        :raises ValueError: The given string does not correspond with a known parsing method writes out line index and line for debugging purposes. 
        """
        raise ValueError(f'No known interpretation for line {index}: {line}')

    def __save(self, name):
        """
        Loops through all states and writes them into a file, with the passed name.  This automata can be loaded later in the program using :meth:`load`
        
        :param name: name without extension of the file the automata should be saved to
        :type name: str
        """
        with open(f"{name}.txt",'w') as f:
            for s in self.__states:
                for t in s.transitions():
                    f.write(f"{str(s)} ({t[1]})-> {str(t[0])}\n")
            f.write("ask")

    def __load(self,name):
        """
        Loops through all lines in the file <name>.txt and passes them to the parsing function :meth:`switch`
        
        :param name: name without extension of the file which contains the automata configuration
        :type name: str
        """
        with open(name,'r') as f:
            for i,l in enumerate(f):
                l = l.strip()
                self.switch(l,i+1)

    def __import_file(self, name):
        """
        A function which takes a certain python file and makes it accessible by the automata
        
        :param name: name of the file without .py extension
        :type name: str
        """
        self.__module = importlib.import_module((name))

            
    def __combine(self, ilist, slist, split = " "):
        """
        This function takes a input list and a string list and combines all the i list entries inbetween the entries noted in the string list.  The combination adds the split string between each joining of strings

        :param ilist: a list with strings to be combined 
        :type ilist: [str]
        :param slist: a list with the strings which should not be combined and thus indicate a new entry in the returned list
        :type slist: [str]
        :param split: the character with which the list was created in a split
        :type split: str
        """
        current = ""
        returnlist = []
        for i in ilist:
            if i in slist:
                returnlist.append(current)
                returnlist.append(i)
                current = ""
            else:
                if not len(current) == 0:
                    current += split
                current += i 
        returnlist.append(current)
        return returnlist
        
    def __set_name(self, name):
        """
        A function which sets the name of the automata.  This is usefull during comparison and printing results.
        """
        self.__name__ = name

    def switch(self,line, index):
        """
        Parses the line and calls the appropriate function for the given line.  Furthermore gives the user the ability to interactivly parse lines
        
        :param line: the parsed line (for subclassing purposes)
        :type line: str
        :param index: the line index
        :type index: int
        """
        if len(line) == 0 or line[0] == "#":
            self.__comment(line)
        elif " = " in line:
            self.__assign(line)
        elif "(" in line:
            self.__connect(line)
        elif "ask" == line[:3]:
            self.__ask(line)
        elif "clear" == line[:5]:
            self.__clear(line)
        elif "save" == line[:4]:
            self.__save(line[5:])
        elif "load" == line[:4]:
            self.__load(line[5:])
        elif "import" == line[:6]:
            self.__import_file(line[7:])
        elif "name" == line[:4]:
            self.__set_name(line[5:])
        else:
            self.__rest(line,index)
        
    def run(self):
        """
        :meth:`load`'s the main file __filename

        """

        self.__load(self.__filename)

