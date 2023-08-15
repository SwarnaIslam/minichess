import pygame as p
from chessAi import chessEngine

width=320
height=384
xDimension=5
yDimension=6

squareSize=64
maxFPS=15

images={}

def loadImages():
    pieces=['bR','bB','bK','bQ','bN','bp','wR','wB','wK','wQ','wN','wp']
    for piece in pieces:
        images[piece]=p.transform.scale( p.image.load('images/'+piece+'.png'),(squareSize,squareSize))

def main():
    p.init()
    screen=p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("black"))

    gameState=chessEngine.GameState()

    loadImages()
    running=True
    sqSelected=()
    playerClicks=[]
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//squareSize
                row=location[1]//squareSize
                if sqSelected == (row,col):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)

                if len(playerClicks)==2:
                    move=chessEngine.Move(playerClicks[0],playerClicks[1],gameState.board)
                    gameState.makeMove(move)
                    sqSelected=()
                    playerClicks=[]
        drawGameState(screen, gameState)
        clock.tick(maxFPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors=[p.Color("white"), p.Color("gray")]
    for r in range(yDimension):
        for c in range(xDimension):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*squareSize, r*squareSize, squareSize, squareSize))


def drawPieces(screen,board):
    for r in range(yDimension):
        for c in range(xDimension):
            piece=board[r][c]
            if piece != "--":
                screen.blit(images[piece],p.Rect(c*squareSize, r*squareSize, squareSize, squareSize))

if __name__=='__main__':
    main()
