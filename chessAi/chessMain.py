import pygame as p
from chessAi import chessEngine

width = 320
height = 384
xDimension = 5
yDimension = 6

squareSize = 64
maxFPS = 15

images = {}


def loadImages():
    pieces = ['bR', 'bB', 'bK', 'bQ', 'bN', 'bp', 'wR', 'wB', 'wK', 'wQ', 'wN', 'wp']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (squareSize, squareSize))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))

    gameState = chessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver=False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // squareSize
                    row = location[1] // squareSize
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    for i in range(len(validMoves)):
                        if len(playerClicks) == 2:
                            move = chessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                animate=True
                                sqSelected = ()
                                playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
                    animate=False
                if e.key==p.K_r:
                    gameState=chessEngine.GameState()
                    validMoves=gameState.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
        if moveMade:
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate=False
        drawGameState(screen, gameState, validMoves, sqSelected)
        if gameState.checkmate:
            gameOver=True
            if gameState.whiteToMove:
                drawText(screen,'black wins by checkmate')
            else:
                drawText(screen,'white wins by checkmate')
        elif gameState.stalemate:
            gameOver=True
            drawText(screen,'stalemate')
        clock.tick(maxFPS)
        p.display.flip()


def highlightSquares(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
            s = p.Surface((squareSize, squareSize))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * squareSize, r * squareSize))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (squareSize * move.endCol, squareSize * move.endRow))
    pass


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(yDimension):
        for c in range(xDimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


def drawPieces(screen, board):
    for r in range(yDimension):
        for c in range(xDimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * squareSize, r * squareSize, squareSize, squareSize))


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
        endSquare = p.Rect(move.endCol * squareSize, move.endRow * squareSize, squareSize, squareSize)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c * squareSize, r * squareSize, squareSize, squareSize))
        p.display.flip()
        clock.tick(60)
    pass
def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,True)
    textObject=font.render(text,0,p.Color('Black'))
    textLocation=p.Rect(0,0,width,height).move(width/2-textObject.get_width()/2,height/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)

if __name__ == '__main__':
    main()
