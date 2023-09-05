class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bB", "bK", "bQ", "bN"],
            ["bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp"],
            ["wR", "wB", "wK", "wQ", "wN"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'B': self.getBishopMoves,
                              'K': self.getKingMoves, 'Q': self.getQueenMoves, 'N': self.getKnightMoves}
        self.whiteKingLocation = (5, 2)
        self.blackKingLocation = (0, 2)

        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares.append((checkRow, checkCol))
                else:
                    for i in range(1, max(len(self.board), len(self.board[0]))):
                        validSquare = (kingRow + i * check[2], kingCol + i * check[3])
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            self.getKingMoves(kingRow, kingCol, moves)
            if moves == []:
                self.checkmate = True
        else:
            moves = self.getAllPossibleMoves()
            if moves == []:
                self.stalemate = True
        return moves

    def checkForPinsAndChecks(self):
        inCheck = False
        checks = []
        pins = []

        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for i in range(len(directions)):
            direction = directions[i]
            possiblePins = ()
            for j in range(1, max(len(self.board), len(self.board[0]))):
                endRow = startRow + direction[0] * j
                endCol = startCol + direction[1] * j

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePins == ():
                            possiblePins = (endRow, endCol, direction[0], direction[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= i <= 3 and type == 'R') or (4 <= i <= 7 and type == 'B') or (
                                j == 1 and type == 'p' and (
                                (enemyColor == 'w' and 6 <= i <= 7) or (enemyColor == 'b' and 4 <= i <= 5))) or (
                                type == 'Q') or (j == 1 and type == 'K'):
                            if possiblePins == ():
                                inCheck = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possiblePins)
                                break
                        else:
                            break
                else:
                    break
        knightDirections = ((2, -1), (2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1))
        for direction in knightDirections:
            endRow = startRow + direction[0]
            endCol = startCol + direction[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, direction[0], direction[1]))

        return inCheck, pins, checks

    def switchPlayer(self):
        self.whiteToMove = not self.whiteToMove

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range((len(self.pins) - 1), -1, -1):
            if r == self.pins[i][0] and c == self.pins[i][1]:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[r - 1][c] == '--':
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
            if c - 1 >= 0:
                if not piecePinned or pinDirection == (-1, -1):
                    if self.board[r - 1][c - 1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if not piecePinned or pinDirection == (-1, 1):
                    if self.board[r - 1][c + 1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == '--':
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if c - 1 >= 0:
                if not piecePinned or pinDirection == (1, -1):
                    if self.board[r + 1][c - 1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if not piecePinned or pinDirection == (1, 1):
                    if self.board[r + 1][c + 1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range((len(self.pins) - 1), -1, -1):
            if r == self.pins[i][0] and c == self.pins[i][1]:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range((len(self.pins) - 1), -1, -1):
            if r == self.pins[i][0] and c == self.pins[i][1]:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, max(len(self.board), len(self.board[0]))):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        directions = ((1, -1), (1, 1), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0))
        allyColor = 'w' if self.whiteToMove else 'b'
        for dir in directions:
            endRow = r + dir[0]
            endCol = c + dir[1]

            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range((len(self.pins) - 1), -1, -1):
            if r == self.pins[i][0] and c == self.pins[i][1]:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((2, -1), (2, 1), (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for dir in directions:
            endRow = r + dir[0]
            endCol = c + dir[1]

            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    ranksToRows = {
        "1": 5, "2": 4, "3": 3, "4": 2, "5": 1, "6": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isCapture = self.pieceCaptured != '--'
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (
                self.pieceMoved == 'bp' and self.endRow == 5)

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        notation=self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1]!='p':
            notation=self.pieceMoved[1]+notation
        return notation

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # def __str__(self):
    #     endSquare=self.getRankFile(self.endRow,self.endCol)
    #     if self.pieceMoved[1]=='p':
    #         if self.isCapture:
    #             return self.colsToFiles[self.startCol]+'x'+endSquare
    #         else:
    #             return endSquare
    #     pass
