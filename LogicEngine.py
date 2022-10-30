
class gameEngine():
    def __init__ (self):
        self.gameBoard =[['bR','bN','bB','bQ','bK','bB','bN','bR'],
                        ['bp','bp','bp','bp','bp','bp','bp','bp'],
                        ['00','00','00','00','00','00','00','00'],
                        ['00','00','00','00','00','00','00','00'],
                        ['00','00','00','00','00','00','00','00'],
                        ['00','00','00','00','00','00','00','00'],
                        ['wp','wp','wp','wp','wp','wp','wp','wp'],
                        ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.whiteTurn = True

    def movePiece(self,oldMTuple,newMTuple):
        self.oldY = oldMTuple[1]
        self.oldX = oldMTuple[0]
        self.newY = newMTuple[1]
        self.newX = newMTuple[0]
        self.selectedPiece = self.gameBoard[self.oldX][self.oldY]
        self.destination = self.gameBoard[self.newX][self.newY]
        #if destination empty, simply move
        if self.destination == '00':
            self.gameBoard[self.newX][self.newY] = self.selectedPiece
            self.gameBoard[self.oldX][self.oldY] = '00'
        #if target occupied (not empty), explodes
        else:
            self.explosion(self.newX,self.newY)
            self.gameBoard[self.oldX][self.oldY] = '00'
        self.whiteTurn = not self.whiteTurn

    #gets all valid moves and also determine who won
    #does all internal board processing
    def getAllValidMoves(self):
        self.allMoves = []
        self.kingAlive = [False,False]
        #checks every square on the board for valid move
        for row in range(len(self.gameBoard)):
            #checks if the white king is on board
            if 'wK' in self.gameBoard[row]:
                self.kingAlive[0] = True
            #checks if black king on board
            if 'bK' in self.gameBoard[row]:
                self.kingAlive[1] = True
            for col in range(len(self.gameBoard[row])):
                if self.gameBoard[row][col] != '00':
                    pieceColor = self.gameBoard[row][col][0]
                    #only let player move when it's their turn
                    if (pieceColor == 'w' and self.whiteTurn) or (pieceColor == 'b' and not self.whiteTurn):
                        pieceType = self.gameBoard[row][col][1]
                        if pieceType == 'p':
                            self.pawnMoves(row,col,pieceColor)
                        if pieceType == 'R':
                            self.rookMoves(row,col,pieceColor)
                        if pieceType == 'N':
                            self.knightMoves(row,col,pieceColor)
                        if pieceType == 'B':
                            self.bishopMoves(row,col,pieceColor)
                        if pieceType == 'Q':
                            self.queenMoves(row,col,pieceColor)
                        if pieceType == 'K':
                            self.kingMoves(row,col,pieceColor)
        #checks if any player has won
        if self.kingAlive[0] == False:
            self.won = 'white'
        if self.kingAlive[1] == False:
            self.won = 'black'
        return self.allMoves

    def pawnMoves(self,row,col,pieceColor):
        pieceCoordinate = (row,col)
        if pieceColor == 'w':
            #moving forward
            if self.gameBoard[row-1][col] == '00':
                self.allMoves.append((pieceCoordinate,(row-1,col)))
                if row == 6 and self.gameBoard[row-2][col] == '00':
                    self.allMoves.append((pieceCoordinate,(row-2,col)))
            #capturing
            if col-1 >= 0 and self.gameBoard[row-1][col-1][0] == 'b':
                self.allMoves.append((pieceCoordinate,(row-1,col-1)))
            if col+1 <= 7 and self.gameBoard[row-1][col+1][0] == 'b':
                self.allMoves.append((pieceCoordinate,(row-1,col+1)))
        #black pawn moves
        else:
            if self.gameBoard[row+1][col] == '00':
                self.allMoves.append((pieceCoordinate,(row+1,col)))
                if row == 1 and self.gameBoard[row+2][col] == '00':
                    self.allMoves.append((pieceCoordinate,(row+2,col)))
            if col-1 >= 0 and self.gameBoard[row+1][col-1][0] == 'w':
                self.allMoves.append((pieceCoordinate,(row+1,col-1)))
            if col+1 <= 7 and self.gameBoard[row+1][col+1][0] == 'w':
                self.allMoves.append((pieceCoordinate,(row+1,col+1)))

    def rookMoves(self,row,col,pieceColor):
        pieceCoordinate = (row,col)
        newRow = row+1
        newCol = col+1
        ###For rows
        while newRow < len(self.gameBoard):
            if self.gameBoard[newRow][col] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,col)))
            else:
                if self.gameBoard[newRow][col][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,col)))
                break
            newRow += 1
        newRow = row-1
        while newRow >= 0:
            if self.gameBoard[newRow][col] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,col)))
            else:
                if self.gameBoard[newRow][col][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,col)))
                break
            newRow -= 1
        ###For columns
        while newCol < len(self.gameBoard[0]):
            if self.gameBoard[row][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(row,newCol)))
            else:
                if self.gameBoard[row][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(row,newCol)))
                break
            newCol += 1
        newCol = col-1
        while newCol >= 0:
            if self.gameBoard[row][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(row,newCol)))
            else:
                if self.gameBoard[row][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(row,newCol)))
                break
            newCol -= 1

    def knightMoves(self,row,col,pieceColor):
        pieceCoordinate = (row,col)
        #upper 2 squares
        if row-2 >= 0:
            if col-1 >= 0:
                if self.gameBoard[row-2][col-1] == '00':
                    self.allMoves.append((pieceCoordinate,(row-2,col-1)))
                else:
                    if self.gameBoard[row-2][col-1][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row-2,col-1)))
            if col+1 < 8:
                if self.gameBoard[row-2][col+1] == '00':
                    self.allMoves.append((pieceCoordinate,(row-2,col+1)))
                else:
                    if self.gameBoard[row-2][col+1][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row-2,col+1)))
        #lower 2 squares
        if row+2 < 8:
            if col-1 >= 0:
                if self.gameBoard[row+2][col-1] == '00':
                    self.allMoves.append((pieceCoordinate,(row+2,col-1)))
                else:
                    if self.gameBoard[row+2][col-1][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row+2,col-1)))
            if col+1 < 8:
                if self.gameBoard[row+2][col+1] == '00':
                    self.allMoves.append((pieceCoordinate,(row+2,col+1)))
                else:
                    if self.gameBoard[row+2][col+1][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row+2,col+1)))
        #left 2 squares
        if col-2 >= 0:
            if row-1 >= 0:
                if self.gameBoard[row-1][col-2] == '00':
                    self.allMoves.append((pieceCoordinate,(row-1,col-2)))
                else:
                    if self.gameBoard[row-1][col-2][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row-1,col-2)))
            if row+1 < 8:
                if self.gameBoard[row+1][col-2] == '00':
                    self.allMoves.append((pieceCoordinate,(row+1,col-2)))
                else:
                    if self.gameBoard[row+1][col-2][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row+1,col-2)))
        #right 2 squares
        if col+2 < 8:
            if row-1 >= 0:
                if self.gameBoard[row-1][col+2] == '00':
                    self.allMoves.append((pieceCoordinate,(row-1,col+2)))
                else:
                    if self.gameBoard[row-1][col+2][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row-1,col+2)))
            if row+1 < 8:
                if self.gameBoard[row+1][col+2] == '00':
                    self.allMoves.append((pieceCoordinate,(row+1,col+2)))
                else:
                    if self.gameBoard[row+1][col+2][0] != pieceColor:
                        self.allMoves.append((pieceCoordinate,(row+1,col+2)))
            
    def bishopMoves(self,row,col,pieceColor):
        pieceCoordinate = (row,col)
        newRow = row+1
        newCol = col+1
        #down right diagonal
        while newRow < len(self.gameBoard) and newCol < len(self.gameBoard[0]):
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            else:
                if self.gameBoard[newRow][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,newCol)))
                break
            newRow += 1
            newCol += 1
        #down left diagonal
        newRow = row+1
        newCol = col-1
        while newRow < len(self.gameBoard) and newCol >= 0:
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            else:
                if self.gameBoard[newRow][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,newCol)))
                break
            newRow += 1
            newCol -= 1
        #up right diagonal
        newRow = row-1
        newCol = col+1
        while newRow >= 0 and newCol < len(self.gameBoard[0]):
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            else:
                if self.gameBoard[newRow][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,newCol)))
                break
            newRow -= 1
            newCol += 1
        #up left diagonal
        newRow = row-1
        newCol = col-1
        while newRow >= 0 and newCol >= 0:
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            else:
                if self.gameBoard[newRow][newCol][0] != pieceColor:
                    self.allMoves.append((pieceCoordinate,(newRow,newCol)))
                break
            newRow -= 1
            newCol -= 1
        
    def queenMoves(self,row,col,pieceColor):
        self.rookMoves(row,col,pieceColor)
        self.bishopMoves(row,col,pieceColor)

    def kingMoves(self,row,col,pieceColor):
        pieceCoordinate = (row,col)
        count = 0
        #upper 3 squares
        newRow = row-1
        newCol = col-1
        while newRow >= 0 and len(self.gameBoard[0]) > newCol >= 0 and count < 3:
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            newCol += 1
            count += 1
        #lower 3 squares
        count = 0
        newRow = row+1
        newCol = col-1
        while newRow < len(self.gameBoard) and len(self.gameBoard[0]) > newCol >= 0 and count < 3:
            if self.gameBoard[newRow][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(newRow,newCol)))
            newCol += 1
            count += 1
        #left and right squares 
        count = 0
        newCol = col-1
        while len(self.gameBoard[0]) > newCol >= 0 and count <= 1:
            if self.gameBoard[row][newCol] == '00':
                self.allMoves.append((pieceCoordinate,(row,newCol)))
            newCol += 2
            count += 1

    '''              
    def isValidMove(self,oldMTuple,newMTuple):
        self.oldY = oldMTuple[0]
        self.oldX = oldMTuple[1]
        self.newY = newMTuple[0]
        self.newX = newMTuple[1]
        self.selectedPiece = self.gameBoard[self.oldX][self.oldY]
        self.destination = self.gameBoard[self.newX][self.newY]
        #if selected empty, move invalid
        if self.selectedPiece == '00':
            return False
        #checks if destination piece color is the same 
        #if same then move is invalid
        if self.selectedPiece[0] == self.destination[0]:
            return False
        #Pawn
        if self.selectedPiece == 'bp':
            return False
        #King
        if self.selectedPiece == 'bK' or self.selectedPiece == 'wK':
            if abs(self.newX-self.oldX) == 1 and abs(self.newY-self.newY) == 1:
                return True
            return False
        #Rook
        if self.selectedPiece == 'bR' or self.selectedPiece == 'wR':
            if self.oldX == self.newX or self.oldY == self.newY:
                for x in range(self.oldX+1,self.newX):
                    if self.gameBoard[x,self.oldY] != '00':
                        return False
                for y in range(self.oldY+1,self.newY):
                    if self.gameBoard[self.oldX,y] != '00':
                        return False
                return True
            return False
        #Knight
        if self.selectedPiece == 'bR' or self.selectedPiece == 'wR':
            return True
        '''
        
   
        

    def explosion(self,row,col):
        #explodes all pieces in 3x3 squares except pawns
        self.gameBoard[row][col] = '00'
        #upper 3 squares
        count = 0
        newRow = row-1
        newCol = col-1
        while newRow >= 0 and len(self.gameBoard[0]) > newCol >= 0 and count < 3:
            if self.gameBoard[newRow][newCol][1] != 'p':
                self.gameBoard[newRow][newCol] = '00'
            newCol += 1
            count += 1
        #lower 3 squares
        count = 0
        newRow = row+1
        newCol = col-1
        while newRow < len(self.gameBoard) and len(self.gameBoard[0]) > newCol >= 0 and count < 3:
            if self.gameBoard[newRow][newCol][1] != 'p':
                self.gameBoard[newRow][newCol] = '00'
            newCol += 1
            count += 1
        #left and right squares 
        count = 0
        newCol = col-1
        while len(self.gameBoard[0]) > newCol >= 0 and count <= 1:
            if self.gameBoard[row][newCol][1] != 'p':
                self.gameBoard[row][newCol] = '00'
            newCol += 2
            count += 1
        '''self.gameBoard[self.newX][self.newY] = '00'
        if self.gameBoard[x-1][y] != 'bp' or 'wp':
            self.gameBoard[x-1][y] = '00'
        if self.gameBoard[x+1][y] != 'bp' or 'wp':
            self.gameBoard[x+1][y] = '00'
        if self.gameBoard[x][y-1] != 'bp' or 'wp':
            self.gameBoard[x][y-1] = '00'
        if self.gameBoard[x][y+1] != 'bp' or 'wp':
            self.gameBoard[x][y+1] = '00'
        if self.gameBoard[x+1][y+1] != 'bp' or 'wp':
            self.gameBoard[x+1][y+1] = '00'
        if self.gameBoard[x-1][y-1] != 'bp' or 'wp':
            self.gameBoard[x-1][y-1] = '00'
        if self.gameBoard[x+1][y-1] != 'bp' or 'wp':
            self.gameBoard[x+1][y-1] = '00'
        if self.gameBoard[x-1][y+1] != 'bp' or 'wp':
            self.gameBoard[x-1][y+1] = '00'
        '''

    
