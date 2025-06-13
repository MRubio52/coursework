import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
    

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        #Mine Cells with a loop to update the KB which I guess is the class sentence here. Different than puzzle.py, will have to double check this one a lot.
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        #Safe Cells with a loop (I'm very bad at loops need to get better)
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #This one seems pretty complex, Mark the Move, Mark the Cell Safe, Add to KB based on Cell and Count, Mark Additional Cells, add to KB any extra data. 
        #mark the move
        self.moves_made.add(cell)
        #mark it safe
        self.mark_safe(cell)
        #build out counters, they don't like being nested (whoopsie)
        unknownCells = []
        #this needs to be zero. You got cheeky with 1 and that wrecked this. 
        Minescount= 0
        #Update the KB with your favorite. A loop. Remember the first row is not 1, it is 0. Also it's range +2. Range function sucks sometimes. No comma after bracket, it breaks the code you big dummy. 
        for i in range(cell[0] - 1, cell[0] + 2 ):
            for j in range(cell[1] - 1, cell[1] + 2):
                #check the corners, time to use in between function and the logic you learned in puzzle.py
                if 0 <= i < self.height and 0 <= j < self.width and (i,j) not in self.mines and (i,j) not in self.safes:
                    unknownCells.append((i,j))
                if (i, j) in self.mines:
                    Minescount +=1
        #Use newSentence instead of newLogic since it uses the Sentence func. Also Minscount sounds weird but whatever. 
        newSentence = Sentence(unknownCells, count - Minescount)
        self.knowledge.append(newSentence)

        for sentence in self.knowledge:
            #mark safe and the ref is safes with an s. 
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
        #subset check
        for sentence in self.knowledge:
            if newSentence.cells.issubset(sentence.cells) and sentence.count > 0 and newSentence.count > 0 and newSentence != sentence:
                newSubset = sentence.cells.difference(newSentence.cells)
                newSentenceSubset = Sentence(list(newSubset), sentence.count - newSentence.count)
                self.knowledge.append(newSentenceSubset) 
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #More direct than above question, believe I should knock this one out first. Moves_Made is the operator here.
        for cell in self.safes:
            if cell in self.moves_made:
                return cell
        return None    
        #Second String need to return none nesting error, needs to be tabbed properly. 

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None
    
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #In order this likely gets called first but I need to build out the safe move first so we don't step on a mine, figuratively and, well figuratively. 
        #Order of operations, possible moves, check size (width, height) (is this a range deal?), check mine, and return none if conditions cannot be met. 
        possibleMoves = []
        #forgot that I matches to rows and J matches to columns. This got me for a weekend. 
        for i in range(self.height):
            for j in range(self.width):
            #so if they're not in the KB we are building with the above logic this should return with None. Tupple time! First moves and mines:
                if (i, j) not in self.moves_made and (i, j ) not in self.mines:
                #Append baby. Update, it needed double brackets. That was silly. 
                    possibleMoves.append((i,j))
        #And this is why random is improted
        if len(possibleMoves) != 0:
            #Random in possible moves, remember it is return and not print. 
            return random.choice(possibleMoves)
        else:
            return None