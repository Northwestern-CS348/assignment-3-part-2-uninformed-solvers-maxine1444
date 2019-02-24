from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        disk_dict = {'disk1': 1, 'disk2': 2, 'disk3': 3, 'disk4': 4, 'disk5': 5}

        #check if any of the pegs are empty

        ask1 = parse_input("fact: (empty peg1")
        answer1 = self.kb.kb_ask(ask1)
        if (answer1): #if peg1 is empty
            p1_tuple = () #empty tuple
        else:
            ask2 = parse_input("fact: (on ?x peg1")
            matches = self.kb.kb_ask(ask2)
            peg_num = []
            
            for item in matches: #loop through each binding to find the disk
                value = item.bindings_dict['?x'] #get the disk number
                peg_num.append(disk_dict[value]) #look in disk dict to get the actual number
            peg_num.sort() 
            p1_tuple = tuple(peg_num) #convert list to tuple
   
        ask3 = parse_input("fact: (empty peg2")
        answer2 = self.kb.kb_ask(ask3)
        
        if (answer2): #if peg1 is empty
            p2_tuple = () #empty tuple
        else:
            ask4 = parse_input("fact: (on ?x peg2")
            matches = self.kb.kb_ask(ask4)
            peg2_num = []
           
            for item in matches: #loop through each binding to find the disk
                value = item.bindings_dict['?x'] #get the disk number
                peg2_num.append(disk_dict[value]) #look in disk dict to get the actual number
            peg2_num.sort()
            p2_tuple = tuple(peg2_num) #convert list to tuple
        
        ask5 = parse_input("fact: (empty peg3")
        answer3 = self.kb.kb_ask(ask5)
        if (answer3): #if peg1 is empty
            p3_tuple = () #empty tuple
        else:
            ask6 = parse_input("fact: (on ?x peg3")
            matches = self.kb.kb_ask(ask6)
            peg3_num = []
           
            for item in matches: #loop through each binding to find the disk
                value = item.bindings_dict['?x'] #get the disk number
                peg3_num.append(disk_dict[value]) #look in disk dict to get the actual number
            peg3_num.sort()
            p3_tuple = tuple(peg3_num) #convert list to tuple

        result_tuple = (p1_tuple, p2_tuple, p3_tuple)
        return result_tuple

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        #check if its a movable statement
        if (movable_statement.predicate == "movable"):
            if self.isMovableLegal(movable_statement): #check if the movable statement is legal
                disk = str(movable_statement.terms[0])
                initial = str(movable_statement.terms[1])
                target = str(movable_statement.terms[2])
                game_state = self.getGameState() 

                oldfact = "fact: (on " + disk + " " + initial + ")"
                self.kb.kb_retract(parse_input(oldfact)) #retract the old on fact in kb
                oldtop = "fact: (topstack " + disk + " " + initial + ")"
                self.kb.kb_retract(parse_input(oldtop)) #retract the old topstack fact in kb

                ask2 = parse_input("fact: (on ?x " + initial + ")")
                answer2 = self.kb.kb_ask(ask2)

                if (not answer2): #if there aren't any disks on the peg
                    empty_fact = "fact: (empty " + initial + ")" 
                    self.kb.kb_assert(parse_input(empty_fact)) #assert the fact that the initial peg is empty now
                else:
                    disk_below = "disk" + str(game_state[int(initial[-1])-1][1])
                    disk_below_fact = "fact: (topstack " + disk_below + " " + initial + ")"
                    self.kb.kb_assert(parse_input(disk_below_fact))

                #check if the target peg is empty or not
                ask1 = parse_input("fact: (empty " + target + ")")
                answer1 = self.kb.kb_ask(ask1)
                
                if (answer1): #if its empty/True
                    self.kb.kb_retract(ask1) #retract the fact that its empty
                else: #if there are other larger disks on the target peg already, retract their topstack fact 
                    there = "disk" + str(game_state[int(target[-1])-1][0])
                    pasttopfact = "fact: (topstack " + there + " " + target + ")"
                    self.kb.kb_retract(parse_input(pasttopfact)) #retract the previous topstack fact

                newfact = "fact: (on " + disk + " " + target + ")"
                self.kb.kb_assert(parse_input(newfact)) #add new position fact to kb

                newtop = "fact: (topstack " + disk + " " + target + ")"
                self.kb.kb_assert(parse_input(newtop)) #add new position fact to kb
                
                factslist = self.kb.facts
                for f in factslist:
                    print(str(f))

                ruleslist = self.kb.rules
                for r in ruleslist:
                    print(str(r))

                return
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        tile_dict = {"tile1": 1, "tile2": 2, "tile3": 3, "tile4": 4, "tile5": 5, "tile6": 6, "tile7": 7, "tile8": 8, "empty": -1}
        xpos_dict = {"pos1": 0, "pos2": 1, "pos3": 2}

        ask1 = parse_input("fact: (on ?t ?x pos1)")
        matches = self.kb.kb_ask(ask1)
        row1 = [0,0,0]
           
        for item in matches: #loop through the tiles in the first row
            xpos = item.bindings_dict['?x'] #get the x position
            xpos1 = xpos_dict[xpos] #get the index number
            value = item.bindings_dict['?t'] #get the disk number
            row1[xpos1] = tile_dict[value] #look in disk dict to get the actual number   
        r1_tuple = tuple(row1) #convert list to tuple

        ask2 = parse_input("fact: (on ?t ?x pos2)") #second row
        matches = self.kb.kb_ask(ask2)
        row2 = [0,0,0]
           
        for item in matches: #loop through the tiles in the 2nd row
            xpos2 = item.bindings_dict['?x'] #get the x position
            xpos22 = xpos_dict[xpos2] #get the index number
            value = item.bindings_dict['?t'] #get the disk number
            row2[xpos22] = tile_dict[value] #look in disk dict to get the actual number 
        r2_tuple = tuple(row2) #convert list to tuple

        ask3 = parse_input("fact: (on ?t ?x pos3)")
        matches = self.kb.kb_ask(ask3)
        row3 = [0,0,0]
           
        for item in matches: #loop through the tiles in the first row
            xpos = item.bindings_dict['?x'] #get the x position
            xpos1 = xpos_dict[xpos] #get the index number
            value = item.bindings_dict['?t'] #get the disk number
            row3[xpos1] = tile_dict[value] #look in disk dict to get the actual number 
        r3_tuple = tuple(row3) #convert list to tuple

        result_tuple = (r1_tuple, r2_tuple, r3_tuple)
        return result_tuple
        
        #pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        if (movable_statement.predicate == "movable"):
            if self.isMovableLegal(movable_statement): #check if the movable statement is legal
                tile = str(movable_statement.terms[0])
                x1 = str(movable_statement.terms[1])
                y1 = str(movable_statement.terms[2])
                x2 = str(movable_statement.terms[3])
                y2 = str(movable_statement.terms[4])

                #switch positions of empty and the tile 
                oldtile = parse_input("fact: (on " + tile + " " + x1 + " " + y1 + ")")
                oldempty = parse_input("fact: (on empty " + x2 + " " + y2 + ")")
                #retract the old tile and empty position facts

                self.kb.kb_retract(oldtile)
                self.kb.kb_retract(oldempty)

                newtile = parse_input("fact: (on " + tile + " " + x2 + " " + y2 + ")")
                newempty = parse_input("fact: (on empty " + x1 + " " + y1 + ")")
                #assert the new tile and empty position facts
                self.kb.kb_assert(newempty)
                self.kb.kb_assert(newtile)
                

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
