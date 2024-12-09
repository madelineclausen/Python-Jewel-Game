# Madeline Clausen
# 60633236

class InvalidInput(Exception):
    """ Raised if input doesn't match specifications,
        caught by either type, value, or index error. """
    pass

class GameState:

    def __init__(self):
        self._board = [[], []]
        self._faller = []
        self._faller_active = False 

    def get_board(self) -> list:
        """ Returns the board """
        return self._board
    
    def create(self, rows: int, cols: int, inputs: list):
        """ Based on user input, adds a board with x
            rows (that the user can see) and y columns.
            Each space on the board is turned into a j
            ewel object. """
        try:
            for m in range(len(inputs[0])):
                self._board[0].append(Jewel('#', 'FROZEN'))
                self._board[1].append(Jewel('#', 'FROZEN'))
            for i in range(len(inputs)):
                self._board.append([])
            for j in range(2, len(inputs)+2):
                for char in inputs[j-2]:
                    self._board[j].append(Jewel(char, 'FROZEN'))
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def passage_of_time(self):
        """ Given "time", matches clear the board and
            fallers drop. """
        try:
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if self._board[i][j].state() == 'MATCH':
                        self._board[i][j].change_state('FROZEN')
                        self._board[i][j].change_value('#')
            if self._faller_active:
                GameState.drop_faller(self)
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def update(self):
        """ Looks for matches, drops frozen pieces
            (if any), and updates faller positions. """
        try:
            GameState.lower_all(self)
            for i in range(len(self._board)):
                for j in range(len(self._board[i])):
                    if self._board[i][j].state() == 'FALLING':
                        self._faller_active = True
            if self._faller_active:
                GameState._add_faller_to_board(self) 
            for m in range(len(self._board)):
                for n in range(len(self._board[m])):
                    if len(self._faller) == 2:
                        last_faller_index = 1
                    else:
                        last_faller_index = 2
                    if self._board[m][n].state() == 'LANDED':
                        if GameState.get_faller(self)[last_faller_index][1] != len(self._board)-1:
                            if self._board[(GameState.get_faller(self)[last_faller_index][1])+1][GameState.get_faller(self)[last_faller_index][2]].value() == '#':
                                self._board[m][n].change_state('FALLING')
                            else:
                                self._board[m][n].change_state('FROZEN')
                                self._faller_active = False
                        else:
                            self._board[m][n].change_state('FROZEN')
                            self._faller_active = False  
            for a in range(len(self._board)):
                for b in range(len(self._board[a])):
                    if self._board[a][b].state() == 'FALLING':
                        if a == (len(self._board)-1) or (self._board[a+1][b].value() != '#' and self._board[a+1][b].state() == 'FROZEN'):
                            for faller in self._faller:
                                faller[0].change_state('LANDED')
            GameState.check_match(self)
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()
        

    def check_match(self):
        """ Runs a check horizontally, vertivally,
            and diagonally looking for matches. """
        try:
            GameState._horizontal_match(self)
            GameState._vertical_match(self)
            GameState._foward_diagonal_match(self)
            GameState._backward_diagonal_match(self)
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def check_game_over(self) -> bool:
        """ Checks to see if conditions are right
            for game over. """
        try:
            for m in range(2):
                for n in range(len(self._board[m])):
                    if self._board[m][n].state() == 'FROZEN' and self._board[m][n].value() != '#':
                        GameState.passage_of_time(self)
                        GameState.update(self)
            for m in range(2):
                for n in range(len(self._board[m])):
                    if self._board[m][n].state() == 'FROZEN' and self._board[m][n].value() != '#':
                        return True
                    
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def lower_all(self):
        """ All frozen pieces are dropped to the
            bottom of the board. """
        try:
            x = 0
            while x < len(self._board):
                for i in range(len(self._board)-1):
                    for j in range(len(self._board[i])):
                        if self._board[i][j].state() != 'FALLING' and i != len(self._board)-1:
                            if self._board[i+1][j].value() == '#':
                                self._board[i+1][j].change_value(self._board[i][j].value())
                                self._board[i][j].change_value('#')
                x += 1
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

            
    def drop_faller(self):
        """ As opposed to dropping all frozen pieces,
            fallers fall one space per iteration. The
            row parameter of each faller is updated. """
        try:
            if len(self._faller) == 3:
                if self._faller[2][1] != len(self._board)-1:
                    if self._board[(self._faller[2][1] + 1)][self._faller[2][2]].value() == '#':
                        for faller in self._faller:
                            faller[1] += 1
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()
            
    def create_faller(self, column: int, falling_jewels: list):
        """ A new faller is created. However, before it
            is made, a check is run to see if the column
            the user inputted is already full of jewels.
            If it is, then just the first 2 fallers are
            implemented. This makes it go into a landing
            state and game over later. """
        try:
            if not self._faller_active:
                GameState.clear_faller(self)
                full_column_check = 0
                for x in range(2, len(self._board)):
                    if self._board[x][column-1].value() != '#':
                        full_column_check += 1
                if full_column_check == len(self._board) - 2:
                    faller_range = 2
                else:
                    faller_range = 3
                for i in range(faller_range):
                    self._faller.append([Jewel(falling_jewels[i], 'FALLING'), i, column-1])
                GameState._add_faller_to_board(self)
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def get_faller(self) -> list:
        """ Returns the faller """
        return self._faller

    def rotate_faller(self):
        """ Makes bottommost jewel the top of the faller,
            and shifts the first 2 jewels down. """
        try:
            if self._faller_active:
                self._faller[0][0], self._faller[2][0] = self._faller[2][0], self._faller[0][0]
                self._faller[1][0], self._faller[2][0] = self._faller[2][0], self._faller[1][0]
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()
            
    def clear_faller(self):
        """ Clears the faller and sets the "active
            faller" to false. This is used elsewhere
            when determining which methods to run. """
        self._faller = []
        self._faller_active = False
        
    def move_faller_left(self):
        """ Shifts the faller left by decrementing
            the column of each faller jewel by 1. """
        try:
            if self._faller_active:
                for m in range(len(self._board)-2):
                    for n in range(1, len(self._board[m])):
                        if n != 0:
                            if self._board[m][n-1].value() == '#' and self._board[m+1][n-1].value() == '#' and self._board[m+2][n-1].value() == '#':
                                if self._board[m][n].state() == 'FALLING' or self._board[m][n].state() == 'LANDED':
                                    if self._board[m+1][n].state() == 'FALLING' or self._board[m+1][n].state() == 'LANDED':
                                        if self._board[m+2][n].state() == 'FALLING' or self._board[m+2][n].state() == 'LANDED':
                                            for i in range(len(self._faller)):
                                                self._faller[i][2] -= 1
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()

    def move_faller_right(self):
        """ Shifts the faller right by incrementing
            the column of each faller jewel by 1. """
        try:
            if self._faller_active:
                for m in range(len(self._board)-2):
                    for n in range(len(self._board[m])-1):
                        if n != len(self._board[m]) - 1:
                            if self._board[m][n+1].value() == '#' and self._board[m+1][n+1].value() == '#':
                                if self._board[m+2][n+1].value() == '#' and self._board[m][n].state() in ('FALLING', 'LANDED'):
                                    if self._board[m+1][n].state() in ('FALLING', 'LANDED') and self._board[m+2][n].state() in ('FALLING', 'LANDED'):
                                        for i in range(len(self._faller)):
                                            self._faller[i][2] += 1
        except (ValueError, TypeError, IndexError):
            raise InvalidInput()
                                        
    def _add_faller_to_board(self):
        """ If the faller position has changed, this
            method updates the board to reflect the
            changes. """
        faller_count_test = []
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                for faller in self._faller:
                    if i == faller[1] and j == faller[2]:
                        self._board[i][j] = faller[0]
                    if (self._board[i][j].state() == 'FALLING' or self._board[i][j].state() == 'LANDED') and i != faller[1] and j != faller[2]:
                        self._board[i][j] = Jewel('#', 'FROZEN')
                       
                if self._board[i][j].state() == 'FALLING':
                    faller_count_test.append(i)
                    faller_count_test.append(j)
                    if len(faller_count_test) > 6:
                        self._board[faller_count_test[0]][faller_count_test[1]] = Jewel('#', 'FROZEN')
                
                    
        for a in range(1, len(self._board)):
            for b in range(len(self._board[i])):
                if a == self._faller[0][1] and b == self._faller[0][2]:
                    if self._board[a-1][b].value() != '#':
                        self._board[a-1][b].change_value('#')
                        self._board[a-1][b].change_state('FROZEN')
                    

    def _horizontal_match(self):
        """ Looks left and right for any matches. """
        for i in range(len(self._board)):
            for j in range(len(self._board[i])-2):
                if self._board[i][j].state() == 'FROZEN' and self._board[i][j+1].state() == 'FROZEN' and self._board[i][j+2].state() == 'FROZEN':
                    if self._board[i][j].value() == self._board[i][j+1].value():
                        if self._board[i][j].value() == self._board[i][j+2].value():
                            if self._board[i][j].value() != '#':
                                self._board[i][j].change_state('MATCH')
                                self._board[i][j+1].change_state('MATCH')
                                self._board[i][j+2].change_state('MATCH')
                                for m in range(len(self._board)):
                                    for n in range(len(self._board[i])-1):
                                        if self._board[m][n].state() == 'MATCH' and self._board[m][n+1].value() == self._board[m][n].value():
                                            self._board[m][n+1].change_state('MATCH')
                

    def _vertical_match(self):
        """ Looks up and down for any matches. """
        for i in range(len(self._board)-2):
            for j in range(len(self._board[i])):
                if self._board[i][j].state() == 'FROZEN' and self._board[i+1][j].state() == 'FROZEN' and self._board[i+2][j].state() == 'FROZEN':
                    if self._board[i][j].value() == self._board[i+1][j].value():
                        if self._board[i][j].value() == self._board[i+2][j].value():
                            if self._board[i][j].value() != '#':
                                self._board[i][j].change_state('MATCH')
                                self._board[i+1][j].change_state('MATCH')
                                self._board[i+2][j].change_state('MATCH')
                                for m in range(len(self._board)-1):
                                    for n in range(len(self._board[i])):
                                        if self._board[m][n].state() == 'MATCH' and self._board[m+1][n].value() == self._board[m][n].value():
                                            self._board[m+1][n].change_state('MATCH')
        
    def _foward_diagonal_match(self):
        """ Looks from top left to bottom right for any matches. """
        for i in range(len(self._board)-2):
            for j in range(len(self._board[i])-2):
                if self._board[i][j].state() == 'FROZEN' and self._board[i+1][j+1].state() == 'FROZEN' and self._board[i+2][j+2].state() == 'FROZEN':
                    if self._board[i][j].value() == self._board[i+1][j+1].value():
                        if self._board[i][j].value() == self._board[i+2][j+2].value():
                            if self._board[i][j].value() != '#':
                                self._board[i][j].change_state('MATCH')
                                self._board[i+1][j+1].change_state('MATCH')
                                self._board[i+2][j+2].change_state('MATCH')
                                for m in range(len(self._board)-1):
                                    for n in range(len(self._board[i])-1):
                                        if self._board[m][n].state() == 'MATCH' and self._board[m+1][n+1].value() == self._board[m][n].value():
                                            self._board[m+1][n+1].change_state('MATCH')
        
    def _backward_diagonal_match(self):
        """ Looks top right to bottom left for any matches. """
        for i in range(1, len(self._board)-1):
            for j in range(1, len(self._board[i])-1):
                if self._board[i][j].state() == 'FROZEN' and self._board[i-1][j+1].state() == 'FROZEN' and self._board[i+1][j-1].state() == 'FROZEN':
                    if self._board[i][j].value() == self._board[i-1][j+1].value():
                        if self._board[i][j].value() == self._board[i+1][j-1].value():
                            if self._board[i][j].value() != '#':
                                self._board[i][j].change_state('MATCH')
                                self._board[i-1][j+1].change_state('MATCH')
                                self._board[i+1][j-1].change_state('MATCH')
                                for m in range(len(self._board)-1):
                                    for n in range(len(self._board[i])-1):
                                        if self._board[m][n].state() == 'MATCH' and self._board[m-1][n+1].value() == self._board[m][n].value():
                                            self._board[m-1][n+1].change_state('MATCH')
                                        if self._board[m][n].state() == 'MATCH' and self._board[m+1][n-1].value() == self._board[m][n].value():
                                            self._board[m+1][n-1].change_state('MATCH')

class Jewel():
    def __init__(self, char: str, standing: str):
        self._char = char
        self._standing = standing

    def jewel(self) -> list:
        """ Returns list containing jewel elements. """
        return [self._char, self._standing]
    
    def value(self) -> str:
        """ Returns string containing jewel value. """
        return self._char
    
    def state(self) -> str:
        """ Returns string containing jewel state. """
        return self._standing
    
    def change_value(self, new_value: str):
        """ Updates jewel value. """
        self._char = new_value

    def change_state(self, new_state: str):
        """ Updates jewel state. """
        self._standing = new_state
