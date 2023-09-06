import pygame as p
from chessAi import chessEngine, SmartMoveFinder

xDimension = 5
yDimension = 6
squareSize = 100
boardWidth = xDimension * squareSize
boardHeight = yDimension * squareSize
panelWidth = 300
panelHeight = boardHeight
rank=20
file=20
maxFPS = 15

images = {}


def loadImages():
    pieces = ['bR', 'bB', 'bK', 'bQ', 'bN', 'bp', 'wR', 'wB', 'wK', 'wQ', 'wN', 'wp']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (squareSize, squareSize))


def main():
    p.init()
    screen = p.display.set_mode((boardWidth + panelWidth+rank*2, boardHeight+rank*2))
    clock = p.time.Clock()
    screen.fill(p.Color("#52240a"))
    moveLogFont = p.font.SysFont('Arial', 15, True, False)
    gameState = chessEngine.GameState()
    validMoves = gameState.getValidMoves(31)
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne=False
    playerTwo=True
    drawRankAndFile(screen,moveLogFont)
    while running:
        humanTurn=(gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = (location[0]-file) // squareSize
                    row = (location[1]-rank) // squareSize
                    if sqSelected == (row, col) or col >= 5 or (location[0]-file)<0 or (location[1]-file)<0:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                # print(validMoves[0].startRow, validMoves[0].startCol)
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                break
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gameState = chessEngine.GameState()
                    validMoves = gameState.getValidMoves(80)
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if not gameOver and not humanTurn:
            # print(validMoves[0].startRow, validMoves[0].startCol)
            AIMove=SmartMoveFinder.findBestMoveMinMax(gameState,validMoves)
            if AIMove is None:
                print('rand')
                AIMove = SmartMoveFinder.findRandomMove(validMoves)

            gameState.makeMove(AIMove)
            moveMade=True
            animate=True
        if moveMade:
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves(99)
            moveMade = False
            animate = False
        drawGameState(screen, gameState, validMoves, sqSelected, moveLogFont)
        if gameState.checkmate or gameState.stalemate:
            gameOver = True
            drawEndGameText(screen,
                            'stalemate' if gameState.stalemate else 'black wins by checkmate' if gameState.whiteToMove else 'white wins by checkmate')
        clock.tick(maxFPS)
        p.display.flip()


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
def drawRankAndFile(screen,font):
    files=['a','b','c','d','e']
    ranks=['6','5','4','3','2','1']
    for i in range(len(files)):
        textObject = font.render(files[i], True, p.Color('white'))
        screen.blit(textObject, (squareSize*i+squareSize//2+rank,0))
        screen.blit(textObject, (squareSize*i+squareSize//2+rank,boardHeight+rank))
    for i in range(len(ranks)):
        textObject = font.render(ranks[i], True, p.Color('white'))
        screen.blit(textObject, (rank//2-textObject.get_width()//2,squareSize*i+squareSize//2+rank))
        screen.blit(textObject, (boardWidth+rank+rank//2-textObject.get_width()//2,squareSize*i+squareSize//2+rank))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(boardWidth+2*file, 0, panelWidth, 2000)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog=gs.moveLog
    moveTexts=[]
    for i in range(0,len(moveLog),2):
        moveString=str(i//2+1)+". "+moveLog[i].getChessNotation()+"   "
        if i+1 < len(moveLog):
            moveString+=moveLog[i+1].getChessNotation()
        moveTexts.append(moveString)
    padding=5
    lineSpacing=2
    textX=padding
    textY=padding
    for i in range(len(moveTexts)):
        text=moveTexts[i]
        textObject=font.render(text,True,p.Color('white'))
        textLocation=moveLogRect.move(textX, textY)
        screen.blit(textObject,textLocation)
        textY+=textObject.get_height()+lineSpacing
        if textY>=panelHeight:
            textX+=textObject.get_width()+padding*3
            textY=padding
def drawBoard(screen):
    global colors
    colors = [p.Color("#f7c899"), p.Color("#CA8745")]
    for r in range(yDimension):
        for c in range(xDimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(file+c * squareSize, rank+r * squareSize, squareSize, squareSize))


def highlightSquares(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
            s = p.Surface((squareSize, squareSize))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * squareSize+file, r * squareSize+rank))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (squareSize * move.endCol+rank, squareSize * move.endRow+rank))
    pass


def drawPieces(screen, board):
    for r in range(yDimension):
        for c in range(xDimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * squareSize+file, r * squareSize+rank, squareSize, squareSize))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * squareSize+file, move.endRow * squareSize+rank, squareSize, squareSize)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c * squareSize+file, r * squareSize+rank, squareSize, squareSize))
        p.display.flip()
        clock.tick(60)
    pass


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, True)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, boardWidth, boardHeight).move(boardWidth / 2 - textObject.get_width() / 2,
                                                              boardHeight / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)


if __name__ == '__main__':
    main()
