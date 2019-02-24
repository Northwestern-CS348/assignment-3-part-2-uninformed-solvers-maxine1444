
from solver import *
from queue import Queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        if self.currentState.state == self.victoryCondition:   # check if already won
            return True
        moves = self.gm.getMovables()  # returns a list of movable 
        child_depth = self.currentState.depth + 1
        step = False
        print("**********")
        print ("Current State" + str(self.currentState.state))
        print ("Movables:")
        if moves:
            for m in moves:
                print (str(m))
        print("**********")
        while not step:  
            if len(moves) <= self.currentState.nextChildToVisit:  
                if self.currentState.parent:  
                    self.gm.reverseMove(self.currentState.requiredMovable)  # reverse move
                    moves = self.gm.getMovables()  
                    self.currentState = self.currentState.parent  #go back to being parent
                    child_depth = self.currentState.depth + 1
                    continue
                else:  # no parents 
                    print("No more parents found!")
                    return False
            first_move = moves[self.currentState.nextChildToVisit]
            self.gm.makeMove(first_move)
            newGameState = self.gm.getGameState()
            new_state = GameState(newGameState, child_depth, first_move)
            if new_state not in self.visited:  #explore the unvisited state
                new_state.parent = self.currentState  
                self.currentState.children.append(new_state)
                self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1 
                self.currentState = new_state  # moves to new state
                step = first_move  # this breaks out of loop
            else:  #we've already visited this
                self.gm.reverseMove(first_move)  
                self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
        state = self.currentState.state
        if state == self.victoryCondition:  #check if won
            return True
        else:
            self.visited[self.currentState] = True  #add to visited bc not win yet
            return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.bfs_queue = Queue()
        self.bfs_queue.put([self.currentState, []])
        self.first_move = False

    def _init_game_master(self):
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if (not self.first_move):
            self.first_move = True
            if self.solveOneStep():
                return True

        #initializing the queue
        if self.bfs_queue:
            self._init_game_master()
            top = self.bfs_queue.get()
            new_state = top[0]
            steps = top[1]

            for s in steps:
                self.gm.makeMove(s)
            if new_state.state == self.victoryCondition:   # check if already won
                return True

            self.visited[new_state] = True
            moves = self.gm.getMovables()  # returns a list of movable 
            
            for m in moves:
                self.gm.makeMove(m)
                gm1 = GameState(self.gm.getGameState(), 0, None)
                if(((new_state.parent is not None) and (self.gm.getGameState() == new_state.parent.state))) or gm1 in self.visited:
                    self.gm.reverseMove(m)
                    continue
                gm2 = GameState(self.gm.getGameState(), 0, None)
                self.visited[gm2] = True

                new_move = []
                for i in steps:
                    new_move.append(i)

                new_move.append(m)
                ns_depth = new_state.depth + 1
                next_state = GameState(self.gm.getGameState(), ns_depth, m)
                next_state.parent = new_state
                new_state.children.append(next_state)
                self.bfs_queue.put([next_state, new_move])
                self.gm.reverseMove(m)
            self.currentState = new_state
            print ("Current State" + str(self.currentState.state))
        else: #return False, can't found
            print("Can't reach desired solution")
            return False
