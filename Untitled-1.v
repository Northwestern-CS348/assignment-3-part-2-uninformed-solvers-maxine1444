#check if the game has already won or not
        if (self.currentState.state == self.victoryCondition): 
            return True
        step = False
        movables = self.gm.getMovables() #get all the possible movable statements
        childDepth = self.currentState.depth + 1
        while (not step): #while the next step isn't there
            next_child = self.currentState.nextChildToVisit
            if(len(movables) <= next_child): #we reached the leaf node
                if(self.currentState.parent is not None): #if there aren't any parents
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    movables = self.gm.getMovables()
                    self.currentState = self.currentState.parent #now is the parent 
                    childDepth = self.currentState.depth + 1
                    continue
                    #return False
                else: #there are parents 
                    return False
                    # self.gm.reverseMove(self.currentState.requiredMovable)
                    # movables = self.gm.getMovables()
                    # self.currentState = self.currentState.parent #now is the parent 
                    # childDepth = self.currentState.depth + 1
                    # continue
            first_move = movables[next_child]
            self.gm.makeMove(first_move)
            newGameState = self.gm.getGameState()
            next_state = GameState(newGameState, childDepth, first_move) #instantiate new game state
            if (next_state in self.visited): #if its already visited
                self.gm.reverseMove(first_move) #go back to current node to do a different step
                self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
            else: #if it hasnt been visited yet
                    #time to explore!
                next_state.parent = self.currentState
                self.currentState.children.append(next_state)
                self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
                self.currentState = next_state
                step = first_move
        if (self.currentState.state != self.victoryCondition): 
            self.visited[self.currentState] = True 
            return False
        else: 
            return True