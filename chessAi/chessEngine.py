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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
        if self.whiteToMove:
            if self.board[r - 1][c] == '--':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == len(self.board) - 2 and self.board[r - 2][c] == '--':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < len(self.board[r]):
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        horizontalDir = [1, -1]
        verticalDir = [1, -1]
        enemyColor = 'b' if self.whiteToMove else 'w'

        for dir in verticalDir:
            for i in range(1, len(self.board)):
                endRow = r + dir * i;

                if 0 <= endRow < len(self.board):
                    endPiece = self.board[endRow][c]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, c), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, c), self.board))
                        break
                    else:
                        break
                else:
                    break
        for dir in horizontalDir:
            for i in range(1, len(self.board[0])):
                endCol = c + dir * i;
                if 0 <= endCol < len(self.board[0]):
                    endPiece = self.board[r][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (r, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (r, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for dir in directions:
            for i in range(1, max(len(self.board), len(self.board[0]))):
                endRow = r + dir[0] * i
                endCol = c + dir[1] * i

                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
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
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKnightMoves(self, r, c, moves):
        directions=((2,-1),(2,1),(1,2),(-1,2),(1,-2),(-1,-2),(-2,1),(-2,-1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for dir in directions:
            endRow = r + dir[0]
            endCol = c + dir[1]

            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[0]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    ranksToRows = {
        "1": 6, "2": 5, "3": 4, "4": 3, "5": 2, "6": 1
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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
