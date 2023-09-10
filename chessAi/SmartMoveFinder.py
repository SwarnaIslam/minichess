import random
import time

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
checkmate = 1000
stalemate = 0
DEPTH = 7


def findRandomMove(validMoves):
    print('Random move is used')
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove
    global undoC
    global moveC
    undoC = 0
    moveC = 0
    nextMove = None
    random.shuffle(validMoves)

    start_time = time.time()
    
    findMoveNegaMaxAlphaBetaPVS(gs, validMoves, DEPTH, -checkmate, checkmate, 1 if gs.whiteToMove else -1)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Time taken to find a move: {:.2f} seconds".format(elapsed_time))
    print('Move counted: ', moveC)

    return nextMove


def findMoveNegaMaxAlphaBetaPVS(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    global undoC
    global moveC
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    orderedMoves = orderMoves(validMoves, gs)
    
    maxScore = -checkmate
    
    if len(orderedMoves) > 0:
        move = orderedMoves[0]
        gs.makeMove(move)
        moveC = moveC + 1
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaPVS(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        undoC = undoC + 1
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH :
                nextMove = move
            alpha = max(alpha, score)
            if alpha >= beta:
                return maxScore
    
    
    for i in range(1, len(orderedMoves)):
        move = orderedMoves[i]
        gs.makeMove(move)
        moveC = moveC + 1
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaPVS(gs, nextMoves, depth - 1, -alpha - 1, -alpha, -turnMultiplier)
        
        if alpha < score < beta:
            score = -findMoveNegaMaxAlphaBetaPVS(gs, nextMoves, depth - 1, -beta, -score, -turnMultiplier)
        
        gs.undoMove()
        undoC = undoC + 1
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH: 
                nextMove = move
            alpha = max(alpha, score)
            if alpha >= beta:
                break
    
    return maxScore


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate
        else:
            return checkmate
    elif gs.stalemate:
        return stalemate
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def orderMoves(validMoves, gs):
    orderedMoves = []
    
   
    def evaluate_move(move):
        score = 0
        if move.pieceCaptured!='--':
            score += pieceScore[move.pieceCaptured[1]] / 2
        if gs.checkmate:
            if gs.whiteToMove:
                score -= checkmate
            else:
                score+= checkmate
        return score
    
    orderedMoves = sorted(validMoves, key=evaluate_move, reverse=True)

    # print('Total moves: ', len(orderedMoves))
    
    return orderedMoves[:10]


