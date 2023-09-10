import pygame as p
import chessEngine, SmartMoveFinder

xDimension = 5
yDimension = 6
squareSize = 100
pawnHeight = 85
pawnWidht = 39
rank = 20
file = 20
boardWidth = xDimension * squareSize
boardHeight = yDimension * squareSize
panelWidth = 400
panelHeight = squareSize*4.5 + rank
panelX=boardWidth + 2 * file
panelY=0
btnWidth=300
btnHeight=40
playerOne = True
playerTwo = False
maxFPS = 60

images = {}

def loadImages():
    pieces = ['bR', 'bB', 'bK', 'bQ', 'bN', 'bp', 'wR', 'wB', 'wK', 'wQ', 'wN', 'wp']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('chessAi/images/' + piece + '.png'), (pawnWidht, pawnHeight))

def isHumanTurn(gameState):
    return (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)

def isCellReset(sqSelected, location, row, col):
    return sqSelected == (row, col) or location[0]<file or location[0]>file+boardWidth or location[1]<rank or location[1]>rank+boardHeight
def validCellSelected(playerClicks):
    return len(playerClicks) == 2

def get_btn_text_position(btn, btn_text):
    textX=btn.x+btn.width/2-btn_text.get_width()/2
    textY=btn.y+btnHeight/2-btn_text.get_height()/2
    return textX,textY

def getBtn(screen,x,y, btnFont, text):
    btn=p.draw.rect(screen, p.Color("#779556"),p.Rect(x, y, 300, btnHeight), 0, 10)
    btn_text = btnFont.render(text, True, p.Color("white"))
    screen.blit(btn_text, (get_btn_text_position(btn, btn_text)))
    return btn
def configReset(screen, font):
    screen.fill(p.Color("#302e2b"))
    drawRankAndFile(screen, font)
def main():
    p.init()
    screen = p.display.set_mode((boardWidth + panelWidth + rank * 2, boardHeight + rank * 2))
    clock = p.time.Clock()

    screen.fill(p.Color("#61210F"))
    moveLogFont = p.font.SysFont('Arial', 15, True, False)
    btnFont=p.font.SysFont("Arial",20,True,False)
    gameState = chessEngine.GameState()
    validMoves = gameState.getValidMoves()

    global playerOne
    global playerTwo
    moveMade = False
    animate = False

    running = True
    gameOver = False

    sqSelected = ()
    playerClicks = []
    loadImages()
    drawRankAndFile(screen, moveLogFont)
    btnX=panelX + panelWidth / 2 - btnWidth/2
    against_human_btn=getBtn(screen,btnX,panelHeight + squareSize / 4,btnFont,"Play Against Human")
    against_computer_btn=getBtn(screen,btnX ,against_human_btn.y+btnHeight+20,btnFont,"Play Against Computer")
    chooseSide=False
    gameStarted=False
    while running:
        humanTurn = isHumanTurn(gameState)

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameStarted:
                    if chooseSide:
                        chooseSide=False
                        if playWhite.collidepoint(p.mouse.get_pos()):
                            playerOne = True
                            playerTwo = False
                            gameStarted=True
                            configReset(screen, moveLogFont)
                            reset = getBtn(screen, btnX, panelHeight + squareSize / 4, btnFont, "Reset")

                        if playBlack.collidepoint(p.mouse.get_pos()):
                            playerOne = False
                            playerTwo = True
                            gameStarted=True
                            configReset(screen, moveLogFont)
                            reset = getBtn(screen, btnX, panelHeight + squareSize / 4, btnFont, "Reset")

                    elif against_human_btn.collidepoint(p.mouse.get_pos()):
                        playerOne=True
                        playerTwo=True
                        gameStarted=True
                        configReset(screen, moveLogFont)
                        reset = getBtn(screen, btnX, panelHeight + squareSize / 4, btnFont, "Reset")
                    elif against_computer_btn.collidepoint(p.mouse.get_pos()):
                        configReset(screen, moveLogFont)
                        playWhite = getBtn(screen, btnX, panelHeight + squareSize / 4, btnFont, "Play White")
                        playBlack = getBtn(screen, btnX, playWhite.y + btnHeight + 20, btnFont, "Play Black")
                        chooseSide=True
                else:
                    if reset.collidepoint(p.mouse.get_pos()):
                        gameOver = False
                        gameState = chessEngine.GameState()
                        validMoves = gameState.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        playerOne = True
                        playerTwo = True
                        moveMade = False
                        animate = False
                        gameStarted = False

                        configReset(screen, moveLogFont)
                        against_human_btn = getBtn(screen, btnX, panelHeight + squareSize / 4, btnFont,
                                                   "Play Against Human")
                        against_computer_btn = getBtn(screen, btnX, against_human_btn.y + btnHeight + 20, btnFont,
                                                      "Play Against Computer")
                        continue
                    if not gameOver and humanTurn:

                        location = p.mouse.get_pos()
                        col = (location[0] - file) // squareSize
                        row = (location[1] - rank) // squareSize

                        if isCellReset(sqSelected, location, row, col):
                            sqSelected=()
                            playerClicks=[]
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if validCellSelected(playerClicks):
                            move = chessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)

                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gameState.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                            if not moveMade:
                                playerClicks = [sqSelected]

        if not gameOver and not humanTurn and gameStarted:
            AIMove = SmartMoveFinder.findBestMove(gameState, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)

            gameState.makeMove(AIMove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gameState, validMoves, sqSelected, moveLogFont)
        if gameState.isGameOver():
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


def drawRankAndFile(screen, font):
    files = ['a', 'b', 'c', 'd', 'e']
    ranks = ['6', '5', '4', '3', '2', '1']
    for i in range(len(files)):
        textObject = font.render(files[i], True, p.Color('white'))
        screen.blit(textObject, (squareSize * i + squareSize // 2 + rank, 0))
        screen.blit(textObject, (squareSize * i + squareSize // 2 + rank, boardHeight + rank))
    for i in range(len(ranks)):
        textObject = font.render(ranks[i], True, p.Color('white'))
        screen.blit(textObject, (rank // 2 - textObject.get_width() // 2, squareSize * i + squareSize // 2 + rank))
        screen.blit(textObject, (
            boardWidth + rank + rank // 2 - textObject.get_width() // 2, squareSize * i + squareSize // 2 + rank))


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(panelX, 0, panelWidth, panelHeight)
    p.draw.rect(screen, p.Color('#341a0e'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + moveLog[i].getChessNotation() + "   "
        if i + 1 < len(moveLog):
            moveString += moveLog[i + 1].getChessNotation()
        moveTexts.append(moveString)
    padding = 5
    lineSpacing = 2
    moveLogObj=p.font.SysFont('Arial', 25, True, True).render("MOVELOG",True, p.Color('white'))
    screen.blit(moveLogObj, moveLogRect.move(panelWidth/2-moveLogObj.get_width()/2,padding))
    textX = padding
    textY = moveLogObj.get_height()+padding
    for i in range(len(moveTexts)):
        text = moveTexts[i]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(textX, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
        if textY >= panelHeight-textObject.get_height():
            textX += textObject.get_width() + 15
            textY = moveLogObj.get_height()+padding


def drawBoard(screen):
    global colors
    colors = [p.Color("#EBECD0"), p.Color("#779556")]
    for r in range(yDimension):
        for c in range(xDimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(file + c * squareSize, rank + r * squareSize, squareSize, squareSize))


def highlightSquares(screen, gameState, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'):
            s = p.Surface((squareSize, squareSize))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * squareSize + file, r * squareSize + rank))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (squareSize * move.endCol + rank, squareSize * move.endRow + rank))
    pass


def drawPieces(screen, board):
    for r in range(yDimension):
        for c in range(xDimension):
            piece = board[r][c]
            if piece != "--":
                square_center_x = c * squareSize + squareSize // 2 + file
                square_center_y = r * squareSize + squareSize // 2 + rank

                piece_x = square_center_x - pawnWidht // 2
                piece_y = square_center_y - pawnHeight // 2

                screen.blit(images[piece], p.Rect(piece_x, piece_y, pawnWidht, pawnHeight))


def animateMove(move, screen, board, clock):
    global colors

    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    framesPerSquare = 20
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    start_x = (move.startCol * squareSize + squareSize // 2 + file, move.startRow * squareSize + squareSize // 2 + rank)
    end_x = (move.endCol * squareSize + squareSize // 2 + file, move.endRow * squareSize + squareSize // 2 + rank)

    delta_x = ((end_x[0] - start_x[0]) / frameCount, (end_x[1] - start_x[1]) / frameCount)

    for frame in range(frameCount - 1):
        current_x = (int(start_x[0] + frame * delta_x[0]), int(start_x[1] + frame * delta_x[1]))

        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]

        endSquare = p.Rect(move.endCol * squareSize + file, move.endRow * squareSize + rank, squareSize, squareSize)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)

        piece_x = current_x[0] - pawnWidht // 2
        piece_y = current_x[1] - pawnHeight // 2 

        screen.blit(images[move.pieceMoved], p.Rect(piece_x, piece_y, pawnWidht, pawnHeight))

        p.display.flip()

        clock.tick(60)





def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, True)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, boardWidth, boardHeight).move(boardWidth / 2 - textObject.get_width() / 2,
                                                              boardHeight / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)


if __name__ == '__main__':
    main()