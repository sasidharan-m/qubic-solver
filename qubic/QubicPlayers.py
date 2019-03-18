import numpy as np
from numpy import inf
import math
from numpy.random import randint

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        d = np.random.randint(4)
        r = np.random.randint(4)
        c = np.random.randint(4)

        valids = self.game.getValidMoves(board, 1)
        a = 16*d + 4*r + c
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanConnect4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        print('\nMoves:', [i for (i, valid) in enumerate(valid_moves) if valid])

        while True:
            move = int(input())
            if valid_moves[move]: break
            else: print('Invalid move')
        return move

class MiniMaxQubicPlayer():
    def __init__(self, game):
        self.game = game

    def update_board(self, board, move, player_num):
        if board[move] == 0:
            board[move] = player_num
            return board

        else:
            print("Player: "+ str(player_num))
            print("Tried to move to location " + str(move))
            print("Which is occupied by player " + str(board[move]))
            raise Exception("CANNOT MOVE THERE!!! ")

    def utility_fcn(self, board, player):

        def returnStreaks(board):
            streak = np.zeros((76, 4), dtype=np.uint8)

            # ULTRA DIAGONALS in 3D

            # From front, top left
            streak[0] = [board[0, 0, 0],
                         board[1, 1, 1],
                         board[2, 2, 2],
                         board[3, 3, 3]]

            # From back, top left
            streak[1] = [board[3, 0, 0],
                         board[2, 1, 1],
                         board[1, 2, 2],
                         board[0, 3, 3]]

            # From front, bottom left
            streak[2] = [board[0, 3, 0],
                         board[1, 2, 1],
                         board[2, 1, 2],
                         board[3, 0, 3]]

            # From back, bottom left
            streak[3] = [board[3, 3, 0],
                         board[2, 2, 1],
                         board[1, 1, 2],
                         board[0, 0, 3]]

            # CHECK ANTI/DIAGONALS in 2D
            for cut in range(4):
                # DIAGONALS by LAYER
                streak[cut + 4] = [board[cut, 0, 0],
                                   board[cut, 1, 1],
                                   board[cut, 2, 2],
                                   board[cut, 3, 3]]

                # ANTI DIAGONALS by LAYER
                streak[cut + 8] = [board[cut, 0, 3],
                                   board[cut, 1, 2],
                                   board[cut, 2, 1],
                                   board[cut, 3, 0]]

                # DIAGONALS by ROW
                streak[cut + 12] = [board[0, cut, 0],
                                    board[1, cut, 1],
                                    board[2, cut, 2],
                                    board[3, cut, 3]]

                # ANTI DIAGONALS by ROW
                streak[cut + 16] = [board[0, cut, 3],
                                    board[1, cut, 2],
                                    board[2, cut, 1],
                                    board[3, cut, 0]]

                # DIAGONALS by COL
                streak[cut + 20] = [board[0, 0, cut],
                                    board[1, 1, cut],
                                    board[2, 2, cut],
                                    board[3, 3, cut]]

                # ANTI DIAGONALS by COL
                streak[cut + 24] = [board[0, 3, cut],
                                    board[1, 2, cut],
                                    board[2, 1, cut],
                                    board[3, 0, cut]]

            index = 28
            # STACK POINTS
            for row in range(4):
                for col in range(4):
                    streak[index] = board[0:4, row, col]
                    index = index + 1
            # ROW POINTS
            for stack in range(4):
                for row in range(4):
                    streak[index] = board[stack, row, 0:4]
                    index = index + 1
            # COL POINTS
            for stack in range(4):
                for col in range(4):
                    streak[index] = board[stack, 0:4, col]
                    index = index + 1

            return streak

        # CHECK POINTS, on each row slice (3*16 in 1d, 24 in 2d, 4 in 4d)
        def value(streak, player):

            points = 0
            for i in range(len(streak)):

                # if i==44:
                #     print streak[i]
                #     print("Player: "+str(player)+" Opponent:"+str(((player % 2) + 1))+"\n")


                if ((player % 2) + 1) in streak[i]:  # No points if opponent is present
                    # print("\t\tOpponent Present")
                    continue
                else:
                    numTokensInStreak = np.equal(streak[i], player)
                    streakScore = sum(numTokensInStreak)
                    if (streakScore == 4):
                        points = inf
                        # print("\t\tWIN!")
                        return points
                    else:
                        points = points + streakScore ** 3
                        # print("\t\tScore: " + str(streakScore ** 2))
            return points

        opponent = (player % 2) + 1
        streak = returnStreaks(board)

        utilityPlayer   = value(streak, player)
        utilityOpponent = value(streak, opponent)

        utility = utilityPlayer - utilityOpponent

        # print("Utility Player:   " +str(player)+": "+str(utilityPlayer))
        # print("Utility Opponent: " +str(opponent)+": "+str(utilityOpponent))
        # print("\nOverall Utility for player " +str(player)+": "+str(utility)+"\n\n")

        return utility

    def MaxValue(self, playerNumber, board4max, alpha, beta, depth2go4max):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4max, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4max == 0) or (abs(utility) == inf):
            return [utility, -1]


        value = -inf
        action2return = (-1,-1,-1)

        for layer in range(4):
            for row in range(4):
                for col in range(4):



                    if board4max[layer, row, col] != 0:            # Check if move is valid
                        continue

                    action = (layer, row, col)

                    if(action2return == (-1,-1,-1)):
                        action2return = action

                    child_board = board4max.copy()
                    child_board = self.update_board(child_board, action, playerNumber)




                    min_child_value = self.MinValue(playerNumber, child_board, alpha, beta, depth2go4max - 1)[0]


                    # if depth2go4max == 2:
                    #     print("Move: " + str(action) + "  Value: " + str(min_child_value))

                    if (min_child_value > value):
                        value = min_child_value
                        action2return = action

                    if value >= beta:
                        return [value, action2return]
                    alpha = max(alpha, value)


        return [value, action2return]

    def MinValue(self, playerNumber, board4min, alpha, beta, depth2go4min):

        # Determine utility, stop recurring if necessary
        utility = self.utility_fcn(board4min, playerNumber)

        # print("Utility" + str(utility) + "\n\n")
        if (depth2go4min == 0) or (abs(utility) == inf):
            return [utility, -1]

        opponent = (playerNumber % 2) + 1
        value = inf
        # action2return = (-1,-1,-1)


        for layer in range(4):
            for row in range(4):
                for col in range(4):

                    if board4min[layer, row, col] != 0:  # Check if move is valid
                        continue

                    action = (layer, row, col)

                    # if (action == (-1, -1, -1)):
                    #     action2return = action

                    child_board = board4min.copy()
                    child_board = self.update_board(child_board, action, opponent)



                    max_child_value = self.MaxValue(playerNumber, child_board, alpha, beta, depth2go4min - 1)[0]


                    if max_child_value < value:
                        value = max_child_value


                    if value <= alpha:
                        return [value, -1]
                    beta = max(beta, value)


        return [value, -1]


    def play(self, board):
        self.depth2go = 2
        self.player = 1
        self.depth = board.shape[0]
        self.rows = board.shape[1]
        self.cols = board.shape[2]
        tmp_board = np.copy(board)
        for i in range(self.depth):
            for j in range(self.rows):
                for k in range(self.cols):
                    if(tmp_board[i][j][k] == -1):
                        tmp_board[i][j][k] = 2
        [reward, action] = self.MaxValue(self.player, board, -inf, inf, self.depth2go)
        if action == -1:
            return -1
        return (16*action[0] + 4*action[1] + action[2])


class HeuristicQubicPlayer():
    def __init__(self, game):
        self.game = game
        self.move_number = 0  # odd moves are "black": black moves 1st
        self.N = 4
        self.lines, self.line_sums = self.extract_lines(self.N)
        self.points = self.initialize_point_dictionary()

    def get_possible_moves(self):
        empty = np.where(self.board == 0)
        return [(empty[0][i], empty[1][i], empty[2][i]) for i in range(len(empty[0]))]

    # Utility to extract all potential win lines (board empty).
    def extract_lines(self, N):
        ''' Extracts all potential winning "lines", returned as a list.
            Run once when a new game is initialized.   '''

        lines = []
        for i in range(N):
            # Lines // to coord directions ( 3N^2 in total ).
            for j in range(N):
                lines.append(tuple([(i, j, k) for k in range(N)]))
                lines.append(tuple([(i, k, j) for k in range(N)]))
                lines.append(tuple([(k, i, j) for k in range(N)]))

            # Short diagonals ( 6N in total ).
            #print( '** len(lines) =', len(lines)
            lines.append(tuple([(k, k, i) for k in range(N)]))
            lines.append(tuple([(N - 1 - k, k, i) for k in range(N)]))
            lines.append(tuple([(k, i, k) for k in range(N)]))
            lines.append(tuple([(N - 1 - k, i, k) for k in range(N)]))
            lines.append(tuple([(i, k, k) for k in range(N)]))
            lines.append(tuple([(i, N - 1 - k, k) for k in range(N)]))

        # Long diagonals ( 4 in total ).
        lines.append(tuple([(k, k, k) for k in range(N)]))
        lines.append(tuple([(k, k, N - 1 - k) for k in range(N)]))
        lines.append(tuple([(k, N - 1 - k, k) for k in range(N)]))
        lines.append(tuple([(N - 1 - k, k, k) for k in range(N)]))

        # Return this list of possible winning lines.
        L1 = len(lines)
        lines = list(set(lines))
        #L2 = len(lines)
        #assert L1 == L2,  'In extract_lines: LINES NOT UNIQUE!!!'

        # Also return an initialized line_sum.
        line_sum = [[0, 0, N] for _ in range(len(lines))]
        return lines, line_sum

    def initialize_point_dictionary(self):
        ''' Initializes a dictionary with the points as keys, and containing
            info about each line through each point:
            {(i, j, k):  { line_1: [#black, #white, #empty],
                                     ...
                           line_m: [#black, #white, #empty] }
                 .                    .
                 .                    .
                 .                    .
            Run when a new game is initialized.   '''
        points = dict()
        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    if (i, j, k) not in points:
                        points[(i, j, k)] = [line_num
                                             for line_num, line in enumerate(self.lines)
                                             if (i, j, k) in line]
        return points


    def board_value(self):
        ''' Input a board and its associated winning lines.
            Output a board valuation (each unoccupied array position will have a
            value equal to the number of lines through that point.
            This ignores all non-empty lines.  '''

        # Determine who made the last move.
        if self.move_number % 2 == 0:   # change the mod for additional players
            pos = True  # moves 0, 2, 4, ...  correspond to a board entry of +1 (white)
        else:
            pos = False  # moves 1, 2, 3 ...  correspond to a board entry of -1 (black)

        L = [line for line in self.lines]  # a copy of lines

        # Remove a line from the possible winning lines,
        # whenever the opponent is blocking that line.
        if pos:
            opponent = np.where(self.board == -1)
            blocked = [(opponent[0][i], opponent[1][i], opponent[2][i]) for i in range(len(opponent[0]))]
            for index in blocked:
                for line in self.lines:
                    if (index in line) and (line in L):
                        L.pop(L.index(line))
        else:
            opponent = np.where(self.board == 1)
            blocked = [(opponent[0][i], opponent[1][i], opponent[2][i]) for i in range(len(opponent[0]))]
            for index in blocked:
                for line in self.lines:
                    if (index in line) and (line in L):
                        L.pop(L.index(line))

        # Initialize valuation array.
        V = np.zeros((self.N, self.N, self.N))

        # For each array point, sum up the number of lines in input array "lines"
        # containing that point. The more lines containing a point, the more value that point.
        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    point = (i, j, k)
                    V[i, j, k] = sum([point in line for line in L])

        # Zero out any already occupied points on the game board.
        # ): Alas, all the good ones are already taken :(
        V[np.where(self.board != 0)] = 0
        return V


    def assess_board(self):
        ''' This assesses the board, from the point of view of the next player
            to move, a move_number one greater than the current self.move_number.
            white_to_move = ((self.move_number + 1) % 2 == 0)

            Here we make use of the points dictionary (one entry per point on board).
            Each entry consists of a dictionary which has for its keys the line_numbers
            of all lines through that point. Each entry of these line dictionaries
            contains a 3-tuple list wherein:

                 num_black = self.points[(i, j, k)][line_num][0]
                 num_white = self.points[(i, j, k)][line_num][1]
                 num_empty = self.points[(i, j, k)][line_num][2]

            We now use this dictionary to create an energy map of the board,
            where the occupied spaces are -inf, and the higher energies are the better
            paces to play.   '''

        E = self.board_value()  # this measures future potential
        E -= E.max() + 1  # E.max is now -1
        E[np.where(self.board != 0)] = -np.inf  # these spaces are occupied

        white_to_move = ((self.move_number % 2) == 0)

        for i in range(self.N):
            for j in range(self.N):
                for k in range(self.N):
                    if E[i, j, k] == -np.inf: continue  # already occupied

                    # Fetch the dictionary of lines through (i, j, k).
                    lines_thru_ijk = self.points[(i, j, k)]

                    for line_num in lines_thru_ijk:
                        # For each line through this point, fetch the number of black,
                        # white, and empty spaces on that line.
                        num_black = self.line_sums[line_num][0]
                        num_white = self.line_sums[line_num][1]
                        num_empty = self.line_sums[line_num][2]

                        # If 1 move away from winning (or losing), the right move is obvious!
                        if num_empty == 1:
                            if (((num_white == self.N - 1) and white_to_move) or
                                ((num_black == self.N - 1) and not white_to_move)):
                                E[i, j, k] = 400  #  moving here wins
                            elif (((num_white == self.N - 1) and not white_to_move) or
                                  ((num_black == self.N - 1) and white_to_move)):
                                E[i, j, k] = 200  #  moving here blocks opponent's win

                        # See if we're 2 moves away from winning (or losing)...
                        elif num_empty == 2:
                            # See if there's another line through this point with 2 empty spaces...
                            for line2_num in lines_thru_ijk:
                                if line2_num != line_num:
                                    # Does this one have 2 empty spaces?
                                    #num_empty2 = self.points[(i, j, k)][line2_num][2]
                                    num_empty2 = self.line_sums[line2_num][2]
                                    if num_empty2 == 2:
                                        # For each line through this point, fetch the number of black,
                                        # white, and empty spaces on that line.
                                        num_black2 = self.line_sums[line2_num][0]
                                        num_white2 = self.line_sums[line2_num][1]

                                        # Here we're looking for a win in 2 moves, or
                                        # a blocking of an opponent's win in 2 moves.
                                        if (((num_white2 == self.N - 2) and white_to_move) or
                                            ((num_black2 == self.N - 2) and not white_to_move)):
                                            E[i, j, k] = 100  #  moving here, white wins in 2 moves
                                        elif (((num_white2 == self.N - 2) and not white_to_move) or
                                            ((num_black2 == self.N - 2) and white_to_move)):
                                            E[i, j, k] = 50  #  moving here, black wins in 2 moves
                                    # We have a line with two empty spaces, one of which is on another
                                    # line with 3 empty spaces. We may want to play at one of those other
                                    # empty spaces, to set up a possible forced win, the num_empty2 = 2 case.
                                    elif num_empty2 == 3:
                                        points_on_line = self.lines[line2_num]
                                        for new_point in points_on_line:
                                            if new_point != (i, j, k) and self.board[new_point] == 0:
                                                #if E[new_point] < 10:
                                                #    E[new_point] = 10
                                                E[new_point] += 30

        #if 50 not in E and 100 not in E and 200 not in E and 400 not in E:
        return E


    def play(self, board):
        ''' Make a move. '''
        self.board = board
        # Construct an energy map E of the current game bohttp://sourceforge.net/projects/numpy/files/ard.
        E = self.assess_board()
        # Fetch a list of possible moves.
        empty = self.get_possible_moves()
        # Eliminate all moves that aren't on maximum energy spaces.
        max_energy = E.max()
        empty = [point for i, point in enumerate(empty) if E[point] == max_energy]

        #print('empty =', empty)
        # Randomly pick a move from these empty spaces.
        move = empty[randint(0, len(empty))]

        return (16*move[0] + 4*move[1] + move[2])
