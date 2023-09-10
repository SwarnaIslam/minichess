import random

pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
checkmate = 1000
stalemate = 0
DEPTH = 7


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -checkmate, checkmate,  1 if gs.whiteToMove else -1)
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    orderedMoves = orderMoves(validMoves, gs)

    maxScore = -checkmate
    for i in range(1, len(orderedMoves)):
        move = orderedMoves[i]
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1,-beta,-alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore>alpha:
            alpha=maxScore
        if alpha>=beta:
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
    # Create a list to store the ordered moves
    orderedMoves = []
    
    # Define an evaluation function that assigns scores to moves
    def evaluate_move(move):
        score = 0
        
        # Prioritize captures
        if gs.isCapture(move):
            score += 100  # You can adjust this value based on your evaluation
        
        # Prioritize checks
        if gs.checkmate:
            score += 50  # You can adjust this value based on your evaluation
        
        return score
    
    # Sort validMoves based on the evaluation function
    orderedMoves = sorted(validMoves, key=evaluate_move, reverse=True)
    
    return orderedMoves


