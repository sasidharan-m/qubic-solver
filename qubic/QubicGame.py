import sys
import numpy as np

sys.path.append('..')
from Game import Game
from .QubicLogic import Board


class QubicGame(Game):
    """
    Connect4 Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, height=None, width=None, depth = None, win_length=None, np_pieces=None):
        Game.__init__(self)
        self._base_board = Board(height, width, depth, win_length, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return (self._base_board.height, self._base_board.width, self._base_board.depth)

    def getActionSize(self):
        return self._base_board.height * self._base_board.width * self._base_board.depth

    def getNextState(self, board, player, action):
        """Returns a copy of the board with updated move, original board is unmodified."""
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        b.add_piece(action, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        "Any zero value in top row in a valid move"
        return self._base_board.with_np_pieces(np_pieces=board).get_valid_moves()

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        winstate = b.get_win_state()
        if winstate.is_ended:
            if winstate.winner is None:
                # draw has very little value.
                return 1e-4
            elif winstate.winner == player:
                return +1
            elif winstate.winner == -player:
                return -1
            else:
                raise ValueError('Unexpected winstate found: ', winstate)
        else:
            # 0 used to represent unfinished game.
            return 0

    def getCanonicalForm(self, board, player):
        # Flip player from 1 to -1
        return board * player

    def getCubeRotations(self, a):
        # Get all combinations of axes that are permutable
        n = a.ndim
        axcomb = np.array(list(itertools.permutations(range(n), n)))

        # Initialize output array
        out = np.zeros((6,2,2,2,) + a.shape,dtype=a.dtype)

        # Run loop through all axes for flipping and permuting each axis
        for i,ax in enumerate(axcomb):
            for j,fx in enumerate([1,-1]):
                for k,fy in enumerate([1,-1]):
                    for l,fz in enumerate([1,-1]):
                        out[i,j,k,l] = np.transpose(a[::fx,::fy,::fz],ax)
        return out


    def convertListToCube(self,l):
        """This function converts a list into a cube"""
        cube = np.zeros((self._base_board.depth, self._base_board.height, self._base_board.width), dtype=np.float32)
        for i in range(self._base_board.depth):
            for j in range(self._base_board.height):
                for k in range(self._base_board.width):
                    cube[i][j][k] = l[16*i+4*j+k]
        return cube

    def convertCubeToList(self,cube):
        """This function convets a cube into a list"""
        l = []
        for i in range(self._base_board.depth):
            for j in range(self._base_board.height):
                for k in range(self._base_board.width):
                    l.append(cube[i][j][k])
        return l


    def getAllTransformations(self,a,pi):
        pi_ = self.convertListToCube(pi)
        a_out = self.get_cube_rotations(a)
        pi_out = self.get_cube_rotations(pi_)
        L = []
        for i in range(6):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        L.append((a_out[i][j][k][l], self.convertCubeToList(pi_out[i][j][k][l])))
        for i in range(len(L)):
            comp = (L[i] == a)
            uq = np.unique(comp)
            if((uq.size == 1) and (uq[0] == True)):
                del L[i]
        return L

    def getSymmetries(self, board, pi):
        """Cube has 48 possible symmetrical transformations"""
        return self.getAllTransformations(board, pi)

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))

    def getDims(self):
        return(self._base_board.depth , self._base_board.height , self._base_board.width)


def display(board):
    print(" -----------------------")
    print(' '.join(map(str, range(len(board[0])))))
    print(board)
    print(" -----------------------")
