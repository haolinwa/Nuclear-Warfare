#GUI not fully completed
#The pieces are able to move in the internal gameboard list
#pieces are able to move internally
from time import sleep
from pygame import *
from LogicEngine import *

engine = gameEngine()
bWidth = bHeight = 720
squareSize = bWidth//8
Images = {}

def loadImages():
    pieces = ['wR','wN','wB','wQ','wK','wp','bR','bN','bB','bQ','bK','bp']
    for i in pieces:
        Images[i] = transform.scale(image.load('images/'+i+'.png'),(squareSize,squareSize))

def createBoard(wnd):
    chessBoard = image.load('images/chessBoard.png')
    chessBoard = transform.scale(chessBoard, (bWidth,bHeight))
    wnd.blit(chessBoard,(0,0))

def createPieces(wnd,gameBoard):
    for row in range(8):
        for column in range(8):
            piece = gameBoard[row][column]
            if piece != '00':
                wnd.blit(Images[piece],(column*90,row*90))

def putOnWnd(wnd):
    createBoard(wnd)
    createPieces(wnd,engine.gameBoard)
    display.update()

#main function
def main():
    init()
    wnd = display.set_mode((bWidth,bHeight))
    display.set_caption("Game")
    fps = 50
    clock = time.Clock()
    run = True
    selectedSq = ()
    alreadySelect = False
    allValidMoves = engine.getAllValidMoves()
    moveMade = False
    loadImages()
    while run:
        clock.tick(fps)
        for e in event.get():
            if e.type == QUIT:
                run = False
            if moveMade:
                allValidMoves = engine.getAllValidMoves()
                moveMade = False
            #mouse selection
            elif e.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()
                selectedSqY = pos[0]//squareSize
                selectedSqX = pos[1]//squareSize
                #Deselects if same square
                if selectedSq == (selectedSqX,selectedSqY):
                    selectedSq = ()
                    alreadySelect = False
                    print()
                else:
                    if alreadySelect == False:
                        selectedSq = (selectedSqX,selectedSqY)
                        alreadySelect = True
                    #if already selected a square selects new square
                    else:
                        newCoordinate = (selectedSqX,selectedSqY)
                        if (selectedSq,newCoordinate) in allValidMoves:
                            engine.movePiece(selectedSq,newCoordinate)
                            moveMade = True
                            putOnWnd(wnd)
                        selectedSq = ()
                        alreadySelect = False
        putOnWnd(wnd)

if __name__ == '__main__':
    main()


